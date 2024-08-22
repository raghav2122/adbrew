import React, { useState } from 'react';

export const TodoForm = () => {
    const [todo, setTodo] = useState(''); // Initialize as an empty string

    const handleSubmit = (event) => {
        event.preventDefault();
        fetch('http://localhost:8000/todos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title: todo, completed: false }), // Send title and completed status
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            setTodo(''); // Clear the input field after submission
            window.location.reload(); // Reload the page after submission
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={todo}
                onChange={e => setTodo(e.target.value)}
                placeholder="Enter todo title"
            />
            <button type="submit">Add Todo</button>
        </form>
    );
};
