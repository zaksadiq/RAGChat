import { useEffect, useState, useRef } from 'react';
import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import icon from '../../assets/icon.svg';
import './App.css';
import { reuleaux } from 'ldrs'
reuleaux.register('loading-animation')
import axios from "axios";

function CommentThread({ keyProp }) {

  const [messagesJSON, setMessagesJSON] = useState<string>(""); 
  const [messages, setMessages] = useState<Array<string>>([]); 

  const [startTime, setStartTime] = useState<number | null>(null);
  const [loadedTime, setLoadedTime] = useState<number | null>(null);
  const [timeDelta, setTimeDelta] = useState<number | null>(null);

  const fetchMessages = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5001/generate");
      console.log('Got response.');
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

  // Record time when component is initialised and then when messages is populated, so we can
  // time performance.
  useEffect(() => {
    if (messages.length == 0) {
      // console.log('Start time: ' + Date.now());
      setStartTime(Date.now()); // Millisconds since Unix epoch.
    } else {
      // console.log('Loaded time: ' + Date.now());
      setLoadedTime(Date.now());
    }
  }, [messages]);
  //
  useEffect(() => {
    if (loadedTime !== null) {
      // console.log('Setting time delta:')
      // console.log('StartTime: ' + startTime);
      // console.log('LoadedTime: ' + loadedTime);
      let timeDelta = loadedTime - startTime;
      console.log(`Delta [${keyProp}] = ${timeDelta}ms ; ${timeDelta / 1000}s` )
      setTimeDelta(timeDelta);
    }
  }, [loadedTime]);
  //
  
  // Run when messagesJSON updates.
  useEffect(() => {
    if (messagesJSON !== "") {
      saveMessages();
    }
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
          <div id="wrapper-loading">
            <div className="greeking"></div>
            <div className="greeking"></div>
            <div className="greeking"></div>
            <div className="loading-box">
              <div className="loading-animation">
                <loading-animation size="30"></loading-animation>
              </div>
              {/* <span>Loading...</span> */}
            </div>
          </div>
        ) 
      }
      </div>
    </>
  );
}

function Pagination() {
  const [pageNumber, setPageNumber] = useState(1);
  const [discussionThreads, setDiscussionThreads] = useState([]);
  
  const generateNewThreads = () => {
    const newThreads = []
    for (let i = 0; i < 5; i++) {
      newThreads.push(<CommentThread key={`${pageNumber}-${i}`} keyProp={`${pageNumber}-${i}`} />);
    }
    setDiscussionThreads(newThreads);
  }
  const newPage = () => {
    setPageNumber(pageNumber+1);
  }

  useEffect(() => {
    generateNewThreads();
  }, [pageNumber]);


  return (
    <div className="page">
        <h2>Page {pageNumber}</h2>
        {/* <CommentThread /> */}
        {/* {discussionThreads.map((item, i) => item) } */}
        {discussionThreads}
        <button onClick={newPage}>{'>'}</button>
    </div>
  )
}

function Sidebar({ setGenerate, setGenerateDisabled }) {
  
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

function UI() {
  const [generate, setGenerate] = useState(false);
  const [generateDisabled, setGenerateDisabled] = useState(true);
  
  return (
    <div id="wrapper">
      <div id="inner-body">
      { generate ? 
      <>
        <Pagination />
      </>
      :
      <>
        <button disabled={generateDisabled} onClick={() => setGenerate(true)}>Generate</button>
      </>
      }
      </div>
      <div id="sidebar-r">
        <Sidebar setGenerate={setGenerate} setGenerateDisabled={setGenerateDisabled} />
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
