from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------- TOOL ----------------

@tool
def read_file(filename: str) -> str:
    """
    Reads and returns the contents of a text file.
    Use this tool ONLY when the user asks to read a file.
    """
    try:
        if not os.path.exists(filename):
            return f"Error: File '{filename}' not found."

        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# ---------------- MODEL ----------------

llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed"
)

# ---------------- AGENT ----------------

SYSTEM_PROMPT = """
You are a helpful assistant.

Rules:
- If the user asks to read a file, use the read_file tool.
- Extract the filename from the user's message.
- Do NOT answer from memory for file contents.
- Otherwise, error.
"""

agent = create_agent(
    model=llm,
    tools=[read_file],
    system_prompt=SYSTEM_PROMPT
)

# ---------------- CHAT LOOP ----------------

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    print("AI:")
    print(result["messages"][-1].content)
