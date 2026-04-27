# 📄 Chat with PDF (RAG AI)

An AI-powered Retrieval-Augmented Generation (RAG) system that allows users to upload PDFs and ask natural language questions.  
The system retrieves the most relevant page content and generates grounded answers using LLMs.

---

# 🚀 Project Overview

This project enables users to:
- Upload PDF documents
- Ask questions in natural language
- Get accurate answers grounded strictly in the document
- View source page references for transparency

---

# 🏗️ Architecture / Flow

PDF Upload
↓
Text Extraction (PyPDF)
↓
Page-wise Chunking
↓
Embedding Generation (SentenceTransformer)
↓
Store Vector Representations
↓
User Query Input
↓
Cosine Similarity Search
↓
Top Matching Chunk Selection
↓
LLM Processing (Groq - LLaMA 3)
↓
Final Answer + Page Source


---

# ⚙️ Project Setup Instructions

## 🔧 Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt
```

Create .env file:
GROQ_API_KEY=your_api_key_here

**Run backend:** uvicorn main:app --reload
Backend runs at: http://127.0.0.1:8000

## 💻 Frontend (React)

cd frontend
npm install
npm run dev
Frontend runs at: http://localhost:5173

---
# 🤖AI Tools and Models Used
Embedding Model: intfloat/e5-base-v2
LLM: llama-3.1-8b-instant (Groq API)
Backend: FastAPI
Frontend: React.js
PDF Parsing: PyPDF
Similarity Search: Cosine Similarity (scikit-learn)

---

# 🧠AI Approach Used (RAG System)

This project uses Retrieval-Augmented Generation (RAG):
   1. Extract text from PDF
   2. Split into page-aware chunks
   3. Convert chunks into embeddings
   4. Store embeddings in memory
   5. Convert user query into embedding
   6. Perform similarity search
   7. Retrieve most relevant chunk
   8. Send only relevant content to LLM
   9. Generate final grounded answer

---

# ✍️Prompt Design

A strict prompt is used to avoid hallucination:

You are a STRICT document QA assistant.

RULES:
 - Use ONLY the provided context
 - Do NOT use external knowledge
 - Do NOT guess or hallucinate
 - If answer is not present, say: Not available in document
 - Keep answers short and factual

---

**🛡️Handling Hallucinations / Incorrect Answers**

To ensure accuracy:
 - Low similarity threshold filtering (< 0.30)
 - Only top relevant chunk is passed to LLM
 - Strict system prompt enforcement
Fallback response:
        Not available in document

This ensures answers are always document-grounded.
---

# Features

 📄 PDF upload
 🧠 AI-powered Q&A
 📍 Page number reference
 🔎 Source highlighting
 💬 Chat history
 ⚡ Fast semantic search
---

# ⚠️Limitations
 - Works only with text-based PDFs (no OCR)
 - Limited cross-page reasoning
 - Large PDFs may slow processing
 - Depends on embedding similarity accuracy

# 🚀Possible Improvements
 - OCR support for scanned PDFs
 - Multi-PDF knowledge base
 - Hybrid search (BM25 + embeddings)
 - Streaming responses (real-time AI typing)
 - Better UI with PDF highlight viewer
 - Persistent database chat history
 - Cloud deployment (Vercel + Render)
---
