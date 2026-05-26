import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(BASE_DIR, "data", "processed", "chroma_db")

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    return vectorstore

def query_documents(question, k=3):
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(question, k=k)
    print(f"\nQuestion: {question}")
    print("-" * 50)
    for i, doc in enumerate(results):
        print(f"\nChunk {i+1} (source: {doc.metadata.get('source', 'unknown')}):")
        print(doc.page_content)

if __name__ == "__main__":
    query_documents("What is this notification about?")