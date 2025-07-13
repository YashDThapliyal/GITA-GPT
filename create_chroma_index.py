import chromadb
import os
import json
from sentence_transformers import SentenceTransformer

client = chromadb.CloudClient(
    api_key=os.environ["CHROMA_CLOUD_API_KEY"],
    tenant=os.environ["CHROMA_CLOUD_TENANT"],
    database="gita_verses"
)
collection = client.get_or_create_collection("gita_verses")

with open("gita_data.json", "r") as f:
    data = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
metadatas = []
ids = []

def safe_meta_value(val):
    if val is None:
        return ""
    if isinstance(val, (int, float, str, bool)):
        return val
    return str(val)

for i, item in enumerate(data):
    text = item.get("chapter_text") or item.get("text") or ""
    documents.append(text)
    metadatas.append({
        "chapter_number": safe_meta_value(item.get("chapter_number")),
        "verse_number": safe_meta_value(item.get("verse_number")),
        "source": "gita"
    })
    ids.append(f"verse_{i}")

batch_size = 100
for i in range(0, len(documents), batch_size):
    batch_docs = documents[i:i+batch_size]
    batch_metas = metadatas[i:i+batch_size]
    batch_ids = ids[i:i+batch_size]
    collection.add(
        documents=batch_docs,
        metadatas=batch_metas,
        ids=batch_ids
    )

print(f"✅ Uploaded {len(documents)} verses to ChromaDB Cloud!") 