import './App.css';
import { TodoForm } from './addTODO';
import { TodoList } from './displayTODO';
import logo from './logo.svg';


export function App() {
  return (
    <div className="App">
      <div>
        <h1>Create a ToDo</h1>
        <TodoForm />
      </div>
      <div>
        <TodoList />
      </div>
    </div>
  );
}

export default App;
