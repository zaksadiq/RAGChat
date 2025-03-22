import { useEffect, useState } from 'react';
import { reuleaux } from 'ldrs'
reuleaux.register('loading-animation')
import axios from "axios";

export default function CommentThread({ keyProp }) {

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
