import streamlit as st
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import requests  # For API calls

# Load FAISS index and model
index = faiss.read_index('gita_index.faiss')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load Gita data
with open('gita_data.json', 'r') as f:
    gita_data = json.load(f)

# Function to retrieve relevant verses
def retrieve_verses(query, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return indices[0]

# Function to get the text of the verses
def get_verse_texts(indices):
    return [gita_data[i]['translation'] for i in indices]

# Placeholder function for GPT-Neo API call
def generate_text(prompt):
    return "Hello world!"
    """
    api_url = "YOUR_GPT_NE0_API_ENDPOINT"  # Replace with your GPT-Neo API endpoint
    headers = {
        "Authorization": "Bearer YOUR_API_KEY"  # Replace with your API key if needed
    }
    payload = {
        "inputs": prompt
    }
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()['choices'][0]['text']  # Adjust this based on API response
"""

# Streamlit app
def main():
    st.title("Gita GPT Retrieval System")

    query = st.text_input("Enter your query:")

    if query:
        # Retrieve relevant verses
        relevant_indices = retrieve_verses(query)
        relevant_verses = get_verse_texts(relevant_indices)

        # Display relevant verses
        st.subheader("Relevant Verses:")
        for verse in relevant_verses:
            st.write(verse)

        # Generate response using GPT-Neo
        response = generate_text(query)
        st.subheader("Response from GPT-Neo:")
        st.write(response)

if __name__ == "__main__":
    main()
