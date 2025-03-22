import { useEffect, useState, useRef } from 'react';

import Pagination from './Pagination';
import Sidebar from './Sidebar';

export default function UI() {
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
