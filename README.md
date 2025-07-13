# GITA-GPT

A modern AI-powered Q&A system for the Bhagavad Gita, using Retrieval-Augmented Generation (RAG) with ChromaDB Cloud, FastAPI, and a beautiful custom frontend.

---

## Features
- **Ask any question** about the Bhagavad Gita and get context-aware answers
- **Semantic search** over verses using vector embeddings
- **FastAPI backend** with Groq LLM integration
- **ChromaDB Cloud** for scalable, managed vector search
- **Modern frontend** (HTML/CSS/JS) with smooth UX

---

## Quick Start

### 1. Clone & Install
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
export GROQ_API_KEY=your_groq_api_key
export CHROMA_CLOUD_API_KEY=your_chroma_cloud_api_key
export CHROMA_CLOUD_TENANT=your_chroma_cloud_tenant_id
```

### 3. Upload Embeddings to ChromaDB Cloud
```bash
python create_chroma_index.py
```

### 4. Run the Backend
```bash
python api.py
```

### 5. Open the Frontend
Go to [http://localhost:8000](http://localhost:8000) in your browser.

---

## Project Structure
```
GITA-GPT/
├── api.py                  # FastAPI backend (cloud-native)
├── create_chroma_index.py  # Embedding upload to ChromaDB Cloud
├── gita_data.json          # Bhagavad Gita data (JSON)
├── requirements.txt        # Python dependencies
├── static/                 # Frontend (HTML, CSS, JS)
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── vercel.json             # Vercel deployment config (optional)
└── README.md               # This file
```

---

## Tech Stack
- **Backend:** FastAPI, ChromaDB Cloud, Groq LLM
- **Frontend:** HTML, CSS, JavaScript
- **Embeddings:** SentenceTransformers (MiniLM-L6-v2)

---

## Deployment

### Vercel (Recommended)
- Connect your repo to Vercel
- Set environment variables in the Vercel dashboard
- Deploy!

### Traditional Hosting
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

---

## Customization
- Change the LLM model in `api.py` if desired
- Adjust the number of verses returned in the frontend or backend
- Style the frontend in `static/styles.css`

---

## License
MIT

---

**Built with ❤️ for learning, exploration, and sharing the wisdom of the Gita.**
