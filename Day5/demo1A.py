from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()   
api_key = os.getenv("GROQ_API_KEY")
llm=ChatGroq(model="llama-3.3-70b-versatile")
user_input = input("You: ")
result=llm.invoke(user_input)
print("AI: ", result.content)
 