from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import requests

app = Flask(__name__)

# Prevent CORS warning/error on frontend. 
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"

payload = {
    "model": "deepseek-r1:8b",
    # "prompt": "Generate a conversation with 7 distinct messages all as social media comments following on from each other, where all messages are objects in an array returned in the messages property of the returning json, and each message object is provided with an integer id property based on its position in the series, and the property message for the contents of that particular comment. Respond using JSON.",
    # "prompt": "Generate JSON containing JSON of an array of 7 distinct messages which follow as an internet comments style conversation. Provide each as a JSON object with properties of id and message, following these strict two properties consistently. DO NOT USE HTML ELEMENTS SUCH AS SPAN JUST KEEP IT PLAIN TEXT AND EMOJI. The output must be presentable for a final product, so do not use bracketed syntax for placeholders such as '[TOPIC]'. DO NOT OUTPUTq '[TOPIC]'",
    "prompt": "Generate JSON containing JSON of an array of 7 distinct messages which follow as a COHERENT internet discussion about a topic of your choosing. Provide each as a JSON object with properties of id and message, following these strict two properties consistently. DO NOT USE HTML ELEMENTS SUCH AS SPAN JUST KEEP IT PLAIN TEXT AND EMOJI. The output must be presentable for a final product and NOT USE TEMPLATES SUCH AS [TOPIC] [PRODUCT X] AND SO ON.",
    "stream": False,
    "format": {
        "type": "object",
        "properties": {
            "messages": {
                "type": "array"
            },
        },
        "required": [
            "messages",
        ]
    }
}

@app.route("/message")
def get_message():
    try:
        # Make call to Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload) # 'json' serialises the payload for us.
        response.raise_for_status() # Raise exception based on status code
        print(response.json())
        return jsonify(response.json())
    
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500