import faiss
import pickle
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Load embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAISS index and chunks
index = faiss.read_index("ugc_index.faiss")
with open("ugc_chunks.pkl", "rb") as f:
    chunks = pickle.load(f)



qa_model = pipeline(
    "text-generation",
    model="tiiuae/falcon-7b-instruct",
  # CPU fallback
)


def ask_ugc_bot(question, k=5):
    question_embedding = embedder.encode([question])
    distances, indices = index.search(question_embedding, k)

    # Combine relevant chunks
    context = "\n\n".join([chunks[i] for i in indices[0]])

    prompt = f"""
You are a helpful assistant for students seeking university admission in Sri Lanka.
Answer the question clearly using only the following UGC Handbook context:

Context:
{context}

Question:
{question}
"""

    result = qa_model(prompt, max_new_tokens=200)[0]["generated_text"]
    return result.strip()
