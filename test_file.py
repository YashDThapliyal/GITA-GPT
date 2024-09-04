import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import json


# Load FAISS index and model
index = faiss.read_index('gita_index.faiss')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load pre-trained model and tokenizer
model_name = "EleutherAI/gpt-neo-1.3B"  # You can also use "EleutherAI/gpt-neo-2.7B" for a larger model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
llm = GPTNeoForCausalLM.from_pretrained(model_name)


with open('gita_data.json', 'r') as f:
    gita_data = json.load(f)

def retrieve_verses(query, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return indices[0]

def get_verse_texts(indices):
    return [gita_data[i]['translation'] for i in indices]


def process_query_with_llm(query):
    try:
        return generate_text(query)
    except Exception as e:
        print(f"Error in GPT-2 inference: {e}")
        return "Error generating response."


def generate_text(prompt, max_length=150, num_return_sequences=1):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = llm.generate(
        inputs["input_ids"], 
        max_length=max_length, 
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,  # Avoid repetition
        early_stopping=True
    )
    return [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]



def main():
    query = "What is the duty of a warrior?"  

    # Retrieve relevant verses
    relevant_indices = retrieve_verses(query)
    print(relevant_indices)
    
    relevant_verses = get_verse_texts(relevant_indices)
    
    # Generate response using GPT-2
    response = process_query_with_llm(query)

    print("Relevant Verses:")
    for verse in relevant_verses:
        print(verse)
    
    print("Response from GPT-2:")
    print(response)

if __name__ == "__main__":
    main()
