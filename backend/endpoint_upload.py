from flask import Blueprint, current_app, jsonify, request
#
import subprocess
import os
#
import chromadb
import parse_pdf


endpoint_upload = Blueprint('endpoint_upload', __name__)

# Constants
LOCAL_UPLOAD_FOLDER = 'uploads'

# Create the upload folder if it doesn't exist
if not os.path.exists(LOCAL_UPLOAD_FOLDER):
    os.makedirs(LOCAL_UPLOAD_FOLDER)


@endpoint_upload.route('/upload', methods=['POST'])
def upload_file():
    print('File uploading.')

    # Validation.
    #
    print('F0.')
    if 'file' not in request.files: 
        response = jsonify({'error': 'No file key in request.'})
        response.status_code = 400 # Bad request code.
        response.headers['Content-Type'] = 'application/json' 
        return response
    #

    # A bit of logic.
    file = request.files['file']

    # Continue  validation (could be extracted).
    print('F1.')
    if file.filename == '':
        response = jsonify({'error': 'Blank filename, possible error selecting file.'})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json' 
        return response
    #
    print('F2.')
    if not file.filename.endswith('.pdf') and not file.filename.endswith('.PDF'):
        response = jsonify({'error': 'Did not end in .PDF file extension.'})
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json' 
        return response
    #

    # Continue logic.
    #
    # Save file.
    print('F3.')
    path_with_filename_to_save_pdf = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path_with_filename_to_save_pdf)
    saved_pdf_path = path_with_filename_to_save_pdf # Sugar to make this more readable later / semantics now pdf is saved.
    #
    # Generate topics from .PDF.
    print('F4.')
    chromadb_client = current_app.config.get('CHROMADB_CLIENT', chromadb.Client())
    topics = parse_pdf.parse_pdf(saved_pdf_path, chromadb_client)

    #
    # Return.
    print('F5.')
    response = jsonify({'message': 'File uploaded and parsed.', 'file_path': saved_pdf_path, 'topics': topics[2]})
    response.status_code = 200
    response.headers['Content-Type'] = 'application/json'
    return response
