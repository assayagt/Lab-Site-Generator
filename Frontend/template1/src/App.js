import './App.css';
import HomePage from './Pages/HomePage/HomePage';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'; // Import Routes, Navigate
import ParticipantsPage from "./Pages/ParticipantsPage/ParticipantsPage"
import ContactUsPage from './Pages/ContactUsPage/ContactUsPage';
import Header from './Components/Header/Header';
import AccountPage from './Pages/AccountPage/AccountPage';
import PublicationsPage from './Pages/PublicationsPage/PublicationsPage';
import publications from "./publications.json"
import { AuthProvider } from './Context/AuthContext';
function App() {

  const components = [
    "Home",
    "Participants",
    "Publications",
    "Contact Us"
  ];

  

  return (
    <AuthProvider>
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
                element= {<ContactUsPage address = "Ben Gurion University of the Negev" email ="roni@bgu.ac.il" phone="+972 523456789"/>}
              />
           <Route
                path="/Account"
                element= {<AccountPage/>}
              />
              <Route
                path="/Publications"
                element= {<PublicationsPage publications={publications}/>}
              />
            </Routes>
    </Router>
    </AuthProvider>
    

    
  );
}

export default App;
