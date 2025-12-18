import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import altair as alt

data = pd.DataFrame (
    np.random.randn(100, 3),
    columns=['a', 'b', 'c']
 )

chart = alt.Chart(data).mark_circle().encode(
    x='a',  y='b',  tooltip=['a', 'b']
 )

st.graphviz_chart("""
digraph { 
watch -> football;
football -> soccer;
soccer -> cricket;
}
""")

st.map()

city = pd.DataFrame({
    'lat':[37.76,37.77,37.78,37.79],
    'lon':[-122.4,-122.41,-122.42,-122.43]
    
})
st.map(city)

st.altair_chart(chart,use_container_width=True)


plt.scatter(data['a'], data['b'])
plt.title("Scatter")
st.pyplot()

st.line_chart(data)
st.area_chart(data)
st.bar_chart(data)

#media

st.image("PP (135).JPG")
st.video("u can add u tube link also")
st.audio("")