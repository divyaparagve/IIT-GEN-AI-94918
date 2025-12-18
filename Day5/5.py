from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
import pandas as pd
from pandasql import sqldf

load_dotenv()

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

csv_file = input("Enter CSV file name: ")
data = pd.read_csv(csv_file)

print("\nCSV schema:")
print(data.dtypes)

# ✅ Guaranteed pandasql binding
pysqldf = lambda q: sqldf(q, {"data": data})

while True:
    user_input = input("\nAsk anything about this CSV (type exit to quit): ")

    if user_input.lower() == "exit":
        break

    # -------- Assignment 1: NL → SQL --------
    llm_input = f"""
    Table Name: data
    Table Schema: {data.dtypes}

    Question:
    {user_input}

    Instruction:
    Write a SQL query for the above question.
    Output ONLY the SQL query.
    """

    sql_query = llm.invoke(llm_input).content.strip()

    print("\nGenerated SQL:")
    print(sql_query)

    # -------- Execute SQL on Pandas --------
    try:
        result_df = pysqldf(sql_query)
        print("\nQuery Result:")
        print(result_df)
    except Exception as e:
        print("❌ SQL Execution Error:", e)
        continue

    # -------- Assignment 2: Explain Result --------
    explanation_prompt = f"""
    User Question:
    {user_input}

    SQL Query:
    {sql_query}

    Query Result:
    {result_df.to_string(index=False)}

    Instruction:
    Explain the result in simple English for a beginner.
    """

    explanation = llm.invoke(explanation_prompt)

    print("\nExplanation:")
    print(explanation.content)
