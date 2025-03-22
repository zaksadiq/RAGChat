from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
#
import os
#
from endpoint_generate import endpoint_generate
from endpoint_upload import endpoint_upload, LOCAL_UPLOAD_FOLDER
#
import chromadb


app = Flask(__name__)

cors = CORS(app) # Prevent CORS warning/error on frontend. 

app.register_blueprint(endpoint_generate)
app.register_blueprint(endpoint_upload)

app.config['UPLOAD_FOLDER'] = LOCAL_UPLOAD_FOLDER
app.config['CHROMADB_CLIENT'] = chromadb.Client() # Vector database global variable.

if __name__ == "__main__":
    app.run(port=5001, debug=True)