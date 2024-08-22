import React, { useState, useEffect } from 'react';

export const TodoList = () => {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/todos/')
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          setTodos(data);
        } else {
          console.error('Unexpected data format:', data);
        }
      })
      .catch(error => {
        console.error('Error fetching todos:', error);
      });
  }, []);

  const handleComplete = (id, completed) => {
    fetch(`http://localhost:8000/todos/${id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ completed: !completed }),
    })
    .then(response => response.json())
    .then(data => {
      setTodos(todos.map(todo => (todo._id === id ? { ...todo, completed: data.completed } : todo)));
    })
    .catch(error => {
      console.error('Error updating todo:', error);
    });
  };

  const handleDelete = (id) => {
    fetch(`http://localhost:8000/todos/${id}/`, {
      method: 'DELETE',
    })
    .then(() => {
      setTodos(todos.filter(todo => todo._id !== id));
    })
    .catch(error => {
      console.error('Error deleting todo:', error);
    });
  };

  return (
    <ul>
      {todos.map(todo => (
        <li key={todo._id}>
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => handleComplete(todo._id, todo.completed)}
          />
          {todo.title}
          <button onClick={() => handleDelete(todo._id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};
