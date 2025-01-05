import './App.css';
import HomePage from './Pages/HomePage/HomePage';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'; // Import Routes, Navigate
import ParticipantsPage from "./Pages/ParticipantsPage/ParticipantsPage"
import ContactUsPage from './Pages/ContactUsPage/ContactUsPage';
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
              <Route
                path="/ContactUs"
                element= {<ContactUsPage address = "Ben-Gurion University of the Negev, David Ben-Gurion Blvd. 1, Beer-Sheva 8410501 P.O Box 653." email ="roni@bgu.ac.il" phone="+972 523456789"/>}
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
