
import streamlit as st
import pandas as pd
from pandasql import sqldf
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

st.set_page_config(page_title="CSV SQL Chatbot", layout="wide")
st.title(" CSV Chatbot using SQL + LLM")

# Initialize LLM
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    st.subheader(" CSV Preview")
    st.dataframe(data.head())

    st.subheader(" CSV Schema")
    st.write(data.dtypes)

    # Bind DataFrame for SQL
    pysqldf = lambda q: sqldf(q, {"data": data})

    # User question
    user_question = st.text_input("Ask anything about this CSV")

    if st.button("Run Query") and user_question:

        # -------- Requirement 1: NL → SQL --------
        sql_prompt = f"""
        Table Name: data
        Table Schema: {data.dtypes}

        Question:
        {user_question}

        Instruction:
        Write a SQL query for the above question.
        Output ONLY the SQL query.
        """

        with st.spinner("Generating SQL..."):
            sql_query = llm.invoke(sql_prompt).content.strip()

        st.subheader(" Generated SQL")
        st.code(sql_query, language="sql")

        # Execute SQL
        try:
            result_df = pysqldf(sql_query)

            st.subheader("Query Result")
            st.dataframe(result_df)

        except Exception as e:
            st.error(f"SQL Execution Error: {e}")
            st.stop()

        # -------- Requirement 2: Explain Result --------
        explain_prompt = f"""
        User Question:
        {user_question}

        SQL Query:
        {sql_query}

        Query Result:
        {result_df.to_string(index=False)}

        Instruction:
        Explain the result in simple English.
        """

        with st.spinner("Explaining result..."):
            explanation = llm.invoke(explain_prompt)

        st.subheader("Explanation")
        st.success(explanation.content)
