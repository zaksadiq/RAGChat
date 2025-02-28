import { useEffect, useState } from 'react';
import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import icon from '../../assets/icon.svg';
import './App.css';
import { reuleaux } from 'ldrs'
reuleaux.register('loading-animation')

function CommentThread() {


  const [messagesJSON, setMessagesJSON] = useState<string>(""); 
  const [messages, setMessages] = useState<Array<string>>([]); 

  const fetchMessages = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/message");
      const data: ApiResponse = await response.json();
      setMessagesJSON(data.response);
    } catch (error) {
      console.error("Error fetching from API: ", error);
    }
  }

  const saveMessages = () => {

    if (messagesJSON != "") {
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

  // Run on app execution.
  useEffect(() => {
    fetchMessages();
  }, []);
  
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

function UI() {



  return (
    <>
      <CommentThread />
      <CommentThread />
    </>
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
