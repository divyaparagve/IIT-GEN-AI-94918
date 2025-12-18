import streamlit as st
st.title("Widget")
st.button("Click Me")

#for adding functionality to the button

if st.button("subscribe"):
    st.write("Thank you for subscribing!")
    
name = st.text_input("Enter your name","Type here...") 
st.write("Your name is:",name)
   
address = st.text_area("Enter your address","Type here...")
st.write("Your address is:",address)

st.date_input("Enter your date")

st.time_input("Enter time")

#st.checkbox("I agree to the terms and conditions",value=False/True)

#for adding functionality to checkbox
if st.checkbox("I agree to the terms and conditions",value=False):
    st.write("thank you")
    
st.radio("Colours",["red","blue","green"],index=1)  
st.selectbox("Colours",["red","blue","green"],index=0)  

#if we want
#v1=st.radio("Colours",["red","blue","green"],index=1)  
#v2=st.selectbox("Colours",["red","blue","green"],index=0) 
#st.write(v1,v2)

#adding like a list
v3 = st.multiselect("Colours",["red","blue","green"])
st.write(v3)

st.slider("age")
#st.slider("age",min_value=0,max_value=100,value=25,value=60,value=30)