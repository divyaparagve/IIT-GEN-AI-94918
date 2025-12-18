import streamlit as st
# Initialize session state
if 'messages' not in st.session_state:
 st.session_state.messages= []
# Display chat history
if st.session_state.messages:
 st.subheader("Chat History")
for msg in st.session_state.messages:
 st.write(msg)
# input the message and append to history
message = st.chat_input("Say something")
if message:
 st.session_state.messages.append(message)
 
with st.sidebar:
 st.header("Settings")
options = ["Upper", "Lower", "Toggle"]
case = st.selectbox("Select Case", options)
count = st.slider("Max Messages", 3, 10, 3, 1)
st.subheader("Current Conf")
st.json({"mode": case, "count": count})
if st.button("Clear History"):
 st.session_state.messages = []