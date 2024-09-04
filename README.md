# GITA-GPT: A Retrieval-Augmented Generation (RAG) System 

GITA-GPT is a minimalistic proof-of-concept project that combines text retrieval and language generation using a Retrieval-Augmented Generation (RAG) approach. This application retrieves relevant verses from the Bhagavad Gita and generates a contextually informed response using a language model.

## Project Structure

Here's an overview of the project files:

- **README.md**: This file, providing an overview of the project.
- **gita.csv**: Contains the raw data of the Bhagavad Gita verses.
- **data_prep.py**: Script to preprocess the raw data and save it in a JSON format.
- **gita_data.json**: JSON file containing processed Bhagavad Gita verses and their translations.
- **embeddings.json**: JSON file containing embeddings for the Bhagavad Gita verses.
- **create_faiss_index.py**: Script to create a FAISS index for the verse embeddings to enable efficient retrieval.
- **gita_index.faiss**: FAISS index file used for verse retrieval.
- **generate_gita_embeddings.py**: Script to generate embeddings for the Bhagavad Gita verses using a Sentence Transformer model.
- **gpt2_inference.py**: Contains the function to generate text using the GPT-2 model. This file is a placeholder for actual LLM inference.
- **gita_retrieval_system.py**: Main script integrating retrieval and language model components (deprecated in favor of Streamlit app).
- **app.py**: Streamlit app file that provides the user interface for querying the system.
- **styles.css**: Contains CSS styles for the Streamlit app to make it look aesthetic.

## Installation

To set up the project environment and install dependencies, follow these steps:

1. **Create a Virtual Environment**:
   ```sh
   python3 -m venv gita-gpt-env
   ```

2. **Activate the Virtual Environment**:
   - On macOS/Linux:
     ```sh
     source gita-gpt-env/bin/activate
     ```
   - On Windows:
     ```sh
     gita-gpt-env\Scripts\activate
     ```

3. **Install Required Packages**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Download Pre-trained Models**:
   Ensure you have the required models downloaded, such as the Sentence Transformer and the GPT-2 model. Modify `generate_gita_embeddings.py` and `gpt2_inference.py` to load these models if they are not already present.

## Usage

1. **Generate Embeddings**:
   Run the script to generate embeddings for the Bhagavad Gita verses:
   ```sh
   python generate_gita_embeddings.py
   ```

2. **Create FAISS Index**:
   Build the FAISS index for efficient verse retrieval:
   ```sh
   python create_faiss_index.py
   ```

3. **Run the Streamlit App**:
   Launch the Streamlit app to interact with the system:
   ```sh
   streamlit run app.py
   ```

   This will open a web browser where you can input queries and receive responses based on the retrieved verses.

## Troubleshooting

- **Segmentation Fault**:
  - Ensure that all dependencies are properly installed.
  - Check for compatibility issues with the Python version or specific libraries.

- **Model Issues**:
  - Verify that the required models are correctly loaded and paths are set up properly in `gpt2_inference.py`.

## Contributing

Feel free to fork the repository and submit pull requests. For any issues or enhancements, please open an issue on the GitHub repository.
