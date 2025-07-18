<img width="1560" height="865" alt="Screenshot 2025-07-14 at 7 21 31 PM" src="https://github.com/user-attachments/assets/a99aafc1-8820-4ed5-b63a-788e279d2938" />

# GITA-GPT

DEMO: https://youtu.be/_aAi9S8k2yE

A modern AI-powered Q&A system for the Bhagavad Gita, using Retrieval-Augmented Generation (RAG) with ChromaDB Cloud, FastAPI, and a beautiful custom frontend.

---

## Features
- **Ask any question** about the Bhagavad Gita and get context-aware answers
- **Semantic search** over verses using vector embeddings
- **FastAPI backend** with Groq LLM integration
- **ChromaDB Cloud** for scalable, managed vector search
- **Modern frontend** (HTML/CSS/JS) with smooth UX


To run the code simply do:

```bash
#0 Get a GROQ API key and store it as GROQ_API_KEY

# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the API server
python api.py
