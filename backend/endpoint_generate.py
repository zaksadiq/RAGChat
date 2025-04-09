from flask import Blueprint, current_app, jsonify, request
from huggingface_hub import InferenceClient
#
import api_keys
import requests
#
import chromadb
from random_topic_and_rag import select_random_topic_and_do_rag


#
endpoint_generate = Blueprint('endpoint_generate', __name__)

## Constants
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
#


#
@endpoint_generate.route("/generate")
def get_message():
    try:
        chromadb_client = current_app.config.get('CHROMADB_CLIENT', chromadb.Client())
        random_topic_text = select_random_topic_and_do_rag(chromadb_client)
        payload = {
            "model": "deepseek-r1:7b",
            "prompt": f"""Respond in JSON, use this format, replacing the content with a generated discussion message:

                        {{
                        "messages": [
                            {{"id": 1, "message": "[Message 1 content.]"}},
                            {{"id": 2, "message": "[Message 2 content.]"}}
                        ]
                        }}

                        Use the following context for the request:

                            {random_topic_text}

                        The request is to generate distinct messages which follow as a COHERENT internet discussion where each message is to do with the provided context and each message can be from a different person. DO NOT USE HTML ELEMENTS SUCH AS SPAN JUST KEEP IT PLAIN TEXT AND EMOJI. The output must be presentable for a final product and NOT USE TEMPLATES SUCH AS [TOPIC] [PRODUCT X] AND SO ON.""",
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

        # Make call to Ollama API
        ai_api_response = requests.post(OLLAMA_API_URL, json=payload) # 'json' serialises the payload for us.
        ai_api_response.raise_for_status() # Raise exception on bad status code
        return jsonify(ai_api_response.json())

    except Exception as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500 # 500 is Internal Server Error code.
#