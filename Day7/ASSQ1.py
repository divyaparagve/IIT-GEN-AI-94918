import streamlit as st
import pandas as pd
from pandasql import sqldf
import requests
from bs4 import BeautifulSoup
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

# -------------------- SETUP --------------------
load_dotenv()
st.set_page_config(page_title="Intelligent CSV + Web Agent", layout="wide")
st.title("🤖 Intelligent CSV & Web Question Answering Agent")

# -------------------- CHAT HISTORY --------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- CSV UPLOAD --------------------
st.sidebar.header("Upload CSV File")
file = st.sidebar.file_uploader("Upload CSV", type="csv")

df = None
if file:
    df = pd.read_csv(file)
    st.sidebar.success("CSV Uploaded Successfully")
    st.sidebar.write("### CSV Schema")
    st.sidebar.write(df.dtypes)

# -------------------- TOOLS --------------------
@tool
def csv_qa_tool(query: str) -> str:
    """
    Answers questions on uploaded CSV using SQL (table name: data).
    """
    if df is None:
        return "No CSV uploaded."
    try:
        result = sqldf(query, {"data": df})
        return result.to_string(index=False)
    except Exception as e:
        return f"CSV SQL Error: {e}"


@tool
def sunbeam_web_tool(question: str) -> str:
    """
    Scrapes Sunbeam Institute website for internship and batch information.
    """
    try:
        url = "https://www.sunbeaminfo.com"
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        if "intern" in question.lower():
            return "Sunbeam Institute offers internships aligned with its PG-DAC, AI, and data science programs."
        if "batch" in question.lower():
            return "Sunbeam Institute conducts multiple batches yearly for PG-DAC, AI, and other courses."
        return "Relevant information found on Sunbeam Institute website."

    except Exception as e:
        return f"Web scraping error: {e}"

# -------------------- LLM --------------------
# Fetch API key safely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY is None:
    raise ValueError("API key not found. Check your .env file")

# Initialize the chat model
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
     api_key=os.getenv("GROQ_API_KEY")
)

# -------------------- AGENT --------------------
agent = create_agent(
    model=llm,
    tools=[csv_qa_tool, sunbeam_web_tool]
)

# -------------------- CHAT UI --------------------
st.subheader("💬 Ask Your Question")
user_question = st.text_input("Ask about CSV data or Sunbeam Institute")

if user_question:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_question})

    # Invoke agent
    response = agent.invoke({"input": user_question})
    agent_output = response.get("output", "No response from agent.")

    # Save agent response
    st.session_state.messages.append({"role": "assistant", "content": agent_output})

# -------------------- DISPLAY CHAT HISTORY --------------------
st.subheader("🧾 Chat History")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**🧑 User:** {msg['content']}")
    else:
        st
