import streamlit as st
from load_model import groq_request, local_request
import time

st.title("Model Comparison: Groq vs Local LLaMA 3.1 8b")

if 'input_text_groq' not in st.session_state:
    st.session_state.input_text_groq = []
if 'groq_response' not in st.session_state:
    st.session_state.groq_response = []
if 'input_text_local' not in st.session_state:
    st.session_state.input_text_local = []
if 'local_response' not in st.session_state:
    st.session_state.local_response = []
if 'current_model' not in st.session_state:
    st.session_state.current_model = "Groq"

def model_write(response):
    with st.spinner(f"model is thinking..."):
        for i in response.split():
            yield i+" "
            time.sleep(0.25)

def display_chat_history(response, user_input, model_name):
    if model_name =="Groq":
        for i ,j in zip(st.session_state.input_text_groq, st.session_state.groq_response):
            if i == user_input and j == response:
                st.chat_message("user").write(i)
                with st.chat_message("assistant"):
                    st.write_stream(model_write(j))

            else:
                st.chat_message("user").write(i)
                st.chat_message("assistant").write(j)
    else:
        for i ,j in zip(st.session_state.input_text_local, st.session_state.local_response):
            if i == user_input and j == response:
                st.chat_message("user").write(i)
                with st.chat_message("assistant"):
                    st.write_stream(model_write(j))
            else:
                st.chat_message("user").write(i)
                st.chat_message("assistant").write(j)


st.sidebar.title("Select Model")
model_choice = st.sidebar.radio("Choose a model to interact with:", ("Groq", "Local LLaMA 3.1 8b"))
if model_choice != st.session_state.current_model:
    st.session_state.current_model = model_choice
    display_chat_history(None, None, model_choice)

user_input=st.chat_input("Enter your message here:")
if user_input:
    if st.session_state.current_model == "Groq":
        st.session_state.input_text_groq.append(user_input)
        response = groq_request(user_input)
        st.session_state.groq_response.append(response)
        display_chat_history(response, user_input, "Groq")
    else:
        st.session_state.input_text_local.append(user_input)
        response = local_request(user_input)
        st.session_state.local_response.append(response)
        display_chat_history(response, user_input, "Local LLaMA 3.1 8b")