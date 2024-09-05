import requests
import json

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Generate text
def generate_text(prompt, max_length=150, num_return_sequences=1):
    data = {
        "model": "llama3.1:latest",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": max_length,
            "stop": ["\n\n"],  # Stop generation at double newline
        }
    }

    responses = []
    for _ in range(num_return_sequences):
        response = requests.post(OLLAMA_API_URL, json=data)
        if response.status_code == 200:
            result = json.loads(response.text)
            responses.append(result['response'])
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    
    return responses

if __name__ == "__main__":
    prompt = "What is the duty of a warrior?"  # Replace with your query
    generated_texts = generate_text(prompt)
    
    print("Generated Texts:")
    for i, text in enumerate(generated_texts):
        print(f"Text {i + 1}:")
        print(text)
        print()