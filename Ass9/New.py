import streamlit as st
import os
import chromadb
import tempfile
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
import time
import pandas as pd



st.title("Resume Management System")
#create chromadb instance
db= chromadb.PersistentClient(path="./shortlist_application_base")

 #create embedding model       
    
embed_model = init_embeddings(
model = "text-embedding-nomic-embed-text-v1.5",
provider="openai",
base_url="http://10.45.159.95:1234/v1",
api_key = "not-needed",
check_embedding_ctx_length = False

)  


if 'page' not in st.session_state:
    st.session_state.page="Home"
    
if 'collection'  not in st.session_state:
    st.session_state.collection=db.get_or_create_collection("ai_resume_shortlist_db")
      
    

# creatng a functions for buttons

def Home():
    st.header("Home")
    st.write("Welcome!! resume managing and shortlisting of resumes")  
    
def Upload():
    st.header("Upload Resume")
    upload_resume = st.file_uploader("Upload File(PDF)",type=["pdf"]) 
    
     
#We create a temporary file because Streamlit does not give a real file path when a user uploads a file
    
    if upload_resume is not None:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(upload_resume.read())
            temp_pdf_path = temp_file.name
    
        # Load the PDF
        loader = PyPDFLoader(temp_pdf_path) 
        docs = loader.load()
        resume_content = ""
        for page in docs:
            resume_content += page.page_content 
            
        metadata = {
            "source": temp_pdf_path,
            "page_count": len(docs),
            "file_name": upload_resume.name,
            "date_time": str(datetime.now())
        }  
        # Generate embedding vector for the resume content

        resume_embeddings = embed_model.embed_documents([resume_content])
        time.sleep(3)
        if st.session_state.collection is not None:
           st.session_state.collection.add(
                ids=[upload_resume.name],
                documents=[resume_content],
                embeddings=resume_embeddings,
                metadatas =[metadata]
        )
           
def Update():
    st.header("Update Resume")
    input= st.chat_input("Enter resume id to Update the resume")
    st.session_state.collection.delete(ids=[input])
    
def Delete():
    st.header("Delete Resume")
    resume_id= st.chat_input("Enter resume id to Delete the resume")
    if resume_id:
        result=st.session_state.collection.get(ids=[resume_id])
        if result["ids"]:
            st.session_state.collection.delete(ids=[resume_id])
            st.success("Resume Deleted Successfully")
        else:
            st.error("Resume ID not found")
            
def List():
    st.header("List of Existing Resumes:")
    count = st.session_state.collection.count()
    st.write("Total Records:",count)
    results = st.session_state.collection.get(
        limit = count,
        include = ["metadatas"] 
    )
    df = pd.DataFrame(columns=["File Name", "Upload Date-Time"])
def Shortlist():
    pass          

#create sidebar menu and adding a buttons

with st.sidebar:
    if st.button("Home",width="stretch"):
        st.session_state.page = "Home"
        st.rerun()
    if st.button("Upload",width="stretch"):
        st.session_state.page = "Upload"
        st.rerun()
    if st.button("Update",width="stretch"):
        st.session_state.page = "Update"
        st.rerun()
    if st.button("Delete",width="stretch"):
        st.session_state.page = "Delete"
        st.rerun()
    if st.button("List",width="stretch"):
        st.session_state.page = "List" 
        st.rerun()               
    if st.button("Shortlist",width="stretch"):
        st.session_state.page = "Shortlist"  
        st.rerun() 
        

           
if st.session_state.page=="Upload":
    Upload()    
if st.session_state.page=="Home":
    Home()  
if st.session_state.page=="Update":
    Update()  
if st.session_state.page=="Delete":
    Delete()
if st.session_state.page=="List":
    List()
if st.session_state.page=="Shortlist":
    Shortlist()                  

                