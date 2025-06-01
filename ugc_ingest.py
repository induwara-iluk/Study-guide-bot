import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_chunks(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page in doc:
        full_text += page.get_text()

    # Split the text into chunks (~500 tokens)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = splitter.split_text(full_text)
    return chunks

# Test it
chunks = extract_text_chunks("HANDBOOK_ENGLISH.pdf")
print(f"Extracted {len(chunks)} chunks.")
print(chunks[:3])  # Preview
