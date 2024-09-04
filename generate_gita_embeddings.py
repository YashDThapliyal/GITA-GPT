from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('gita_data.json', 'r') as file:
    data = json.load(file)

verses = [item['translation'] for item in data]
embeddings = model.encode(verses)

with open('embeddings.json', 'w') as file:
    json.dump(embeddings.tolist(), file)
