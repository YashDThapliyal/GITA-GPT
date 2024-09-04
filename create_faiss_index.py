import faiss
import numpy as np
import json

with open('embeddings.json', 'r') as file:
    embeddings = np.array(json.load(file))

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, 'gita_index.faiss')
