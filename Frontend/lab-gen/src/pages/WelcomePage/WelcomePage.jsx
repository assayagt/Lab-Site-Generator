import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header/Header';
import "./WelcomePage.css";
import { useAuth } from '../../Context/AuthContext';
import LoginPopup from '../../components/Popups/LoginPopup'; 
import FeatureCarousel from './FeatureCarousel';  // Import FeatureCarousel component

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

  const features = [
    <div>
      <h3>Easy Setup</h3>
      <p>Choose a template, select the components, and provide details about your lab and research.</p>
    </div>,
    <div>
      <h3>Fully Customizable</h3>
      <p>Add images, videos, documents, and more to make your site truly reflect your lab's unique identity.</p>
    </div>,
    <div>
      <h3>Live Preview</h3>
      <p>View your site as you build it to ensure it meets your expectations before you generate it.</p>
    </div>
  ];

  return (
    <div>
      {fetchData()}
      <main className='main_section'>
        <h1>Welcome to Website Generator</h1>

        <div className="welcome-body">
          <p className="intro-text">
            This tool allows you to effortlessly create custom websites for your lab
            or research group.<br/> Whether you're a professor, researcher, or student,<br/> our platform makes it easy to generate a professional-looking website<br/> with just a few clicks.
          </p>
          
          {/* Feature Carousel */}
          <div className="features">
            <h2>Product Highlights:</h2>
            <FeatureCarousel features={features} />
          </div>

          <div className="cta">
            <h3>Ready to get started?</h3>
            <p>Simply log in or sign up to begin creating your personalized lab website.</p>
          </div>
          <button className='start_button' onClick={handleStartClick}>Let's Start</button>
        </div>
      </main>

      {showLoginPopup && <LoginPopup onClose={() => setShowLoginPopup(false)} />}

      {/* Error Popup for Invalid Credentials */}
      {showErrorPopup && (
        <div className="error-popup-overlay">
          <div className="error-popup">
            <button className="close-popup" onClick={handleErrorPopupClose}>X</button>
            <h3>Error</h3>
            <p>{errorMessage}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default WelcomePage;
