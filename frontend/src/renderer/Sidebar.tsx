import { useEffect, useState, useRef } from 'react';

export default function Sidebar({ setGenerate, setGenerateDisabled }) {
  
  const [file, setFile] = useState<Blob | null>(null);
  const [filename, setFilename] = useState<String | null>(null);
  const [uploading, setUploading] = useState<Boolean>(false);
  const [uploaded, setUploaded] = useState<Boolean>(false);
  const [success, setSuccess] = useState<Boolean>(false);
  const [response, setResponse] = useState<String>("");

  const fileInputRef = useRef();

  const browseFile = e => {
    // Use hidden file input when button is pressed.
    fileInputRef.current.click()
  }
  const uploadFileOnSelect = e => {
    console.log('Selected file.');
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFilename(selectedFile.name);
      setFile(selectedFile);
    }
  }

  // Run when file updates.
  useEffect(() => {
      // Send it to the backend.
      if (file !== null) {
        sendFileToBackend(file);
      }
  }, [file]);

  const sendFileToBackend = async (file : Blob) => {
    setGenerate(false);
    setGenerateDisabled(true);
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file); // Append file to formData
    try {
      console.log('About to make API call.');
      // Make API call to upload the file
      const APIResponse = await fetch('http://127.0.0.1:5001/upload', {
        method: 'POST',
        body: formData,
      });

      console.log('Response:');
      console.log(APIResponse);

      const response = await APIResponse.json();
      if (!APIResponse.ok) {
        throw new Error(response.error);
      } else {
        setResponse(response);
        setSuccess(true);
      }
    } catch (error) {
      setSuccess(false);
      setResponse(error.message);
      console.error(error); 
    } finally {
      setUploading(false); // Reset uploading state
      setUploaded(true);
      setGenerateDisabled(false);
    }
  }

  return (
    <div>
      <button disabled={uploading} id="btn-upload" onClick={browseFile}>+</button>
      <input onChange={uploadFileOnSelect} ref={fileInputRef} style={{ display: 'none' }} type="file" />
      { uploading ? <p className="wrapper-fileThumbnail">Uploading...</p> : (uploaded && success) ? <>
        <div className="wrapper-fileThumbnail">
          <div className="fileThumbnail">
          </div>
          <p>{response.file_path ? response.file_path : filename}</p>
          <ol className="topics">
            Topics:
            {response.topics ? response.topics.map((item, index) => (
              <li key={index}>{item}</li>
            )) : ""}
          </ol>
        </div>
      </> : (uploaded && !success) ? <p className="wrapper-fileThumbnail">Error: {response}</p> : <>
        <div className="wrapper-fileThumbnail">
          <p>No file uploaded.</p>
        </div>
      </>
      }
    </div>
  );
}