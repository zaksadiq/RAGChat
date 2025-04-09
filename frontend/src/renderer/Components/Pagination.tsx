import { useEffect, useState } from 'react';

import CommentThread from './CommentThread';


export default function Pagination() {

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
        {discussionThreads}
        <button onClick={newPage}>{'>'}</button>
    </div>
  )
}
