import React, { useEffect, useState } from "react";
import axios from "axios";
import { DragDropContext, Draggable, Droppable } from "react-beautiful-dnd";

function App() {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const result = await axios.get("http://localhost:5000/get_record");
      setTransactions(result.data);
    }

    fetchData();
  }, []);

  function handleDragEnd(result) {
    if (!result.destination) return;

    const newTransactions = Array.from(transactions);
    const [movedTransaction] = newTransactions.splice(result.source.index, 1);
    newTransactions.splice(result.destination.index, 0, movedTransaction);

    setTransactions(newTransactions);
    // Here, you might make another API call to update the data in your backend.
  }

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <Droppable droppableId="droppable">
        {(provided) => (
          <div ref={provided.innerRef} {...provided.droppableProps}>
            {transactions.map((transaction, index) => (
              <Draggable key={transaction.id} draggableId={transaction.id} index={index}>
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                  >
                    {/* Your transaction display goes here */}
                    <span>{transaction.name}</span>
                  </div>
                )}
              </Draggable>
            ))}
            {provided.placeholder}
          </div>
        )}
      </Droppable>
    </DragDropContext>
  );
}

export default App;
