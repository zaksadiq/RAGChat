import { useEffect, useState, useRef } from 'react';
import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import icon from '../../assets/icon.svg';
import './App.css';
import { reuleaux } from 'ldrs'
reuleaux.register('loading-animation')
import axios from "axios";

function CommentThread() {


  const [messagesJSON, setMessagesJSON] = useState<string>(""); 
  const [messages, setMessages] = useState<Array<string>>([]); 

  const fetchMessages = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5001/message");
      console.log('Got response.');
      // console.log(response.json());
      const data: ApiResponse = await response.json();
      setMessagesJSON(data.response);
    } catch (error) {
      console.error("Error fetching from API: ", error);
    }
  }

  const saveMessages = () => {

    console.log('messages json.');
    console.log(messagesJSON);
    // Check the three gates.
    if (messagesJSON != "" && messagesJSON !== undefined && messagesJSON !== null) {
      console.log('about to parse:');
      console.log(messagesJSON);
      const json: { messages: Array<{ id: number, message: string }> } = JSON.parse(messagesJSON);
      console.log('json parsed!');
      console.log(json);
      const temporaryMessagesArray: Array<string> = [];
      json.messages.map( (value: { id: number; message: string }, index: number) => {
        temporaryMessagesArray[index] = value.message;
      });
      setMessages(temporaryMessagesArray);
    }
  }

  // Run on initial app execution.
  useEffect(() => {
    fetchMessages();
  }, []);
  
  // Run when messagesJSON updates.
  useEffect(() => {
    saveMessages();
  }, [messagesJSON]);

  return (
    <>
      {/* <span>Message JSON:</span> */}
      {/* <span>{messagesJSON}</span> */}
      <div className="comment-thread-box">
      { 
        messages.length > 0 ? (
          messages.map( (value: string, index: number) => {
            return (
              <div key={index} className={index > 0 ? 'sub-comment' : 'parent-comment'}>
                {value}
              </div>
            );
          }) 
        ) : ( 
          <>
            <div className="greeking"></div>
            <div className="greeking"></div>
            <div className="greeking"></div>
            <div className="loading-box">
              <div className="loading-animation">
                <loading-animation size="30"></loading-animation>
              </div>
              {/* <span>Loading...</span> */}
            </div>
          </>
        ) 
      }
      </div>
    </>
  );
}

function Sidebar() {
  
  const [file, setFile] = useState<Blob | null>(null);
  const [filename, setFilename] = useState<String | null>(null);
  const [uploading, setUploading] = useState<Boolean>(false);
  const [response, setResponse] = useState<String>("");

  const fileInputRef = useRef();

  const browseFile = e => {
    // Use hidden file input.
    fileInputRef.current.click()
  }
  const uploadFileOnSelect = e => {
    console.log('Selected file.');
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFilename(selectedFile.name);
      setFile(selectedFile);
      sendFileToBackend(file);
    }
    
    // Send it to the backend.
    setUploading(true);
  }
  const sendFileToBackend = async (file : Blob) => {
    const formData = new FormData();
    formData.append("file", file); // Append file to formData
    try {
      console.log('About to make API call.');
      // Make API call to upload the file
      const APIResponse = await fetch('http://127.0.0.1:5001/upload', {
        method: 'POST',
        body: formData,
      });
      console.log(APIResponse);
      // console.log(APIResponse.data); // Handle response as needed
      // setResponse(APIRresponse.data);
    } catch (err) {
      console.error(err); // Handle any errors
    } finally {
      setUploading(false); // Reset uploading state
    }
  }

  return (
    <>
      <div>
        <button disabled={uploading} id="btn-upload" onClick={browseFile}>+</button>
        <input onChange={uploadFileOnSelect} ref={fileInputRef} style={{display:'none'}} type="file" />
        { uploading ? <>
              Uploading...
              {/* <div className="loading-animation">
                <loading-animation size="30"></loading-animation>
              </div> */}
          </> : <> 
          {response}
                <div class="wrapper-fileThumbnail">
                  <div class="fileThumbnail">
                  </div>
                  <p>{filename}</p>
                </div>
          </> }
      </div>
    </>
  );
}

function UI() {



  return (
    <div id="wrapper">
      <div id="inner-body">
        <CommentThread />
        <CommentThread />
        <CommentThread />
        <CommentThread />
        <CommentThread />
      </div>
      <div id="sidebar-r">
        <Sidebar />
      </div>
    </div>
  );
}



export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UI />} />
      </Routes>
    </Router>
  );
}
