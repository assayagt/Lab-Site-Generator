import React, { useState } from 'react';
import { useAuth } from '../../Context/AuthContext'; // Assuming you have this context
import './LoginPopup.css'; // Add necessary styles

const LoginPopup = ({ onClose }) => {
  const [email, setEmail] = useState('');
  const { login } = useAuth();  // Access the login function from context

  const handleLogin = () => {
    if (email) {
      let data = login(email); 
      if(data === false) {
        //todo: show error message
      }
      else{
        onClose();  
      }
    } else {
      alert('Please enter a valid email.');
    }
  };

  return (
    <div className="login-popup-overlay">
      <div className="login-popup">
        <button className="close-popup" onClick={onClose}>X</button>
        <h3>Login</h3>
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
