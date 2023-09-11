import React from 'react';
import './Record.css';

function Record({ record }) {
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
