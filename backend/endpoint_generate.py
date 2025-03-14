from flask import Blueprint, current_app, jsonify, request
from huggingface_hub import InferenceClient

import api_keys
import requests

import chromadb
from random_topic_and_rag import select_random_and_do_rag

endpoint_generate = Blueprint('endpoint_generate', __name__)


OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"

client = InferenceClient(
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    token=api_keys.HUGGING_FACE_API_KEY,
)
# prompt = "Explain quantum computing in simple terms."
prompt = "Generate JSON containing JSON of an array of 7 distinct messages which follow as a COHERENT internet discussion about a topic of your choosing. Provide each as a JSON object with properties of id and message, following these strict two properties consistently. DO NOT USE HTML ELEMENTS SUCH AS SPAN JUST KEEP IT PLAIN TEXT AND EMOJI. The output must be presentable for a final product and NOT USE TEMPLATES SUCH AS [TOPIC] [PRODUCT X] AND SO ON."

@endpoint_generate.route("/message")
def get_message():
    try:
        chromadb_client = current_app.config.get('CHROMADB_CLIENT', chromadb.Client())
        random_topic_text = select_random_and_do_rag(chromadb_client)
        payload = {
            "model": "deepseek-r1:7b",
            "prompt": f"""Always respond in the exact JSON format:

                        {{
                        "messages": [
                            {{"id": 1, "message": "your response here"}},
                            {{"id": 2, "message": "another response here"}}
                        ]
                        }}

                        Do not add explanations, only return a valid JSON object.    
                        Using the following context, 

                            {random_topic_text}

                        Generate JSON containing JSON of an array of 7 distinct messages which follow as a COHERENT internet discussion. Provide each as a JSON object with properties of id and message, following these strict two properties consistently. DO NOT USE HTML ELEMENTS SUCH AS SPAN JUST KEEP IT PLAIN TEXT AND EMOJI. The output must be presentable for a final product and NOT USE TEMPLATES SUCH AS [TOPIC] [PRODUCT X] AND SO ON.""",
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
        response = requests.post(OLLAMA_API_URL, json=payload) # 'json' serialises the payload for us.
        # response = client.text_generation(prompt, max_new_tokens=200)
        response.raise_for_status() # Raise exception based on status code
        print('about to print:')
        # print(response)
        # return jsonify(response)
        return jsonify(response.json())
    except Exception as e:
        current_app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

    # except requests.RequestException as e:
    #     return jsonify({"error": str(e)}), 500
