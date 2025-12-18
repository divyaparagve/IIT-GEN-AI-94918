import streamlit as st
if 'counter' not in st.session_state:
 st.session_state.counter = 0
 col1, col2 = st.columns(2)
with col1:
 if st.button("Increment"):
  st.session_state.counter += 1
with col2:
 if st.button("Reset"):
  st.session_state.counter = 0
  st.write(f"{st.session_state.counter}")
