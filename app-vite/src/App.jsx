import React, { useState } from 'react';
import Record from './components/Record'
import Categories from './components/Categories'

function App() {
  const [currentRecordId, setCurrentRecordId] = useState(null);
  const [recordData, setRecordData] = useState(null);
  const [currentRecord, setCurrentRecord] = useState(null);
  
  const getNextRecord = () => {
    fetch('http://localhost:5000/get_record')
      .then(response => response.json())
      .then(data => {
        setCurrentRecordId(data.id);
        setRecordData(JSON.stringify(data, null, 2));
      });
  };

  const classifyRecord = (category) => {
    if (currentRecordId) {
      fetch('http://localhost:5000/label_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          id: currentRecordId,
          label: category,
        }),
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          getNextRecord();
        });
    } else {
      console.log('No record to classify');
    }
  };

  return (
    <div>

        <div className="App">
          <button onClick={getNextRecord}>Get Next Record</button>
          
          <div id="record" style={{ whiteSpace: 'pre-wrap' }}>
            {recordData}
          </div>

          {/* <Record record={currentRecord} /> */}
          <Categories classifyRecord={classifyRecord} />
        </div>
      
      </div>
  );
}

export default App;


{/* <div className="App">
        <button onClick={getNextRecord}>Get Next Record</button>
        <Record record={currentRecord} />
        <Categories classifyRecord={classifyRecord} />
      </div> */}
      
      {/* Version 2 of the "Get Next Record Button" This should set the value of recordData, which will be referenced in the next div */}
      {/* <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', textAlign: 'center' }}>
        <button onClick={getNextRecord}>Get Next Record</button> */}
                  
        {/* This div is for the "Record" display, but this will be ommitted for the imported Record.
        However, We will comment this out so that we can have this rendered above   */}
        {/* <div id="record" style={{ whiteSpace: 'pre-wrap' }}>
          {recordData}
        </div> */}

        {/* This div is for the category buttons that appear below the "Get Next Record" button.
        However, We will comment this out so that we can have this rendered above         */}
        {/* <div id="categories">
          <button onClick={() => classifyRecord('Groceries')}>Groceries</button>
          <button onClick={() => classifyRecord('Home Improvement')}>Home Improvement</button>
          <button onClick={() => classifyRecord('Subscriptions')}>Subscriptions</button>
          <button onClick={() => classifyRecord('Utilities')}>Utilities</button>
        </div>
       */}