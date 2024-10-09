# GITA-GPT 🕉️
**AI-powered system for exploring the teachings of the Bhagavad Gita**

GITA-GPT is an advanced AI-based question-answering system designed to provide insights and relevant verses from the Bhagavad Gita. Using cutting-edge technologies like *Retrieval-Augmented Generation (RAG) architecture*, *Meta's LLAMA LLM*, *FAISS vector search*, and the *GROQ API*, this tool makes it easier to explore the wisdom of this ancient text in a modern and interactive way.

## Features
- **Question-Answering System**: Submit any question related to the Bhagavad Gita and receive thoughtful and contextually relevant answers.
- **Real-time Inference**: Powered by *Meta's LLAMA LLM* via the *GROQ API* for generating concise and insightful responses.
- **Verse Retrieval**: Retrieves relevant verses based on cosine similarity using *FAISS* for fast and efficient vector search.
- **Contextual Responses**: Incorporates retrieved verses into the response to provide a holistic understanding of the Bhagavad Gita.
- **Related Questions Generation**: Automatically generates additional questions based on the response to enhance exploration of the topic.
- **User Interaction**: Features an interactive UI where users can ask questions, copy responses, and explore related verses.
- **Efficient Query Processing**: Leveraging *SentenceTransformers* to encode queries and generate relevant embeddings for the search.

## Technologies Used
- **Streamlit**: Provides a user-friendly web interface for submitting queries and exploring responses.
- **Sentence Transformers**: Used for encoding input queries and verses for vector-based search.
- **FAISS (Facebook AI Similarity Search)**: Powers the vector-based search for retrieving relevant verses from the Bhagavad Gita.
- **Meta's LLAMA LLM**: Handles real-time inference, providing insightful and context-aware answers to user queries.
- **GROQ API**: Used to interact with the LLAMA model for generating natural language responses.
- **TensorFlow**: Integrated into some components for machine learning processes.
- **XML Parsing**: For generating related questions and improving user interaction.

## How It Works
1. **Input Query**: Enter a question about the Bhagavad Gita into the text input field (e.g., "What does the Gita say about duty?").
2. **Verse Retrieval**: The query is encoded using *SentenceTransformers*, and the FAISS index is searched for the top *k* relevant verses.
3. **Inference**: The retrieved verses, along with the query, are passed to *Meta's LLAMA LLM* for generating an insightful response.
4. **Response Display**: The system displays both the generated answer and the retrieved verses, allowing for deeper exploration.
5. **Related Questions**: Based on the generated answer, the system suggests additional related questions to help guide further inquiry.

## Installation
To run GITA-GPT locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/gita-gpt.git
    cd gita-gpt
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up the FAISS Index and Gita Data**:
    - Ensure you have `gita_index.faiss` and `gita_data.json` files in the root directory.

4. **Set your GROQ API Key**:
    - Insert your GROQ API key in the `client` initialization:
      ```python
      client = Groq(api_key="your-groq-api-key")
      ```

5. **Run the application**:
    ```bash
    streamlit run app.py
    ```

6. **Open the web interface**:
    - The app should open in your browser at `http://localhost:8501`.

## Usage
- **Submit a Query**: Enter a question in the input field and click “Submit” to get relevant verses and AI-generated insights.
- **Explore Verses**: Click on each verse to expand and read the full text.
- **Copy Insights/Verses**: Use the provided buttons to copy any insights or verses to your clipboard.
- **Related Questions**: Click on any of the suggested related questions to dive deeper into the Bhagavad Gita's teachings.

## Example Queries
- *What does the Gita say about duty?*
- *How does the Gita define the concept of the soul?*
- *What lessons does the Gita provide on leadership?*

## Contributing
We welcome contributions to improve GITA-GPT. If you’d like to contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a Pull Request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
