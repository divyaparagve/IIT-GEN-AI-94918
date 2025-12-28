import pandas as pd
from pandasql import sqldf
import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import re

load_dotenv()

# -------------------------------
# LLM Setup
# -------------------------------
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ===============================
# TOOL 1: CSV QUESTION ANSWERING
# ===============================

@tool
def csv_qa_tool(csv_path: str, question: str) -> str:
    """Answer questions on CSV using SQL"""
    try:
        df = pd.read_csv(csv_path)
        schema = df.dtypes.to_string()

        prompt = f"""
You are an expert SQL assistant.

Table name: df

Schema:
{schema}

Rules:
- Use SQLite syntax
- Use table name df only
- Return ONLY SQL

Question:
{question}
"""

        sql_query = llm.invoke(prompt).content
        sql_query = re.sub(r"```sql|```", "", sql_query).strip()

        result = sqldf(sql_query, {"df": df})

        return f"""
📊 SCHEMA:
{schema}

🧠 GENERATED SQL:
{sql_query}

✅ RESULT:
{result.to_string(index=False)}
"""

    except Exception as e:
        return f"❌ CSV Tool Error: {str(e)}"


# ===============================
# TOOL 2: WEB SCRAPING TOOL
# ===============================

@tool
def web_scraping_tool(url: str, question: str) -> str:
    """Scrape website and answer questions"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        page_text = " ".join(
            tag.get_text(strip=True)
            for tag in soup.find_all(["p", "li", "h1", "h2", "h3"])
        )

        prompt = f"""
Answer the question strictly using the content below.

CONTENT:
{page_text[:6000]}

QUESTION:
{question}
"""

        return llm.invoke(prompt).content

    except Exception as e:
        return f"❌ Web Tool Error: {str(e)}"


# ===============================
# USER INPUT (TERMINAL)
# ===============================

if __name__ == "__main__":

    print("\n===== CSV QUESTION ANSWERING =====")
    csv_path = input("Enter CSV file path: ")
    csv_question = input("Ask a question about the CSV: ")

    csv_response = csv_qa_tool.invoke({
        "csv_path": csv_path,
        "question": csv_question
    })

    print("\n--- CSV TOOL OUTPUT ---")
    print(csv_response)

    print("\n===== WEB SCRAPING QA =====")
    url = input("Enter website URL: ")
    web_question = input("Ask a question about the website: ")

    web_response = web_scraping_tool.invoke({
        "url": url,
        "question": web_question
    })

    print("\n--- WEB TOOL OUTPUT ---")
    print(web_response)
