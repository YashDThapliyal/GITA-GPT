# GITA-GPT: Exploring the Bhagavad Gita with RAG Architecture

## Overview

**GITA-GPT** is a project designed to answer questions based on the teachings of the Bhagavad Gita using advanced AI technologies. Leveraging the Retrieval-Augmented Generation (RAG) architecture, vector databases, and a local language model, this tool offers insights into the ancient text in a modern, interactive way.

## Project Components

1. **Data Preparation (`data_prep.py`)**
   - Converts the Bhagavad Gita CSV into a structured JSON format for easy processing.
   
2. **Embedding Generation (`generate_gita_embeddings.py`)**
   - Generates embeddings for the verses using the `SentenceTransformer` model and saves them in JSON format.
   
3. **FAISS Index Creation (`create_faiss_index.py`)**
   - Creates a FAISS index from the verse embeddings to enable fast similarity search.
   
4. **GPT-2 Inference (`gpt2_inference.py`)**
   - Contains functions for interacting with the GPT-2 model to generate text based on user queries.

5. **Retrieval System (`gita_retrieval_system.py`)**
   - Integrates the retrieval of relevant verses using the FAISS index with text generation via GPT-2, combining the outputs for comprehensive answers.

6. **Streamlit Application (`app.py`)**
   - Provides a user-friendly interface for querying the system and displaying results, including relevant verses from the Bhagavad Gita and responses from the language model.

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

## Getting Started

### Prerequisites

- Python 3.9+
- Required libraries: `faiss`, `numpy`, `sentence-transformers`, `transformers`, `streamlit`, and others.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

### Usage

1. Open the Streamlit app in your browser.
2. Enter a question related to the Bhagavad Gita.
3. Click 'Submit' to view relevant verses and AI-generated responses.

## Project Structure

```
.
├── README.md
├── gita.csv
├── data_prep.py
├── gita_data.json
├── embeddings.json
├── create_faiss_index.py
├── gita_index.faiss
├── generate_gita_embeddings.py
├── gpt2_inference.py
├── app.py
└── __pycache__/
```

## Future Enhancements

- Integrate with more advanced or specific language models.
- Improve the user interface and experience.
- Expand the dataset with more texts or additional features.
