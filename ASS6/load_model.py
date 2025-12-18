import os
import requests
import json
import time
#from dotenv import load_dotenv

#load_dotenv()

Api_key = "DeMO_KEY"
#Groq_API_key = os.getenv('GROK_API_key')
Groq_API_key = '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'

def groq_request(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Groq_API_key}"
    }
    data = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [{
            "role": "user",
            "content" : user_input
        }],
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()['choices'][0]['message']['content']
    return response_json

def local_request(user_input):
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {Api_key}"
    }
    data = {
        "model": "meta-llama-3.1-8b-instruct",
        "messages": [{
            "role": "user",
            "content" : user_input
        }],
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()['choices'][0]['message']['content']

    return response_json


if __name__ == "__main__":
    user_input = "Explain the theory of relativity in simple terms."
    start_time=time.time()
    response = groq_request(user_input)
    print("Groq Response:", response)
    end_time=time.time()
    print(f"Groq Time taken: {end_time - start_time} seconds")
    start_time=time.time()
    response = local_request(user_input)
    print("Local Response:", response)
    end_time=time.time()
    print(f"Local Time taken: {end_time - start_time} seconds")