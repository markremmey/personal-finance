import React, { useEffect } from 'react';
// import './Record.css';


function Record({ record, getNextRecord }) {
  
  useEffect(() => {
    getNextRecord();
    }, []);
  
  if (!record) return null;

  const data = JSON.parse(record);
  
  return (
    <div className="record">
      {Object.keys(data).map((key) => (
        <div key={key}><strong>{key.replace(/_/g, ' ')}:</strong> {data[key]}</div>
      ))}
    </div>
  );
}

export default Record;
