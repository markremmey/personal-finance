import React from 'react';

function Categories({ classifyRecord }) {
  return (
    <div>
      <button onClick={() => classifyRecord('Groceries')}>Groceries</button>
      <button onClick={() => classifyRecord('Home Improvement')}>Home Improvement</button>
      <button onClick={() => classifyRecord('Subscriptions')}>Subscriptions</button>
      <button onClick={() => classifyRecord('Utilities')}>Utilities</button>
    </div>
  );
}

export default Categories;
