from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from langchain.agents import create_agent
load_dotenv()
import os
llm = init_chat_model(
"google/gemma-3-4b",
model_provider="openai",
base_url=os.environ.get("http://127.0.0.1:1234/v1"),
api_key=os.getenv("GROQ_API_KEY")

)
agent = create_agent(model=llm, tools=[])
result = agent.invoke({
"messages": [{"role": "user", "content": "What isLangChain"}]
})
print(result["messages"][-1].content)
