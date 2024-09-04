import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

# Load FAISS index and model
index = faiss.read_index('gita_index.faiss')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load Gita data
with open('gita_data.json', 'r') as f:
    gita_data = json.load(f)

def retrieve_verses(query, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return indices[0]

def get_verse_texts(indices):
    return [gita_data[i]['translation'] for i in indices]

def process_query_with_llm(query):
    # Placeholder for LLM call
    return "This is where the response from the LLM will be generated."

# Embed external CSS
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit app layout
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<h1>Gita GPT Retrieval System</h1>', unsafe_allow_html=True)
st.markdown('<p>Ask a question about the Bhagavad Gita and get relevant verses and insights.</p>', unsafe_allow_html=True)

query = st.text_input('Enter your question:')

if st.button('Submit'):
    if query:
        # Retrieve relevant verses
        relevant_indices = retrieve_verses(query)
        relevant_verses = get_verse_texts(relevant_indices)
        
        # Generate response using LLM
        response = process_query_with_llm(query)

        # Display results
        st.markdown('<h2>Relevant Verses:</h2>', unsafe_allow_html=True)
        for verse in relevant_verses:
            st.markdown(f'<p>{verse}</p>', unsafe_allow_html=True)

        st.markdown('<h2>Response from LLM:</h2>', unsafe_allow_html=True)
        st.markdown(f'<p>{response}</p>', unsafe_allow_html=True)
    else:
        st.error("Please enter a question before submitting.")
    
st.markdown('</div>', unsafe_allow_html=True)
