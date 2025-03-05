from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import os
from endpoint_generate import endpoint_generate
from endpoint_upload import endpoint_upload, LOCAL_UPLOAD_FOLDER

app = Flask(__name__)
# Prevent CORS warning/error on frontend. 
cors = CORS(app)

app.register_blueprint(endpoint_generate)
app.register_blueprint(endpoint_upload)

# app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = LOCAL_UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16 MB


if __name__ == "__main__":
    app.run(port=5001, debug=True)