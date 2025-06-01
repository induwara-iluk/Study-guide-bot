from sentence_transformers import SentenceTransformer
import faiss
import pickle
# Optionally paste this function from your previous script
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        
        full_text += page.get_text()

    # Split the text into chunks (~1000 characters)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    return splitter.split_text(full_text)

# Call it here to get chunks
chunks = extract_text_chunks("HANDBOOK_ENGLISH.pdf")

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed all text chunks
embeddings = model.encode(chunks, show_progress_bar=True)

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index and chunks
faiss.write_index(index, "ugc_index.faiss")
with open("ugc_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("✅ FAISS index and chunks saved!")

