import streamlit as st

# Page title
st.title("🤖  Shriram mali")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")

# Simple chatbot logic
def bot_reply(user_text):
    user_text = user_text.lower()

    if "hello  " in user_text or "hi" in user_text:
        return "plz come mali  😊 "
    elif "i want to say" in user_text:
        return "plx come here."
    elif "come fast" in user_text:
        return " i am waiting 👋"
    else:
        return "Sorry, I didn't understand that."

# Process input
if user_input:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Get bot response
    response = bot_reply(user_input)

    # Save bot message
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    # Display bot response
    with st.chat_message("assistant"):
        st.write(response)


