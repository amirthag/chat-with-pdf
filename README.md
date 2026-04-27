Chat with PDF (RAG AI)

An AI-powered Retrieval-Augmented Generation (RAG) system that allows users to upload PDFs and ask questions based strictly on document content using semantic search + LLM.

🚀Project Overview
This project enables users to:

Upload PDF documents
Ask natural language questions
Get answers strictly grounded in the document
View page-wise source references
See confidence score for each answer

It combines:

Embedding-based retrieval
Cosine similarity search
LLM-based answer generation (Groq LLaMA 3)

🏗️ Architecture / System Flow
User → Upload PDF
        ↓
PDF Parser (PyPDF)
        ↓
Text Chunking (page-aware)
        ↓
Sentence Transformer Embeddings
        ↓
Cosine Similarity Search
        ↓
Top Matching Chunk Selected
        ↓
Prompt Construction
        ↓
LLM (Groq - LLaMA 3)
        ↓
Final Answer + Page Source Returned

🧠 AI Models & Tools Used
🔹 Embedding Model
intfloat/e5-base-v2
Converts text into vector embeddings for semantic search
🔹 LLM (Answer Generation)
llama-3.1-8b-instant via Groq API
🔹 NLP Techniques
Cosine Similarity
Semantic Retrieval (RAG)
Text Chunking (page-aware)
🔹 Backend
FastAPI (Python)
🔹 Frontend
React + Axios

💬 Prompt Used 
🔹 System Prompt
You are a STRICT document QA assistant.
Never use external knowledge.
Answer ONLY from the given context.
If answer is not present, say:
Not available in document
🔹 User Prompt Template
You are a STRICT document QA system.

RULES:
- Use ONLY provided page content
- Do NOT use outside knowledge
- Do NOT guess or infer
- If answer is not present, say exactly:
  Not available in document

PAGE CONTENT:
{page_text}

QUESTION:
{query}

📌 Features
PDF Upload
Semantic Search (RAG)
Page-wise Answer Source
Confidence Score
Chat History
Drag & Drop Upload UI
Strict hallucination control

⚠️ Limitations
Works best on text-based PDFs (not scanned images)
Retrieval depends on embedding quality
Large PDFs may reduce response speed
Single-best chunk used for answer (not multi-page reasoning)
Requires API key for Groq LLM

🚀 Possible Improvements
🔥 1. Multi-page reasoning

Combine multiple relevant chunks instead of single page

🔥 2. Better UI/UX
Highlight exact answer in PDF
Page jump navigation
Inline citations like ChatGPT
🔥 3. Streaming Responses

Real-time typing effect for answers

🔥 4. Database Storage

Store chat history permanently (MongoDB / PostgreSQL)

🔥 5. Authentication

User login system for multi-user support



⚙️ Project Setup Instructions
🔧 1. Clone Repository
git clone https://github.com/your-username/chat-with-pdf-rag.git
cd chat-with-pdf-rag
🐍 2. Backend Setup
cd backend
pip install -r requirements.txt
▶️ Run Backend
uvicorn main:app --reload

Backend runs at:

http://127.0.0.1:8000
🌐 3. Frontend Setup
cd frontend
npm install
npm run dev

Frontend runs at:

http://localhost:5173
🔐 4. Environment Variables

Create .env inside backend:

GROQ_API_KEY=your_api_key_here