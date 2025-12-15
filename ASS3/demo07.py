import streamlit as st
# Input widgets

name = st.text_input("enter your name:")
message = st.text_area("enter your message:", height=100)
uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'csv'])
model = st.selectbox("Choose AI model:", ["GPT-4", "Llama 3", "Gemini", "Claude"])
# Display widgets
if name:
 st.write(f"Hello, {name}!")
 st.markdown("**This is bold text** and *this is italic*")
# Display dataframe
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
st.dataframe(df)
# Display JSON
config = {"model": "gpt-4", "temperature": 0.7, "max_tokens": 500}
st.json(config)