import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from ingestion import process_all_pdfs

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(BASE_DIR, "data", "processed", "chroma_db")

def chunk_and_embed():
    documents = process_all_pdfs()

    if not documents:
        return None

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    all_chunks = []
    all_metadata = []

    for doc in documents:
        chunks = splitter.split_text(doc["text"])
        all_chunks.extend(chunks)
        all_metadata.extend([{"source": doc["filename"]}] * len(chunks))
        print(f"  {doc['filename']} - {len(chunks)} chunks")

    print(f"\nTotal chunks: {len(all_chunks)}")
    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    print("Embedding and storing in ChromaDB...")
    vectorstore = Chroma.from_texts(
        texts=all_chunks,
        embedding=embeddings,
        metadatas=all_metadata,
        persist_directory=CHROMA_DIR
    )

    print("Done. Vector store ready.")
    return vectorstore

if __name__ == "__main__":
    chunk_and_embed()