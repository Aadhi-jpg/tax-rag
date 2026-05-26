import os
import sys
import io
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import streamlit as st
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq
import PyPDF2

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="CA Tax Assistant", page_icon="📋")
st.title("CA Tax Notification Assistant")
st.caption("Ask questions about loaded tax notifications. Answers are sourced strictly from uploaded documents.")

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_vectorstore():
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    return st.session_state.vectorstore

if st.session_state.get("vectorstore") is None:
        st.session_state.vectorstore = FAISS.from_texts(
            texts=chunks,
            embedding=embeddings,
            metadatas=metadata
        )
    else:
        new_vs = FAISS.from_texts(
            texts=chunks,
            embedding=embeddings,
            metadatas=metadata
        )
        st.session_state.vectorstore.merge_from(new_vs)
def ask(question):
    vectorstore = get_vectorstore()

    if vectorstore is None:
        return "No notifications loaded yet. Please upload a PDF first.", []

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

    return response.choices[0].message.content, sources

with st.sidebar:
    st.header("Upload Notifications")
    uploaded_file = st.file_uploader("Upload a PDF notification", type="pdf")
    if uploaded_file:
        with st.spinner("Ingesting PDF..."):
            success, message = ingest_pdf(uploaded_file)
        if success:
            st.success(message)
        else:
            st.error(message)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask about a tax notification..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching notifications..."):
            answer, sources = ask(question)
        st.markdown(answer)
        if sources:
            st.caption(f"Sources: {', '.join(sources)}")

    st.session_state.messages.append({"role": "assistant", "content": answer})