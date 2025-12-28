import streamlit as st

st.markdown("<h1>USER REGISTRATION</h1>",unsafe_allow_html=True)
#(1)form=st.form("form 1")
#st.text_input("First Name")
#form.form_submit_button("Submit")

#(2)with st.form("form 2"):
   # st.text_input("First  Name")
   # st.form_submit_button("Submit")
   # st.text_input("Last Name")
   # st.form_submit_button("Submit")
   # st.text_input("Email")
   # st.form_submit_button("Submit")
   
   #creating columns
with st.form("form 2"):   
 col1,col2=st.columns(2)
 col1.text_input("First Name")
 col2.text_input("Last Name")
 st.text_input("Email Address")
 st.text_input("Phone Number")
 st.text_input("Password")
 st.text_input("Confirm Password")
 st.form_submit_button("Submit")