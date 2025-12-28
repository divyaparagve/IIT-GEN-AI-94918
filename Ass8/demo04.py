from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests

# Load environment variables
load_dotenv()

# -------------------- TOOLS --------------------

@tool
def calculator(expression: str) -> str:
    """
    Solve a mathematical expression.
    Use ONLY for arithmetic calculations.
    """
    try:
        return str(eval(expression))
    except:
        return "Error: Invalid expression"


@tool
def get_weather(city: str) -> str:
    """
    Get the CURRENT weather of a city.
    Use this tool ONLY when the user explicitly asks about weather,
    temperature, or forecast.
    """
    try:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return "Error: Weather API key not found"

        url = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return "Error"

        return json.dumps(data)
    except:
        return "Error"

    


# -------------------- MODEL --------------------

llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-required"
)

# -------------------- AGENT --------------------

SYSTEM_PROMPT = """
You are a helpful assistant.

Rules:
- Answer general knowledge questions directly.
- Use tools ONLY when necessary.
- Use calculator ONLY for math expressions.
- Use get_weather ONLY for weather-related questions.
- Keep answers short and clear.
"""

agent = create_agent(
    model=llm,
    tools=[calculator, get_weather],
    system_prompt=SYSTEM_PROMPT
)

# -------------------- CHAT LOOP --------------------

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    print("AI:", result["messages"][-1].content)
