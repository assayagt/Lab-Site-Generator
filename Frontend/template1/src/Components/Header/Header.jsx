import React, { useState, useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Header.css";
import accountIcon from "../../images/account_avatar.svg";
import { useAuth } from "../../Context/AuthContext";
import { NotificationContext } from "../../Context/NotificationContext";
import { useEditMode } from "../../Context/EditModeContext";

function Header(props) {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, logout } = useAuth();
  const { hasNewNotifications } = useContext(NotificationContext);
  const [showLogin, setShowLogin] = useState(false);
  const [email, setEmail] = useState("");
  const [loginError, setLoginError] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(
    sessionStorage.getItem("isLoggedIn")
  );
  const [isNavbarExpanded, setIsNavbarExpanded] = useState(false); // Track expansion
  const { editMode, toggleEditMode } = useEditMode(); // 🔹 Get Edit Mode state from context

  const handleClick = (item) => {
    if (item === "Home") {
      navigate("/");
    } else {
      navigate(`/${item.replace(" ", "")}`);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    let data = await login(email);
    if (data) {
      setShowLogin(false);
      setLoginError("");
      setIsLoggedIn(true);
    } else {
      setIsLoggedIn(false);
      setShowLogin(true);
      setLoginError("Login failed. Please check your username.");
    }
    setEmail("");
  };

  const handleLogout = () => {
    let ans = logout();
    if (ans) {
      sessionStorage.removeItem("isLoggedIn");
      sessionStorage.removeItem("userEmail");
      setIsLoggedIn(false);
      location.pathname === "/Account"
        ? navigate("/")
        : window.location.reload();
    }
  };

  return (
    <div className="header">
      {/* Logo & Title */}
      <img
        className="header_logo"
        src={props.logo}
        alt="logo"
        onClick={() => navigate("/")}
      />
      <div className="header_title" onClick={() => navigate("/")}>
        {props.title}
      </div>

      {/* Navbar - Expands on Hover */}
      <div
        className={`navbar ${isNavbarExpanded ? "expanded" : ""}`}
        onMouseEnter={() => setIsNavbarExpanded(true)}
        onMouseLeave={() => setIsNavbarExpanded(false)}
      >
        {props.components
          .filter((item) => item !== "About Us")
          .map((item, index, filteredArray) => (
            <div className="navbar-item" key={index}>
              <button
                onClick={() => handleClick(item)}
                className="navbar-item-button"
              >
                {item}
              </button>
              {index !== filteredArray.length - 1 && (
                <div className="line-nav">|</div>
              )}
            </div>
          ))}
      </div>

      {/* Profile Menu */}
      <div className="icon_photo">
        <div className="menu">
          {hasNewNotifications && <div className="notification-dot"></div>}

          <div className="hidden-box">
            <div className="personal_menu">
              <div className="icon_photo">
                <img src={accountIcon} alt="icon" />
              </div>
              <hr className="hr_line" />
              {/* 🔹 ADD THIS TOGGLE SWITCH */}
              {isLoggedIn && (
                <div className="edit-mode-toggle">
                  <label className="switch">
                    <input
                      type="checkbox"
                      checked={editMode}
                      onChange={toggleEditMode}
                    />
                    <span className="slider round"></span>
                  </label>
                </div>
              )}
              {isLoggedIn ? (
                <div className="choose_item">
                  <button
                    className="my_sites_button"
                    onClick={() => navigate("Account")}
                  >
                    My Account
                  </button>
                  <button className="logout_button" onClick={handleLogout}>
                    Logout
                  </button>
                </div>
              ) : (
                <div className="choose_item">
                  <button
                    className="login_button"
                    onClick={() => setShowLogin(true)}
                  >
                    Login
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Login Popup */}
      {showLogin && (
        <div className="login-modal">
          <div className="login-content">
            <div className="close-button" onClick={() => setShowLogin(false)}>
              X
            </div>
            <h2>Login</h2>
            {loginError && <div className="login-error">{loginError}</div>}
            <form onSubmit={handleLogin}>
              <input
                type="text"
                placeholder="Username"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <button type="submit">Login</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Header;
