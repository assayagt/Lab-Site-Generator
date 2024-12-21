import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'; // Import Routes, Navigate
import WelcomePage from './pages/WelcomePage/WelcomePage';
import ChooseComponentsPage from './pages/Generate/ChooseComponentsPage/ChooseComponentsPage';
import UploadFilesPage from './pages/Generate/UploadFilesPage/UploadFilesPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <Routes>
        {/* Use the new "Routes" component for defining your routes */}
        <Route path="/" element={<WelcomePage onLogin={handleLogin} />} />
        <Route
          path="/choose-components"
          element={isLoggedIn ? <ChooseComponentsPage /> : <Navigate to="/" />}
        />
        <Route
          path="/upload-files"
          element={isLoggedIn ? <UploadFilesPage /> : <Navigate to="/" />}
        />
        {/* <Route
          path="/generate-website"
          element={isLoggedIn ? <GenerateWebsitePage /> : <Navigate to="/" />}
        /> */}
      </Routes>
    </Router>
  );
}

export default App;
