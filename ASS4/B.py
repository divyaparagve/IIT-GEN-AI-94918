import streamlit as st
import numpy as np
import pandas as pd
a = [1,2,3,4,5,6,7,8]
n = np.array(a)
nd = n.reshape((2,4))
dic = {
    "name":["divya","alice","bob","charlie"],
    "age":[22,56,34,23],
    "city":["bangalore","newyork","chicago","sanfrancisco"]
}

data = pd.read_csv("products.csv")
st.dataframe(data)