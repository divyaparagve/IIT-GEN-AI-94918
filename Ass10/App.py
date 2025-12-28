import streamlit as st


import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from langchain_core.prompts import PromptTemplate


# Load env
load_dotenv()

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("💬 Ask Your MySQL Database")

st.sidebar.header("🔐 MySQL Connection")

host = st.sidebar.text_input("Host", "localhost")
user = st.sidebar.text_input("User", "root")
password = st.sidebar.text_input("Password", type="password")
database = st.sidebar.text_input("Database", "test_db")

# ----------------------------
# LLM Setup (Groq)
# ----------------------------
llm = init_chat_model(
    model="microsoft/phi-4-mini-reasoning",
    model_provider="openai",
    base_url="http://10.45.159.95:1234/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ----------------------------
# Connect to MySQL
# ----------------------------
def get_connection():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

# ----------------------------
# SQL Generator Prompt
# ----------------------------
sql_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are an expert MySQL assistant.

Generate ONLY a valid SELECT SQL query.
Do NOT use INSERT, UPDATE, DELETE, DROP.

Question: {question}
SQL:
"""
)

# ----------------------------
# Explanation Prompt
# ----------------------------
explain_prompt = PromptTemplate(
    input_variables=["question", "result"],
    template="""
User question: {question}

SQL result:
{result}

Explain the result in simple English.
"""
)

# ----------------------------
# User Question
# ----------------------------
question = st.text_input("Ask a question about your database:")

if st.button("Run Query") and question:
    try:
        # Generate SQL
        sql_query = llm.invoke(sql_prompt.format(question=question)).content.strip()

        st.subheader("🧾 Generated SQL")
        st.code(sql_query, language="sql")

        if not sql_query.lower().startswith("select"):
            st.error("Only SELECT queries are allowed.")
        else:
            # Execute SQL
            conn = get_connection()
            df = pd.read_sql(sql_query, conn)
            conn.close()

            st.subheader("📊 Query Result")
            st.dataframe(df)

            # Explain result
            explanation = llm.invoke(
                explain_prompt.format(
                    question=question,
                    result=df.to_string(index=False)
                )
            ).content

            st.subheader("📝 Explanation")
            st.write(explanation)

    except Exception as e:
        st.error(f"Error: {e}")
