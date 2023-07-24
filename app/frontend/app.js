import React from 'react';
import Item from './Item';
import './style.css';
import axios from 'axios';

function App() {
  const items = ['Apple', 'Banana', 'Cherry', 'Canelope'];
  const response = axios.get('get-transaction.azurewebsites.net/get_record');

  return (
    <div className="App">
      <div className="centered">
        <ul>
          {items.map((item, index) => (
            <Item key={index} name={item} />
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;