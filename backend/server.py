from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Prevent CORS warning/error on frontend. 
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/message")
def get_message():        
    return jsonify({ "message": "Hello world!" })