import os
from dotenv import load_dotenv
import requests
import json
import time

load_dotenv()

def groq(user_input):
    GROCK_API_key = os.getenv('GROCK_API_key')
    #print("GROCK_API_key:", GROCK_API_key)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROCK_API_key}"
    }

    data = {
        "model": "moonshotai/kimi-k2-instruct-0905",
        "messages": [{
            "role": "user",
            "content" : user_input
        }],
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()
    #print("Response JSON:", response_json)
    print("Groq Response:", response_json['choices'][0]['message']['content'])



def gemini(user_input):
    gemini_API_key = os.getenv('GEMINI_API_key')

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_API_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": "Hello, how are you?"}
                ]
            }
        ]
    }

    #response = requests.post(url, headers=headers, json=data)
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json() 
    #output=response_json(['candidates'][0]['content']['text'])   
    print("Gemini Response:", response_json)




user_input = input("Enter your query: ")
time_start = time.time()
groq(user_input)
time_end = time.time()
print(f"Time taken for GROQ API call: {time_end - time_start:.2f} seconds")
time_start = time.time()
gemini(user_input)
time_end = time.time()
print(f"Time taken for Gemini API call: {time_end - time_start:.2f} seconds")