import logo from './logo.svg';
import './App.css';
import Header from "./Header/Header"



function App() {

  const components = [
    "Home",
    "About",
    "Services",
    "Contact",
    "Publications"
  ];
  return (
    <div className="App">
     <Header components={components} ></Header>
    </div>
  );
}

export default App;
