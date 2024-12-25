import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'; // Import Routes, Navigate
import WelcomePage from './pages/WelcomePage/WelcomePage';
import ChooseComponentsPage from './pages/Generate/ChooseComponentsPage/ChooseComponentsPage';
import UploadFilesPage from './pages/Generate/UploadFilesPage/UploadFilesPage';
import { AuthProvider } from './Context/AuthContext';
import { WebsiteProvider
  
 } from './Context/WebsiteContext';
function App() {

  return (
    <AuthProvider>
       <WebsiteProvider>
       <Router>
            <Routes>
              {/* Use the new "Routes" component for defining your routes */}
              <Route path="/" element={<WelcomePage/>} />
              <Route
                path="/choose-components"
                element= {<ChooseComponentsPage />}
              />
              <Route
                path="/upload-files"
                element={<UploadFilesPage />}
              />
            </Routes>
          </Router>
       </WebsiteProvider>
      
    </AuthProvider>
    
  );
}

export default App;
