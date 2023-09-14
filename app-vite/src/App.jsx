import './App.css';
import React, { useState } from 'react';
import Record from './components/Record'
import Categories from './components/Categories'

const x = "test"
console.log(x)

function App() {
  const [currentRecordId, setCurrentRecordId] = useState(null);
  const [recordData, setRecordData] = useState(null);
  // const [currentRecord, setCurrentRecord] = useState(null);
  
  // gets Next Record, the following function calls the local host
  // endpoint to get the next record. Then, it converts the reponse to a JSON
  // object and sets the current record to the response.


  // This function is invoked when the "Get Next Record" button is clicked.
  const getNextRecord = () => {
    fetch('http://localhost:5000/get_record')
      .then(response => response.json())
      .then(data => {
        setCurrentRecordId(data.id);
        setRecordData(JSON.stringify(data, null, 2));
      });
  };
  console.log("recordData", recordData);

  const classifyRecord = (category) => {
    if (currentRecordId) {
      fetch('http://localhost:5000/label_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          id: currentRecordId,
          description: recordData,
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
      <div className="App">
        <button onClick={getNextRecord}>Get Next Transaction</button>
        
        <div id="record" style={{ whiteSpace: 'pre-wrap' }}>
          <Record record={recordData} getNextRecord={getNextRecord} />
        </div>

        <Categories classifyRecord={classifyRecord} />
      </div>
  );
}

export default App;