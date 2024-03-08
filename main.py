import google.generativeai as genai
from flask import Flask, jsonify
import requests
import base64
import json

app = Flask(__name__)

genai.configure(api_key="AIzaSyAPjctkeCjBluMysPLZxZyJrnJFUi9dJ-M")

# Set up the model
gen_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=gen_config,
                              safety_settings=safety_settings)


REPO_URL = "https://api.github.com/repos/marak27/BiblePromtData/contents/mainPromt.json"
TOKEN = "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"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v4+raw"
}

mainPromt = []

response = requests.get(REPO_URL, headers=headers)

if response and response.status_code == 200:
    binary_content = base64.b64decode(response.json()["content"])
    content = binary_content.decode("utf-8")
    mainPromt = json.loads(content)
else:
    print(response)


chat = model.start_chat(history= mainPromt)

data = []

@app.route('/')
def home():
    return "Hello Bible enthusiast, add /input/<promt> to chat and add /history to check the history"

@app.route('/input/<promt>', methods=['GET'])
def input(promt):
    response = chat.send_message(promt, stream=True)
    for chunk in response:
        data.append(chunk.text)
    temp = ' '.join(data)
    return temp

@app.route('/history', methods=['GET'])
def history():
    history = chat.history
    hst = history[1:]
    return hst

#if __name__ == '__main__':
#    app.run()
