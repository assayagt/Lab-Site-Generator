import './App.css';
import HomePage from './Pages/HomePage/HomePage';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'; // Import Routes, Navigate
import ParticipantsPage from "./Pages/ParticipantsPage/ParticipantsPage"
import Header from './Components/Header/Header';

function App() {

  const components = [
    "Home",
    "Participants",
    "Contact Us",
    "Publications"
  ];
  return (
    <Router>
            <Header components={components} title="SPL"></Header>
            <Routes>
              <Route path="/" element={<HomePage/>} />
              <Route
                path="/Participants"
                element= {<ParticipantsPage />}
              />
              {/* <Route
                path="/upload-files"
                element={<UploadFilesPage />}
              /> */}
            </Routes>
    </Router>

    
  );
}

export default App;
