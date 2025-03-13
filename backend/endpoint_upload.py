from flask import Blueprint, current_app, jsonify, request
import subprocess
import os
import parse_pdf

endpoint_upload = Blueprint('endpoint_upload', __name__)

LOCAL_UPLOAD_FOLDER = 'uploads'
# Allowed file extensions (to limit the types of files that can be uploaded)
ALLOWED_EXTENSIONS = {'pdf'}

# Function to check allowed file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create the upload folder if it doesn't exist
if not os.path.exists(LOCAL_UPLOAD_FOLDER):
    os.makedirs(LOCAL_UPLOAD_FOLDER)

@endpoint_upload.route('/upload', methods=['POST'])
def upload_file():
    print('File uploading.')

    print('F0.')
    # Check if the request contains a file
    if 'file' not in request.files:
        response = jsonify({'error': 'No file part'})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json' 
        return response
    
    print('F1.')
    file = request.files['file']
    
    print('F2.')
    # Check if the file has a valid name
    if file.filename == '':
        response = jsonify({'error': 'No selected file'})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json' 
        return response
    
    print('F3.')
    # Check if the file extension is allowed
    if not allowed_file(file.filename):
        response = jsonify({'error': 'File type not allowed'})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json' 
        return response
    
    print('F4.')
    # Save the file to the upload folder
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    print('F5.')
    topics = parse_pdf.parse_pdf(file_path)

    print('F6.')
    # Respond with the file path and other relevant info
    response = jsonify({'message': 'File uploaded and parsed.', 'file_path': file_path, 'topics': topics[1]})
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    return response
    # return jsonify({'message': 'File uploaded and parsed successfully', 'file_path': file_path, 'topics': topics[1]}), 200

