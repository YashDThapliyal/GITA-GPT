# GITA-GPT: Exploring the Bhagavad Gita with RAG Architecture

## Overview

**GITA-GPT** is a project designed to answer questions based on the teachings of the Bhagavad Gita using advanced AI technologies. Leveraging the Retrieval-Augmented Generation (RAG) architecture, vector databases, and a Meta's LLAMA large language model via the GROQ API, this tool offers insights into the ancient text in a modern, interactive way.


## How It Works

1. **Data Preparation:**
   - Convert and clean the Bhagavad Gita text into JSON format for processing.

2. **Embedding Generation:**
   - Compute embeddings for each verse to capture semantic meaning.

3. **Index Creation:**
   - Build a FAISS index to allow efficient retrieval of similar verses based on a given query.

4. **Query Handling:**
   - Use RAG architecture to combine retrieved verses with generated text for a comprehensive response.

5. **User Interface:**
   - Deploy a Streamlit app that allows users to input questions and view relevant verses and AI-generated responses.
