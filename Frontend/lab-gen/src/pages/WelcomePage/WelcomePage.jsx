import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header/Header';
import "./WelcomePage.css";
import { useAuth } from '../../Context/AuthContext';
import LoginPopup from '../../components/Popups/LoginPopup'; 

const WelcomePage = () => {
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  const [showErrorPopup, setShowErrorPopup] = useState(false);  
  const [errorMessage, setErrorMessage] = useState('');

  const navigate = useNavigate();
  const { fetchToken } = useAuth();

  // useEffect to check sessionStorage and fetch token if neede
    function fetchData() {
      const storedSid = sessionStorage.getItem('sid');
      if (!storedSid) {
        fetchToken();  
      }    
    }

  
  const handleStartClick = () => {
    if (!sessionStorage.getItem('isLoggedIn')) {
      setShowLoginPopup(true); 
    } else {
      navigate('/choose-components');
    }
  };

  const handleErrorPopupClose = () => {
    setShowErrorPopup(false);  
  };


  return (
    <div>
      {fetchData()}
      <div className='landing-container'>
      <main className='main-section'>
        <div className='text-content'>
          <h1>Your research website should do more than exist</h1>
          <p>
            Effortlessly create and maintain a professional website for your lab or research group. Our platform is easy to use, updates automatically, and requires minimal maintenance.
          </p>
          <button className='start-button' onClick={handleStartClick}>Start Building</button>
        </div>
      </main>
      {showLoginPopup && <LoginPopup onClose={() => setShowLoginPopup(false)} />}
      {showErrorPopup && (
        <div className='error-popup-overlay'>
          <div className='error-popup'>
            <button className='close-popup' onClick={handleErrorPopupClose}>X</button>
            <h3>Error</h3>
            <p>{errorMessage}</p>
          </div>
        </div>
      )}
    </div>
    </div>
  );
};

export default WelcomePage;
