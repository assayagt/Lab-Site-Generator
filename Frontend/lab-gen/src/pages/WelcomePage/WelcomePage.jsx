import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Use useNavigate instead of useHistory

const WelcomePage = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  const navigate = useNavigate(); // Use useNavigate

  const handleStartClick = () => {
    if (!email || !password) {
      setShowLoginPopup(true); // Show login if not logged in
    } else {
      navigate('/choose-components'); // Navigate to next page if logged in
    }
  };

  const handleLoginClick = () => {
    if (email === 'test@example.com' && password === 'password123') {
      onLogin(); // Pass login state to App.js
      setShowLoginPopup(false); // Close login popup
      navigate('/choose-components'); // Redirect to next page
    } else {
      alert('Invalid credentials');
    }
  };

  const handleRegisterClick = () => {
    alert('Registered successfully!');
  };

  return (
    <div>
      <header>
        <button onClick={handleLoginClick}>Login</button>
        <button onClick={handleRegisterClick}>Register</button>
      </header>
      <main>
        <h1>Welcome to Website Generator</h1>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button onClick={handleStartClick}>Let's Start</button>
      </main>

      {showLoginPopup && (
        <div className="login-popup">
          <div className="popup-content">
            <h3>Login</h3>
            <div>
              <label>Email:</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label>Password:</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button onClick={handleLoginClick}>Login</button>
            <button onClick={() => setShowLoginPopup(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default WelcomePage;
