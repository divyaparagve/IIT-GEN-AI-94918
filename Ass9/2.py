import streamlit as st
import os
import chromadb

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import init_embeddings
from langchain.chat_models import init_chat_model

# =============================
# STREAMLIT CONFIG
# =============================
st.set_page_config(page_title="AI Resume Shortlisting (RAG)", layout="wide")
st.title("📄 AI Resume Shortlisting System using RAG")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# =============================
# CHROMA VECTOR DATABASE
# =============================
db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection("resumes")

# =============================
# EMBEDDING MODEL (LM STUDIO)
# =============================
embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

# =============================
# LLM (FOR RAG GENERATION)
# =============================
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# =============================
# HELPER FUNCTIONS
# =============================
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    text = ""
    for p in pages:
        text += p.page_content + "\n"
    return text


def get_resume_ids():
    data = collection.get(include=["metadatas"])
    if not data["metadatas"]:
        return []
    return sorted(set(m["resume_id"] for m in data["metadatas"]))


def store_resume(resume_id, pdf_path):
    text = load_pdf(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)
    embeddings = embed_model.embed_documents(chunks)

    ids = [f"{resume_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{
        "resume_id": resume_id,
        "source": pdf_path,
        "chunk_id": i
    } for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def delete_resume(resume_id):
    collection.delete(where={"resume_id": resume_id})


def update_resume(resume_id, pdf_path):
    delete_resume(resume_id)
    store_resume(resume_id, pdf_path)


# =============================
# RAG SHORTLIST FUNCTION
# =============================
def rag_shortlist(job_desc, top_n):
    # 1️⃣ Embed job description
    query_embedding = embed_model.embed_query(job_desc)

    # 2️⃣ Retrieve relevant resume chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_n * 3,
        include=["documents", "metadatas"]
    )

    resume_context = {}
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        rid = meta["resume_id"]
        resume_context.setdefault(rid, "")
        resume_context[rid] += doc + "\n"

    # 3️⃣ Build RAG prompt
    context_text = ""
    for rid, text in resume_context.items():
        context_text += f"\nResume ID: {rid}\n{text[:1500]}\n"

    prompt = f"""
You are an AI HR assistant.

Job Description:
{job_desc}

Below are resume excerpts retrieved from the database:
{context_text}

Task:
1. Rank resumes from best to worst
2. Give short reason for each resume

Return result in numbered list format.
"""

    # 4️⃣ LLM generates ranked output
    response = llm.invoke(prompt)
    return response.content


# =============================
# SIDEBAR BUTTONS
# =============================
st.sidebar.title("📌 Functions")

if "mode" not in st.session_state:
    st.session_state.mode = "upload"

if st.sidebar.button("📤 Upload Resume"):
    st.session_state.mode = "upload"

if st.sidebar.button("🔄 Update Resume"):
    st.session_state.mode = "update"

if st.sidebar.button("📋 List Resumes"):
    st.session_state.mode = "list"

if st.sidebar.button("🗑️ Delete Resume"):
    st.session_state.mode = "delete"

if st.sidebar.button("⭐ Shortlist (RAG)"):
    st.session_state.mode = "shortlist"


# =============================
# UI SCREENS
# =============================
mode = st.session_state.mode

# ---- UPLOAD ----
if mode == "upload":
    st.header("📤 Upload Resume")

    resume_id = st.text_input("Resume ID")
    file = st.file_uploader("Upload PDF", type=["pdf"])

    if st.button("Upload"):
        if resume_id and file:
            path = os.path.join(UPLOAD_DIR, file.name)
            with open(path, "wb") as f:
                f.write(file.read())
            store_resume(resume_id, path)
            st.success("✅ Resume uploaded & stored")
        else:
            st.warning("Provide Resume ID and PDF")

# ---- UPDATE ----
elif mode == "update":
    st.header("🔄 Update Resume")

    ids = get_resume_ids()
    resume_id = st.selectbox("Select Resume", ids)
    file = st.file_uploader("Upload New PDF", type=["pdf"])

    if st.button("Update"):
        if file:
            path = os.path.join(UPLOAD_DIR, file.name)
            with open(path, "wb") as f:
                f.write(file.read())
            update_resume(resume_id, path)
            st.success("✅ Resume updated")

# ---- LIST ----
elif mode == "list":
    st.header("📋 Stored Resumes")

    ids = get_resume_ids()
    for r in ids:
        st.write("•", r)
    st.caption(f"Total resumes: {len(ids)}")

# ---- DELETE ----
elif mode == "delete":
    st.header("🗑️ Delete Resume")

    resume_id = st.selectbox("Select Resume", get_resume_ids())
    if st.button("Delete"):
        delete_resume(resume_id)
        st.success("✅ Resume deleted")

# ---- SHORTLIST (RAG) ----
elif mode == "shortlist":
    st.header("⭐ RAG-based Resume Shortlisting")

    job_desc = st.text_area("Enter Job Description")
    top_n = st.slider("Number of resumes", 1, 5, 3)

    if st.button("Run Shortlisting"):
        if not job_desc.strip():
            st.warning("Enter job description")
        else:
            with st.spinner("Retrieving & ranking resumes..."):
                result = rag_shortlist(job_desc, top_n)

            st.subheader("📌 Ranked Resumes")
            st.markdown(result)
