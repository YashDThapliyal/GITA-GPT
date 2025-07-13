from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import chromadb
from groq import Groq
import os
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="GITA-GPT API", version="1.0.0")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware - this is crucial for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable not set")

# Initialize clients
client = Groq(api_key=GROQ_API_KEY)
chroma_client = chromadb.CloudClient(
    api_key=os.environ["CHROMA_CLOUD_API_KEY"],
    tenant=os.environ["CHROMA_CLOUD_TENANT"],
    database="gita_verses"
)
collection = chroma_client.get_collection("gita_verses")

class QueryRequest(BaseModel):
    query: str
    num_verses: int = 3

class QueryResponse(BaseModel):
    query: str
    ai_response: str
    verses: List[dict]
    related_questions: List[str]

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/test")
async def test_frontend():
    return FileResponse("test_frontend.html")

@app.post("/api/query")
async def process_query(request: QueryRequest):
    try:
        # Get verses from ChromaDB
        results = collection.query(
            query_texts=[request.query],
            n_results=request.num_verses
        )
        
        # Process verses
        verses = []
        for i, (doc, metadata, distance) in enumerate(zip(
            results['documents'][0], 
            results['metadatas'][0], 
            results['distances'][0]
        )):
            # Truncate long verses
            text = doc[:500] + "..." if len(doc) > 500 else doc
            verses.append({
                "chapter": metadata.get('chapter_number', 'Unknown'),
                "verse": metadata.get('verse_number', 'Unknown'),
                "text": text,
                "similarity": round((1 - distance) * 100, 1)
            })
        
        # Create simple context
        context = f"Question: {request.query}\n\nRelevant verses:\n"
        for verse in verses:
            context += f"Chapter {verse['chapter']}, Verse {verse['verse']}: {verse['text']}\n"
        
        # Create improved, structured prompt
        prompt = f"""
        You are a wise and friendly AI assistant specializing in the Bhagavad Gita.
        Answer the following question using only the provided verses.
        - Start with a brief summary in 1-2 sentences.
        - Then, provide a detailed answer, referencing the verses as needed.
        - Use bullet points or numbered lists for clarity if appropriate.
        - Highlight key concepts in bold (use **double asterisks** for bold).
        - End with a practical takeaway or reflection for the user.

        Question: {request.query}

        Relevant verses:
        {context}

        Please provide a clear, insightful, and structured answer.
        """

        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.5,
            max_tokens=1024,
        )
        
        ai_response = chat_completion.choices[0].message.content
        
        # Generate dynamic related questions using the LLM
        related_prompt = f"""
        Based on the following question and answer, suggest 3 related questions a user might ask next. Return only the questions as a numbered list.
        
        Question: {request.query}
        Answer: {ai_response}
        """
        related_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": related_prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=256,
        )
        related_text = related_completion.choices[0].message.content
        # Parse the LLM's numbered list into a Python list
        related_questions = re.findall(r"\d+\.\s*(.*)", related_text)
        if not related_questions:
            # fallback: split by lines if no numbers found
            related_questions = [q.strip('- ').strip() for q in related_text.split('\n') if q.strip()]
        
        return {
            "query": request.query,
            "ai_response": ai_response,
            "verses": verses,
            "related_questions": related_questions
        }
        
    except Exception as e:
        error_message = handle_groq_error(e)
        raise HTTPException(status_code=500, detail=error_message)

def handle_groq_error(error):
    """Handle different types of Groq API errors with user-friendly messages"""
    error_str = str(error)
    
    # Rate limit errors
    if "413" in error_str or "rate_limit" in error_str.lower() or "tokens per minute" in error_str.lower():
        return {
            "error_type": "rate_limit",
            "message": "The AI service is currently experiencing high demand. Please wait a moment and try again.",
            "user_message": "🌊 The divine wisdom is in high demand right now. Please wait a moment and try again.",
            "retry_after": 60
        }
    
    # Model capacity errors
    if "model_decommissioned" in error_str.lower() or "model not found" in error_str.lower():
        return {
            "error_type": "model_unavailable",
            "message": "The AI model is temporarily unavailable. Please try again later.",
            "user_message": "🕉️ The divine connection is temporarily unavailable. Please try again in a few moments.",
            "retry_after": 300
        }
    
    # Token limit errors
    if "payload too large" in error_str.lower() or "request too large" in error_str.lower():
        return {
            "error_type": "token_limit",
            "message": "The request was too large. Please try a shorter question.",
            "user_message": "📝 Your question is too detailed. Please try a shorter, more focused question.",
            "retry_after": 0
        }
    
    # Authentication errors
    if "401" in error_str or "unauthorized" in error_str.lower():
        return {
            "error_type": "auth_error",
            "message": "Authentication error with the AI service.",
            "user_message": "🔐 There's an issue with the divine connection. Please contact support.",
            "retry_after": 0
        }
    
    # Network errors
    if "timeout" in error_str.lower() or "connection" in error_str.lower():
        return {
            "error_type": "network_error",
            "message": "Network connection error.",
            "user_message": "🌐 The divine connection is weak. Please check your internet and try again.",
            "retry_after": 30
        }
    
    # Generic error
    return {
        "error_type": "unknown_error",
        "message": f"An unexpected error occurred: {str(error)}",
        "user_message": "✨ The divine wisdom is temporarily unavailable. Please try again later.",
        "retry_after": 60
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "GITA-GPT API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 