import streamlit as st
from langchain.embeddings import init_embeddings
import chromadb
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import time
from datetime import datetime

st.title("AI Enabled Resume Shortlisting Application",text_alignment="center")

# Chromadb
db = chromadb.PersistentClient(path="./shortlist_application_base")
# st.session_state.collection = db.get_or_create_collection("ai_resume_shortlist_db")

# Initialization 
if 'page' not in st.session_state:
    st.session_state.page = "home"

if 'collection' not in st.session_state:
    st.session_state.collection = db.get_or_create_collection("ai_resume_shortlist_db")


with st.sidebar:
    st.header("Menu")
    if st.button("Home", width="stretch"):
        st.session_state.page = "home"
        st.rerun()
    if st.button("Upload New Resume", width="stretch"):
        st.session_state.page = "upload"
        st.rerun()
    if st.button("List Existing Resumes", width="stretch"):
        st.session_state.page = "list_resumes"
        st.rerun()
    if st.button("Update Existing Resume", width="stretch"):
        st.session_state.page = "update"
        st.rerun()
    if st.button("Shortlist Resumes", width="stretch"):
        st.session_state.page = "shortlist"
        st.rerun()
    if st.button("Delete Resumes", width="stretch"):
        st.session_state.page = "delete"
        st.rerun() 

# Create a En=mbedding model
embed_model = init_embeddings(
    model="text-embedding-all-minilm-l6-v2-embedding",
    provider="openai",
    base_url = "http://127.0.0.1:1234/v1",
    api_key= "not-needed",
    check_embedding_ctx_length=False
)

# Pages
def home():
    st.header("Home")
    st.write("Welcome!! Our application is helpful for managing and shortlisting of resumes")


def upload():
    st.header("Upload New Resume")
    uploaded_file = st.file_uploader("Upload file (PDF)", type=["pdf"])

    if uploaded_file is not None:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_pdf_path = temp_file.name

        # Load the PDF
        #PyPDFLoader is designed to extract text from PDF files.
        loader = PyPDFLoader(temp_pdf_path)
        # st.write(loader)
        docs = loader.load()
        # st.write(type(docs))
        # st.write(docs[0])
        resume_content = ""
        for page in docs:
            resume_content += page.page_content

        metadata = {
            "file_name": uploaded_file.name,
            "page_count": len(docs),
            "date_time": str(datetime.now())
        }

        # Create embed vectors    
        resume_embeddings = embed_model.embed_documents([resume_content])
        time.sleep(3)
        if st.session_state.collection is not None: 
            st.session_state.collection.add(ids=[uploaded_file.name], embeddings=resume_embeddings, documents=[resume_content], metadatas=[metadata])

            # Display Details
            st.subheader("Resume Details:")
            results = st.session_state.collection.get(
            ids=[uploaded_file.name],
            include = ["metadatas", "documents"] 
            )
            st.write("Metadata:", results["metadatas"][0])
            st.write("Document:", results["documents"][0])
                 

def update():
    st.header("Update")
    input = st.chat_input("Enter resume id to Update the resume")
    st.session_state.collection.delete(ids=[input])

def list_resumes():
    st.header("List of Existing Resumes:")
    count = st.session_state.collection.count()
    # st.write("Total Records:",count)
    results = st.session_state.collection.get(
        limit = count,
        include = ["metadatas"] 
    )
    df = pd.DataFrame(columns=["File Name", "Upload Date-Time"])

    # st.write(results)
    for i in range(len(results["ids"])):
        file_name = results["metadatas"][i]["file_name"]
        date_time = results["metadatas"][i]["date_time"]
        df.loc[len(df)] = [file_name, date_time]

    st.dataframe(df)
        

def shortlist():
    pass

def delete():
    st.header("Delete Resume")

    # Display existiong resume list
    st.subheader("Existing Resumes", text_alignment="center")
    count = st.session_state.collection.count()
    # st.write("Total Records:",count)
    results = st.session_state.collection.get(
        limit = count,
        include = ["metadatas"] 
    )
    df = pd.DataFrame(columns=["File Name", "Upload Date-Time"])

    # st.write(results)
    for i in range(len(results["ids"])):
        file_name = results["metadatas"][i]["file_name"]
        date_time = results["metadatas"][i]["date_time"]
        df.loc[len(df)] = [file_name, date_time]

    st.dataframe(df)

    # Delete the resume using id
    id = st.chat_input("Enter resume id to delete resume")
    try:
        if id:
            with st.chat_message("user"):
                st.write(f"Delete : {id}")
            data = id + ".pdf"
            st.session_state.collection.delete(ids=[data])
            st.success(f"{id} successfully deleted")

            # After delete
            results = st.session_state.collection.get(
                limit = count,
                include = ["metadatas"] 
            )
            dl = pd.DataFrame(columns=["File Name", "Upload Date-Time"])
            st.subheader("After delete:")
            for i in range(len(results["ids"])):
                file_name = results["metadatas"][i]["file_name"]
                date_time = results["metadatas"][i]["date_time"]
                dl.loc[len(dl)] = [file_name, date_time]

            st.dataframe(dl)
    except:
        st.error("Some error occurred!!")

    
if st.session_state.page == "home":
    home()
elif st.session_state.page == "upload":
    upload()
elif st.session_state.page == "update":
    update()
elif st.session_state.page == "list_resumes":
    list_resumes()
elif st.session_state.page == "shortlist":
    shortlist()
elif st.session_state.page == "delete":
    delete()




