import React, { useState } from "react";
import logoIcon from "../../images/launcher.svg";
import "./Header.css";
import { useAuth } from "../../Context/AuthContext";

function Header(props) {
  const { isLoggedIn, userEmail, login, logout } = useAuth();
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  const [email, setEmail] = useState('');  // Email state for the popup

  const handleLogin = () => {
    setShowLoginPopup(true);  
  };

  const login_user = () => {
    login(email);  
    setShowLoginPopup(false);  
  };

  const handleLogout = () => {
    logout();  
  };

  return (
    <div className="header">
      <img alt="Logo" src={logoIcon} className="img_logo" />
      <h1>{props.title}</h1>
      <div className="menu">
        <div className="hidden-box">
          <div className="personal_menu">
            <div className="icon_photo"></div>
            <hr className="hr_line" />
            <div className="choose item">
              {isLoggedIn ? (
                <button onClick={handleLogout}>Logout</button>
              ) : (
                <button onClick={handleLogin}>Login</button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Conditional rendering of the login popup */}
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
            <button onClick={login_user}>Login</button>
          </div>
        </div>
      )}
    </div>
  );
}
export default Header;
