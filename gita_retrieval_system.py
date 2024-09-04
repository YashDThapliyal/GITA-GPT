import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


index = faiss.read_index('gita_index.faiss')

model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_verses(query, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return indices[0]


"""
query = "What is the duty of a warrior?" #test retrieval
relevant_verses = retrieve_verses(query)
print(relevant_verses)
"""