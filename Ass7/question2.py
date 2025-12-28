import streamlit as st
import requests
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Streamlit page config
st.set_page_config(page_title="Weather Explanation App", layout="centered")
st.title(" Weather Explanation using LLM")

# Initialize LLM
llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# Weather API key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Input city name
city = st.text_input("Enter city name")

if st.button("Get Weather") and city:

    # Call Weather API
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        st.error(" City not found or API error")
        st.stop()

    weather_data = response.json()

    # Extract data
    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    description = weather_data["weather"][0]["description"]
    wind_speed = weather_data["wind"]["speed"]

    # Display raw weather info
    st.subheader(" Current Weather Data")
    st.write(f" Temperature: {temperature} °C")
    st.write(f" Humidity: {humidity}%")
    st.write(f" Wind Speed: {wind_speed} m/s")
    st.write(f" Condition: {description}")

    # ---------------- Requirement 3 ----------------
    # Ask LLM to explain weather
    explain_prompt = f"""
    City: {city}
    Temperature: {temperature} °C
    Humidity: {humidity}%
    Wind Speed: {wind_speed} m/s
    Weather Condition: {description}

    Instruction:
    Explain the current weather in simple English for a normal person.
    """

    with st.spinner("Explaining weather..."):
        explanation = llm.invoke(explain_prompt)

    st.subheader(" Weather Explanation")
    st.success(explanation.content)
