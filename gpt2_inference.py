from transformers import GPTNeoForCausalLM, GPT2Tokenizer

# Load pre-trained model and tokenizer
model_name = "EleutherAI/gpt-neo-1.3B"  # You can also use "EleutherAI/gpt-neo-2.7B" for a larger model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPTNeoForCausalLM.from_pretrained(model_name)

# Generate text
def generate_text(prompt, max_length=150, num_return_sequences=1):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs["input_ids"], 
        max_length=max_length, 
        num_return_sequences=num_return_sequences,
        no_repeat_ngram_size=2,  # Avoid repetition
        early_stopping=True
    )
    return [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

if __name__ == "__main__":
    prompt = "What is the duty of a warrior?"  # Replace with your query
    generated_texts = generate_text(prompt)
    
    print("Generated Texts:")
    for i, text in enumerate(generated_texts):
        print(f"Text {i + 1}:")
        print(text)
        print()
