import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from groq import Groq

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DIR = os.path.join(BASE_DIR, "data", "processed", "chroma_db")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
    return vectorstore

def ask(question):
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(question, k=3)
    
    context = "\n\n".join([doc.page_content for doc in results])
    sources = list(set([doc.metadata.get("source", "unknown") for doc in results]))

    prompt = f"""You are a tax regulation assistant for a CA firm in India.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I could not find this in the loaded notifications."
Do not make up any information.

Context:
{context}

Question: {question}
Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    print(f"\nQuestion: {question}")
    print(f"\nAnswer: {answer}")
    print(f"\nSources: {sources}")

if __name__ == "__main__":
    while True:
        question = input("\nAsk a question (or type 'exit'): ")
        if question.lower() == "exit":
            break
        ask(question)