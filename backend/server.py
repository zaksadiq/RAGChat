from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import requests
from huggingface_hub import InferenceClient
import os


app = Flask(__name__)

# Prevent CORS warning/error on frontend. 
cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16 MB


OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"

payload = {
    "model": "deepseek-r1:7b",
    # "prompt": "Generate a conversation with 7 distinct messages all as social media comments following on from each other, where all messages are objects in an array returned in the messages property of the returning json, and each message object is provided with an integer id property based on its position in the series, and the property message for the contents of that particular comment. Respond using JSON.",
    # "prompt": "Generate JSON containing JSON of an array of 7 distinct messages which follow as an internet comments style conversation. Provide each as a JSON object with properties of id and message, following these strict two properties consistently. DO NOT USE HTML ELEMENTS SUCH AS SPAN JUST KEEP IT PLAIN TEXT AND EMOJI. The output must be presentable for a final product, so do not use bracketed syntax for placeholders such as '[TOPIC]'. DO NOT OUTPUTq '[TOPIC]'",
    "prompt": """Always respond in the exact JSON format:

                {
                "messages": [
                    {"id": 1, "message": "your response here"},
                    {"id": 2, "message": "another response here"}
                ]
                }

                Do not add explanations, only return a valid JSON object.    
                Generate JSON containing JSON of an array of 7 distinct messages which follow as a COHERENT internet discussion about a topic of your choosing. Provide each as a JSON object with properties of id and message, following these strict two properties consistently. DO NOT USE HTML ELEMENTS SUCH AS SPAN JUST KEEP IT PLAIN TEXT AND EMOJI. The output must be presentable for a final product and NOT USE TEMPLATES SUCH AS [TOPIC] [PRODUCT X] AND SO ON.""",
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


client = InferenceClient(
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
    token="",
)
# prompt = "Explain quantum computing in simple terms."
prompt = "Generate JSON containing JSON of an array of 7 distinct messages which follow as a COHERENT internet discussion about a topic of your choosing. Provide each as a JSON object with properties of id and message, following these strict two properties consistently. DO NOT USE HTML ELEMENTS SUCH AS SPAN JUST KEEP IT PLAIN TEXT AND EMOJI. The output must be presentable for a final product and NOT USE TEMPLATES SUCH AS [TOPIC] [PRODUCT X] AND SO ON."

@app.route("/message")
def get_message():
    try:
        # Make call to Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload) # 'json' serialises the payload for us.
        # response = client.text_generation(prompt, max_new_tokens=200)
        response.raise_for_status() # Raise exception based on status code
        print('about to print:')
        # print(response)
        # return jsonify(response)
        return jsonify(response.json())
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

    # except requests.RequestException as e:
    #     return jsonify({"error": str(e)}), 500



    
# File Upload

# Allowed file extensions (to limit the types of files that can be uploaded)
ALLOWED_EXTENSIONS = {'pdf'}

# Function to check allowed file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    print('File uploading.')
    # Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # Check if the file has a valid name
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Check if the file extension is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Save the file to the upload folder
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Respond with the file path or other relevant info
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200






if __name__ == "__main__":
    app.run(port=5001, debug=True)