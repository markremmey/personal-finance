import React, { useState } from 'react';

function Categories({ classifyRecord }) {
  const [categories, setCategories] = useState([]);
  const [newCategory, setNewCategory] = useState('');

  const addCategory = () => {
    if (newCategory.trim() !== '') {
      setCategories([...categories, newCategory]);
      setNewCategory('');
    }
  };

  return (
    <div>

      <button onClick={addCategory}>Add Category</button>
      <input 
        type="text" 
        value={newCategory} 
        onChange={(e) => setNewCategory(e.target.value)} 
        placeholder="Add new category" 
      />
      <div>
        {categories.map((category, index) => (
          <button key={index} onClick={() => classifyRecord(category)}>
            {category}
          </button>
        ))}
      </div>
    </div>
  );
}

export default Categories;


// import React from 'react';

// function Categories({ classifyRecord }) {
//   return (
//     <div>
//       <button onClick={() => classifyRecord('Groceries')}>Groceries</button>
//       <button onClick={() => classifyRecord('Home Improvement')}>Home Improvement</button>
//       <button onClick={() => classifyRecord('Subscriptions')}>Subscriptions</button>
//       <button onClick={() => classifyRecord('Utilities')}>Utilities</button>
//     </div>
//   );
// }

// export default Categories;
