import React, { useState } from 'react';
import { useAuth } from '../../Context/AuthContext'; // Assuming you have this context
import './LoginPopup.css'; // Add necessary styles

const LoginPopup = ({ onClose }) => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState(false);
  const { login } = useAuth();  // Access the login function from context

  const handleLogin = async () => {
    if (email) {
      try {
        let data = await login(email); // Await the login function to get the result
        
        if (data === false) {
          setError(true);
        } else {
        
          setError(false);
          onClose();  
          
        }
      } catch (err) {
        console.error("Login error:", err);
        setError(true); 
      }
    } else {
      setError(true); 
    }
  };

  return (
    <div className="login-popup-overlay">
      <div className="login-popup">
        <button className="close-popup" onClick={onClose}>X</button>
        <h3>Login</h3>
        <div className={error?"error":"no_error"}>Wrong email, please try again</div>
        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <button onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
};

export default LoginPopup;
