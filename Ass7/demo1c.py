from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv() 
llm_url = "http://127.0.0.1:1234/v1"
llm = ChatOpenAI(
    base_url=llm_url,
    model="google/gemma-3-4b",
    api_key="dummy-key"
) 

user_input = input("You: ")
result = llm.invoke(user_input)
print("AI: ", result.content)