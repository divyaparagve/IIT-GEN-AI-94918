import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings

db = chromadb.PersistentClient(path="./knowledge_base")
collection = db.get_or_create_collection("resumes")

embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    resume_content = ""
    for page in docs:
        resume_content += page.page_content + "\n"
    metadata = {
        "source": pdf_path,
        "page_count": len(docs)
    }
    return resume_content, metadata


resume_path = r"C:\Users\dparg\Downloads\fake-resumes\resume-017.pdf"
resume_text, resume_info = load_pdf_resume(resume_path)

# Generate embedding
resume_embeddings = embed_model.embed_documents([resume_text])
print(f"Len = {len(resume_embeddings[0])} --> {resume_embeddings[0][:4]}")

# ✅ STORE
collection.add(
    documents=[resume_text],
    embeddings=resume_embeddings,
    metadatas=[{
        "resume_id": "resume_017",
        "source": resume_path,
        "page_count": resume_info["page_count"]
    }],
    ids=["resume_017"]
)

print("✅ Resume stored in Chroma")

# ✅ FETCH
results = collection.get(
    ids=["resume_017"],
    include=["documents", "metadatas", "embeddings"]
)

print("Metadata:", results["metadatas"])
print("Document length:", len(results["documents"][0]))
print("Embedding length:", len(results["embeddings"][0]))
print("Document preview:\n", results["documents"][0][:300])
