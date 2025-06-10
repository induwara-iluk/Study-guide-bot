import google.generativeai as genai
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from transformers import pipeline
embedder = SentenceTransformer('all-MiniLM-L6-v2')
# Load FAISS index and chunks
index = faiss.read_index("ugc_index.faiss")
with open("ugc_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

# Initialize Google Generative AI

genai.configure(api_key="AIzaSyAhx7IRQ1DsgAM87rDAC17e9MajXsUurdA")  # Use `getpass` or env var for safety
model = genai.GenerativeModel("models/gemini-1.5-flash")
chat = model.start_chat(history=[])


def ask_ugc_bot(question, k=20):
    question_embedding = embedder.encode([question])
    distances, indices = index.search(question_embedding, k)

    # Combine relevant chunks
    context = "\n\n".join([chunks[i] for i in indices[0]])

    # Build prompt
    prompt = f"""
You are a helpful assistant for students seeking university admission in Sri Lanka.
Use the following context from the UGC Handbook to answer clearly and concisely.

Context:
{context}

Question:
{question}
"""

    # Send prompt to Gemini
    response = chat.send_message(prompt)
    return response.text.strip()

chat.send_message("""
You are a helpful and precise assistant for university admission questions in Sri Lanka.
You must only answer using context from the UGC Handbook provided.
Avoid guessing or adding extra knowledge. If unsure, say so.
""")