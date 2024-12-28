import logo from './logo.svg';
import './App.css';
import Header from "./Header/Header"



function App() {

  const components = [
    "Home",
    "Participants",
    "Contact Us",
    "Publications"
  ];
  return (
    <div className="App">
      <div>
        <Header components={components} title="SPL"></Header>
        <div>Welcome to our lab website. </div>
      </div>
    </div>
  );
}

export default App;
