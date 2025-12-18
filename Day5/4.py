import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from dotenv import load_dotenv
load_dotenv()
import os

load_dotenv()

# ---------- LLM ----------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

st.title("Streamlit Chatbot (Context Control)")

# ---------- SLIDER ----------
window_size = st.slider(
    "How many previous messages should the AI remember?",
    min_value=1,
    max_value=20,
    value=5
)

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful assistant.")
    ]

# ---------- USER INPUT ----------
user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.messages.append(HumanMessage(content=user_input))

    # ✅ Send ONLY last N messages + system message
    messages_to_send = (
        [st.session_state.messages[0]] +     # system
        st.session_state.messages[-window_size:]
    )

    response = llm.invoke(messages_to_send)

    st.session_state.messages.append(
        AIMessage(content=response.content)
    )

# ---------- DISPLAY CHAT ----------
for msg in st.session_state.messages[1:]:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.write(msg.content)
