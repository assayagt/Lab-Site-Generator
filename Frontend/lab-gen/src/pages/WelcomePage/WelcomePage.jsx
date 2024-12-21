import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

const WelcomePage = ({ onLogin, isLoggedIn }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showLoginPopup, setShowLoginPopup] = useState(false); // Manage the popup visibility
  const history = useHistory();

  const handleStartClick = () => {
    // If the user is not logged in, show the login popup
    if (!isLoggedIn) {
      setShowLoginPopup(true);
    } else {
      history.push('/choose-components');
    }
  };

  const handleLoginClick = () => {
    // Simulate login logic
    if (email === 'test@example.com' && password === 'password123') {
      onLogin(); // Update the parent component with the login state
      setShowLoginPopup(false); // Close the popup
      history.push('/choose-components'); // Redirect to next page after login
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
