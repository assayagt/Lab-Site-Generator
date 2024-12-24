import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header/Header';
import "./WelcomePage.css";
import { useAuth } from '../../Context/AuthContext';

const WelcomePage = () => {
  const [email, setEmail] = useState('');
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  const navigate = useNavigate();
  const {isLoggedIn, userEmail, login } = useAuth();

  const handleStartClick = () => {
    if (!isLoggedIn) {
      setShowLoginPopup(true); 
    } else {
      navigate('/choose-components');
    }
  };

  const handleLoginClick = () => {
    if (email === 'test@example.com') {
      login("test@example.com");
      setShowLoginPopup(false);
      navigate('/choose-components');
    } else {
      alert('Invalid credentials'); //TODO: change to popup
    }
  };

  
  return (
    <div>
      <Header title="LabLauncher"></Header>
      <main className='main_section'>
        <h1>Welcome to Website Generator</h1>
        <div className="welcome-body">
          <p className="intro-text">
            This tool allows you to effortlessly create custom websites for your lab
            or research group.<br /> Whether you're a professor, researcher, or student, our platform makes it easy to generate a professional-looking website<br /> with just a few clicks.
          </p>
          <div className="features">
            <h2>Features:</h2>
            <ul>
              <li><strong>Easy Setup:</strong> Choose a template, select the components, and provide details about your lab and research.</li>
              <li><strong>Fully Customizable:</strong> Add images, videos, documents, and more to make your site truly reflect your lab's unique identity.</li>
              <li><strong>Live Preview:</strong> View your site as you build it to ensure it meets your expectations before you generate it.</li>
            </ul>
          </div>
          <div className="cta">
            <h3>Ready to get started?</h3>
            <p>Simply log in or sign up to begin creating your personalized lab website.</p>
          </div>
          <button className='start_button' onClick={handleStartClick}>Let's Start</button>
        </div>
      </main>

      {/* Login Popup */}
      {showLoginPopup && (
        <div className="login-popup-overlay">
          <div className="login-popup">
            <button className="close-popup" onClick={() => setShowLoginPopup(false)}>X</button>
            <h3>Login</h3>
            <div>
              <label>Email:</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <button onClick={handleLoginClick}>Login</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default WelcomePage;
