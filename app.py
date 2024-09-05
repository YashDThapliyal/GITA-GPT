import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np
from groq import Groq
import xml.etree.ElementTree as ET

# Page configuration
st.set_page_config(
    page_title="Gita GPT Retrieval System",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Groq client
client = Groq(api_key="your_api_key_here")

# Load FAISS index and SentenceTransformer model
@st.cache_resource
def load_model_and_index():
    index = faiss.read_index('gita_index.faiss')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return index, model

index, model = load_model_and_index()

# Load Gita data
@st.cache_data
def load_data():
    with open('gita_data.json', 'r') as f:
        data = json.load(f)
    return data

gita_data = load_data()

def retrieve_verses(query, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    return indices[0], distances[0]

def get_verse_texts(indices):
    return [gita_data[i]['translation'] for i in indices]

def process_query_with_groq(context):
    prompt = f"""You are an AI assistant specializing in the Bhagavad Gita. 
    Given the following context and question, provide a thoughtful and insightful response:

    Context: {context}

    Please provide a concise yet comprehensive answer, drawing from the given verses only when appropriate. Keep in mind the verses are provided by the system autonomously based on what it thinks are relevant to the question based on cosine similarity, so sometimes they may not be correct. If that's the case, feel free to improvise and provide the correct answer. Don't acknowledge that the system made a mistake, just provide the correct answer."""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.1-8b-instant",
        temperature=0.5,
        max_tokens=4096,
        top_p=1,
        stream=False,
        stop=None
    )
    
    return chat_completion.choices[0].message.content

def get_related_questions(response, num_questions=3):
    # Few-shot examples
    few_shot_examples = """
    <examples>
        <example>
            <response>The Bhagavad Gita discusses the concept of dharma, which refers to one's duty or righteous living.</response>
            <questions>
                <question>What are some specific examples of dharma mentioned in the Bhagavad Gita?</question>
                <question>How does the concept of dharma relate to the caste system in ancient Indian society?</question>
                <question>Can you explain how the Bhagavad Gita balances the idea of duty with individual choice?</question>
            </questions>
        </example>
        <example>
            <response>Krishna teaches Arjuna about the nature of the soul and its relationship to the physical body.</response>
            <questions>
                <question>What specific analogies does Krishna use to explain the nature of the soul?</question>
                <question>How does the Bhagavad Gita's view of the soul compare to other philosophical or religious traditions?</question>
                <question>In what ways does understanding the nature of the soul impact one's actions, according to the Gita?</question>
            </questions>
        </example>
    </examples>
    """

    prompt = f"""Based on the following response about the Bhagavad Gita, suggest {num_questions} related questions. 
    Format your response in XML as shown in the examples below:

    {few_shot_examples}

    Now, generate questions for this response:
    <response>{response}</response>
    """

    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=4096,
    )

    # Parse the XML response
    xml_response = f"<root>{completion.choices[0].message.content}</root>"
    root = ET.fromstring(xml_response)

    # Extract questions from the XML
    questions = [q.text for q in root.findall('.//question')]

    return questions

# Sidebar
with st.sidebar:
    st.header("About Gita GPT")
    st.write("""
    Gita GPT is an AI-powered system that helps you explore the wisdom of the Bhagavad Gita. 
    It uses advanced natural language processing to find relevant verses and generate insightful responses to your questions.
    """)

# Main content
st.title("🕉️ Gita GPT Retrieval System")

st.markdown("Ask a question about the Bhagavad Gita and get relevant verses and insights.")

query = st.text_input('Enter your question:', placeholder="e.g., What does the Gita say about duty?", key="query_input")
num_verses = st.slider("Number of verses to retrieve", min_value=1, max_value=10, value=5)

# Function to process the query
def process_query():
    if query:
        with st.spinner("Searching for relevant verses..."):
            relevant_indices, distances = retrieve_verses(query, num_verses)
            relevant_verses = get_verse_texts(relevant_indices)

        with st.spinner("Generating insight..."):
            context = "\n".join(relevant_verses) + f"\n\nQuestion: {query}"
            response = process_query_with_groq(context)   

        st.subheader("Gita GPT's Insight:")
        st.success(response)

        if st.button("Copy insight"):
            st.write("Insight copied to clipboard!")  


        st.subheader("Relevant Verses:")
        for i, verse in enumerate(relevant_verses, 1):
            with st.expander(f"Verse {i}"):
                st.write(verse)
                if st.button(f"Copy verse {i}", key=f"copy_verse_{i}"):
                    st.write(f"Copied: {verse}")
        
        st.subheader("Related Questions:")
        related_questions = get_related_questions(response)
        for q in related_questions:
            if st.button(q, key=f"related_{q}"):
                st.session_state.query = q
                st.experimental_rerun()
    else:
        st.error("Please enter a question before submitting.")

# Check if Enter key is pressed
if query and len(query) > 0 and query[-1] == '\n':
    process_query()
    st.session_state.query = query.rstrip()  # Remove the newline character
    st.experimental_rerun()

# Submit button
if st.button('Submit', type='primary'):
    process_query()

# Clear button
if st.button("Clear"):
    st.session_state.query = ""
    st.experimental_rerun()