from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel
import numpy as np
import os
import re
import io

# -----------------------------
# ENV
# -----------------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -----------------------------
# APP
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# MODEL
# -----------------------------
embedder = SentenceTransformer("intfloat/e5-base-v2")

# -----------------------------
# STORAGE (MULTI PDF READY)
# -----------------------------
pdf_chunks = []
pdf_embeddings = None

# -----------------------------
# REQUEST MODEL (FIX 422 ERROR)
# -----------------------------
class QueryRequest(BaseModel):
    query: str

# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

# -----------------------------
# CHUNKING (PAGE AWARE)
# -----------------------------
def chunk_page_text(text, page_num, chunk_size=600):
    sentences = text.split(". ")
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < chunk_size:
            current += sentence + ". "
        else:
            chunks.append({
                "text": current.strip(),
                "page": page_num
            })
            current = sentence + ". "

    if current:
        chunks.append({
            "text": current.strip(),
            "page": page_num
        })

    return chunks

# -----------------------------
# UPLOAD PDF (MULTI SUPPORT)
# -----------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    global pdf_chunks, pdf_embeddings

    reader = PdfReader(io.BytesIO(await file.read()))

    new_chunks = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if not text:
            continue

        text = clean_text(text)
        new_chunks.extend(chunk_page_text(text, page_num))

    if not new_chunks:
        return {"message": "No readable text found"}

    # append for multi PDF support
    pdf_chunks.extend(new_chunks)

    pdf_embeddings = embedder.encode(
        [c["text"] for c in pdf_chunks],
        normalize_embeddings=True
    )

    return {
        "message": "PDF uploaded successfully",
        "pages": len(reader.pages),
        "total_chunks": len(pdf_chunks)
    }

# -----------------------------
# ASK (STRICT RAG ENGINE)
# -----------------------------
@app.post("/ask")
async def ask(req: QueryRequest):

    query = req.query

    if not pdf_chunks or pdf_embeddings is None:
        return {"answer": "Please upload a PDF first"}

    # -----------------------------
    # SEARCH
    # -----------------------------
    query_embedding = embedder.encode([query], normalize_embeddings=True)
    scores = cosine_similarity(query_embedding, pdf_embeddings)[0]

    best_index = int(np.argmax(scores))
    best_score = float(scores[best_index])

    if best_score < 0.30:
        return {
            "answer": "Not available in document",
            "confidence": best_score,
            "source": None
        }

    page_num = pdf_chunks[best_index]["page"]
    page_text = pdf_chunks[best_index]["text"]

    # -----------------------------
    # STRICT PROMPT (NO EXPLANATION ALLOWED)
    # -----------------------------
    prompt = f"""
You are a STRICT EXTRACTION SYSTEM.

CRITICAL RULES:
- Output ONLY the final answer
- NO explanations
- NO notes
- NO reasoning
- NO formatting text
- NO "Answer:" prefix
- NO commentary
- ONLY extract relevant content from text

If answer is not present, output exactly:
Not available in document

DOCUMENT TEXT:
{page_text}

QUESTION:
{query}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict extractor. Return only raw extracted text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content.strip()

        # -----------------------------
        # POST CLEANING (IMPORTANT FIX)
        # -----------------------------
        answer = re.sub(r"\bAnswer:\b", "", answer)
        answer = re.sub(r"\n+", " ", answer).strip()
        answer = re.sub(r"\s{2,}", " ", answer)

        return {
            "answer": answer,
            "confidence": best_score,
            "source": {
                "page": page_num,
                "text": page_text
            }
        }

    except Exception:
        return {
            "answer": "Error processing request",
            "confidence": 0.0,
            "source": None
        }