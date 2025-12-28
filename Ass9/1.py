import streamlit as st
import os
import chromadb

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import init_embeddings

# ============================
# Streamlit Config
# ============================
st.set_page_config(page_title="AI Resume Shortlisting (RAG)", layout="wide")
st.title("📄 AI Enabled Resume Shortlisting System")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ============================
# Chroma DB
# ============================
db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection("resumes")

# ============================
# Embedding Model (LM Studio)
# ============================
embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

# ============================
# Backend Helper Functions
# ============================
def load_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    text = ""
    for p in pages:
        text += p.page_content + "\n"
    return text, len(pages)


def get_resume_ids():
    data = collection.get(include=["metadatas"])
    if not data["metadatas"]:
        return []
    return sorted(list(set(m["resume_id"] for m in data["metadatas"])))


def store_resume(resume_id, pdf_path):
    text, page_count = load_pdf(pdf_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.split_text(text)
    embeddings = embed_model.embed_documents(chunks)

    ids = [f"{resume_id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{
        "resume_id": resume_id,
        "chunk_id": i,
        "source": pdf_path
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


def shortlist_resumes(job_desc, top_n):
    query_embedding = embed_model.embed_query(job_desc)

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_n
    )

    shortlisted = []
    for meta in results["metadatas"][0]:
        shortlisted.append(meta["resume_id"])

    # remove duplicates, keep order
    return list(dict.fromkeys(shortlisted))


# ============================
# UI FUNCTIONS
# ============================
def upload_ui():
    st.header("📤 Upload Resume")

    resume_id = st.text_input("Resume ID")
    file = st.file_uploader("Upload PDF Resume", type=["pdf"])

    if st.button("Upload"):
        if resume_id and file:
            path = os.path.join(UPLOAD_DIR, file.name)
            with open(path, "wb") as f:
                f.write(file.read())

            store_resume(resume_id, path)
            st.success("✅ Resume uploaded and stored")
        else:
            st.warning("Please enter Resume ID and upload PDF")


def update_ui():
    st.header("🔄 Update Resume")

    ids = get_resume_ids()
    if not ids:
        st.info("No resumes available")
        return

    resume_id = st.selectbox("Select Resume ID", ids)
    file = st.file_uploader("Upload Updated PDF", type=["pdf"])

    if st.button("Update"):
        if file:
            path = os.path.join(UPLOAD_DIR, file.name)
            with open(path, "wb") as f:
                f.write(file.read())

            update_resume(resume_id, path)
            st.success("✅ Resume updated")


def list_view_ui():
    st.header("📋 Stored Resumes")

    ids = get_resume_ids()
    if not ids:
        st.info("No resumes found")
    else:
        for r in ids:
            st.write("•", r)

    st.caption(f"Total resumes: {len(ids)}")


def delete_ui():
    st.header("🗑️ Delete Resume")

    ids = get_resume_ids()
    if not ids:
        st.info("No resumes available")
        return

    resume_id = st.selectbox("Select Resume ID", ids)

    if st.button("Delete"):
        delete_resume(resume_id)
        st.success("✅ Resume deleted")


def shortlist_ui():
    st.header("⭐ Shortlist Resumes")

    job_desc = st.text_area("Enter Job Description")
    top_n = st.slider("Number of Resumes", 1, 10, 3)

    if st.button("Shortlist"):
        if not job_desc:
            st.warning("Please enter job description")
            return

        results = shortlist_resumes(job_desc, top_n)

        if not results:
            st.info("No matching resumes found")
        else:
            st.subheader("Shortlisted Resumes")
            for i, r in enumerate(results, 1):
                st.write(f"{i}. {r}")


# ============================
# SIDEBAR BUTTONS
# ============================
st.sidebar.title("📌 Functions")

if "mode" not in st.session_state:
    st.session_state.mode = "upload"

if st.sidebar.button("📤 Upload Resume"):
    st.session_state.mode = "upload"

if st.sidebar.button("🔄 Update Resume"):
    st.session_state.mode = "update"

if st.sidebar.button("📋 List View"):
    st.session_state.mode = "list"

if st.sidebar.button("🗑️ Delete Resume"):
    st.session_state.mode = "delete"

if st.sidebar.button("⭐ Shortlist"):
    st.session_state.mode = "shortlist"


# ============================
# MAIN CONTROLLER
# ============================
mode = st.session_state.mode

if mode == "upload":
    upload_ui()
elif mode == "update":
    update_ui()
elif mode == "list":
    list_view_ui()
elif mode == "delete":
    delete_ui()
elif mode == "shortlist":
    shortlist_ui()
