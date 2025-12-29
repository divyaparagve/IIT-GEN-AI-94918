import streamlit as st



st.set_page_config(
    page_title="AI Resume Shortlisting System",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
import chromadb
import tempfile
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
import time
import pandas as pd


st.markdown("""
<div class="card">
<h1>📄 AI Resume Shortlisting System</h1>
<p style="text-align:center; color:gray;">
Upload resumes, match with job descriptions, and shortlist candidates using RAG
</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("🔍 Navigation")

st.markdown("""
<style>
/* Main background */
.main {
    background-color: #f8f9fa;
}

/* Title */
h1 {
    color: #0d6efd;
    text-align: center;
}

/* Card style */
.card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Buttons */
.stButton>button {
    border-radius: 10px;
    background-color: #0d6efd;
    color: white;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #084298;
}

/* Sidebar */
.css-1d391kg {
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)


#create chromadb instance
db= chromadb.PersistentClient(path="./shortlist_application_base")

 #create embedding model       
    
embed_model = init_embeddings(
model = "text-embedding-nomic-embed-text-v1.5",
provider="openai",
base_url="http://192.168.0.109:1234/v1",
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
        st.success(f"{upload_resume.name} uploaded successfully")
def Update():
    st.header("Update Resume")

    # initialize state
    if "ready_for_upload" not in st.session_state:
        st.session_state.ready_for_upload = False

    resume_name = st.text_input(
        "Enter resume file name to update (example: resume-019.pdf)"
    )

    if not resume_name:
        return

    results = st.session_state.collection.get(include=["metadatas"])

    existing_ids = []
    for i in range(len(results["ids"])):
        if results["metadatas"][i]["file_name"] == resume_name:
            existing_ids.append(results["ids"][i])

    # STEP 1: Check existence (only before delete)
    if not existing_ids and not st.session_state.ready_for_upload:
        st.error("File does not exist in database")
        return

    # STEP 2: Resume exists → delete option
    if not st.session_state.ready_for_upload:
        st.success("Resume found")

        if st.button("Delete Old Resume"):
            st.session_state.collection.delete(ids=existing_ids)
            st.session_state.ready_for_upload = True
            st.success("Old resume deleted. Please upload updated resume.")
            st.rerun()

    # STEP 3: Upload new resume after delete
    if st.session_state.ready_for_upload:
        updated_resume = st.file_uploader(
            "Upload updated resume (PDF)",
            type=["pdf"]
        )

        if updated_resume is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(updated_resume.read())
                temp_pdf_path = temp_file.name

            loader = PyPDFLoader(temp_pdf_path)
            docs = loader.load()

            resume_content = ""
            for page in docs:
                resume_content += page.page_content

            metadata = {
                "source": temp_pdf_path,
                "page_count": len(docs),
                "file_name": updated_resume.name,
                "date_time": str(datetime.now())
            }

            resume_embeddings = embed_model.embed_documents([resume_content])

            st.session_state.collection.add(
                ids=[updated_resume.name],
                documents=[resume_content],
                embeddings=resume_embeddings,
                metadatas=[metadata]
            )

            st.success(f"{updated_resume.name} updated successfully")

            # reset state
            st.session_state.ready_for_upload = False




    
def Delete():
    st.header("Delete Resume")
     # Show existing resumes
    st.subheader("Existing Resumes")
    count = st.session_state.collection.count()
    

    if count == 0:
        st.info("No resumes available")
        return

    results = st.session_state.collection.get(
        limit=count,
        include=["metadatas"]
    )

    df = pd.DataFrame(columns=["Resume ID", "File Name", "Upload Date-Time"])

    for i in range(len(results["ids"])):
        df.loc[len(df)] = [
            results["ids"][i],
            results["metadatas"][i]["file_name"],
            results["metadatas"][i]["date_time"]
        ]

    st.dataframe(df, use_container_width=True)

    # Delete input
    resume_id = st.text_input("Enter Resume ID to delete")

    if st.button("Delete Resume"):
        if not resume_id:
            st.warning("Please enter Resume ID")
        else:
            try:
                st.session_state.collection.delete(ids=[resume_id])
                st.success(f"{resume_id} deleted successfully")
              
            except Exception as e:
                st.error(f"Error: {e}")
     
             
            
def List():
    
    st.header("List of Existing Resumes:")
    
    count = st.session_state.collection.count()
    st.write("Total Records:", count)

    if count == 0:
        st.info("No resumes uploaded yet")
        return

    results = st.session_state.collection.get(
        limit=count,
        include=["metadatas"]
    )

    df = pd.DataFrame(columns=["Resume ID", "File Name", "Upload Date-Time"])

    for i in range(len(results["ids"])):
        resume_id = results["ids"][i]
        file_name = results["metadatas"][i]["file_name"]
        date_time = results["metadatas"][i]["date_time"]

        df.loc[len(df)] = [resume_id, file_name, date_time]

    st.dataframe(df, use_container_width=True)

def Shortlist():
    
   
    st.header("Shortlist Resumes")

    job_description = st.text_area(
        "Enter Job Description",
        placeholder="Example: Python developer with ML and NLP experience"
    )

    top_k = st.number_input(
        "Number of resumes to shortlist",
        min_value=1,
        max_value=10,
        value=3
    )

    MATCH_THRESHOLD = 0.30   # adjust if needed

    if st.button("Shortlist"):
        if not job_description:
            st.warning("Please enter job description")
            return

        #  Embed job description
        jd_embedding = embed_model.embed_documents([job_description])

        #  Query ChromaDB
        results = st.session_state.collection.query(
            query_embeddings=jd_embedding,
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )

        if not results["ids"] or len(results["ids"][0]) == 0:
            st.info("No resumes matched the job description")
            return

        found_match = False
        st.subheader("Shortlisted Resumes")

        for i in range(len(results["ids"][0])):
            score = 1 - results["distances"][0][i]

            # Skip weak matches
            if score < MATCH_THRESHOLD:
                continue

            found_match = True
            file_name = results["metadatas"][0][i]["file_name"]
            resume_text = results["documents"][0][i]

            #  CLEAN SHORT PARAGRAPH 
            sentences = resume_text.replace("\n", " ").split(".")
            clean_lines = []

            for s in sentences:
                s_lower = s.lower()
                if (
                    "@" in s or
                    "email" in s_lower or
                    "phone" in s_lower or
                    "contact" in s_lower or
                    any(char.isdigit() for char in s)
                ):
                    continue

                clean_lines.append(s.strip())
                if len(clean_lines) == 4:
                    break

            short_para = ". ".join(clean_lines) + "."

            st.markdown(f"### {file_name}")
            st.write(short_para)
            st.write(f"**Match Score:** {round(score, 2)}")
            st.markdown("---")

        #  If nothing crossed threshold
        if not found_match:
            st.info("No resumes matched the job description")


    


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

                