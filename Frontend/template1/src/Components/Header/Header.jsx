import React, { useState, useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Header.css";
import accountIcon from "../../images/account_avatar.svg";
import { useAuth } from "../../Context/AuthContext";
import { NotificationContext } from "../../Context/NotificationContext";
import { useEditMode } from "../../Context/EditModeContext";
import { fetchUserNotifications } from "../../services/UserService";

function Header(props) {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, logout } = useAuth();
  const { hasNewNotifications, updateNotifications, notifications } =
    useContext(NotificationContext);
  const [showLogin, setShowLogin] = useState(false);
  const [email, setEmail] = useState("");
  const [loginError, setLoginError] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(() => {
    return sessionStorage.getItem("isLoggedIn") === "true" ? true : false;
  });
  const [isNavbarExpanded, setIsNavbarExpanded] = useState(false);
  const { editMode, toggleEditMode } = useEditMode();
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
      const notifications = await fetchUserNotifications(email);
      console.log(notifications);
      updateNotifications(notifications);
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
      <div className="header_title_name">
        <img
          className="header_logo"
          src={props.logo}
          alt="logo"
          onClick={() => navigate("/")}
        />
        <div className="header_title" onClick={() => navigate("/")}>
          {props.title}
        </div>
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

      <div className="icon_photo">
        {isLoggedIn && (
          <div className="edit-mode-container">
            <span className="edit-mode-label">Edit Mode</span>
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
        <div className="menu">
          {isLoggedIn && hasNewNotifications && notifications.length !== 0 && (
            <div className="notification-dot"></div>
          )}

          <div className="hidden-box">
            <div className="personal_menu">
              <div className="icon_photo2">
                <img src={accountIcon} alt="icon" />
              </div>
              <hr className="hr_line" />

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
        // <div className="login-modal">
        //   <div className="login-content">
        //     <div className="close-button" onClick={() => setShowLogin(false)}>
        //       X
        //     </div>
        //     <h2>Login</h2>
        //     {loginError && <div className="login-error">{loginError}</div>}
        //     <form onSubmit={handleLogin}>
        //       <input
        //         type="text"
        //         placeholder="Username"
        //         value={email}
        //         onChange={(e) => setEmail(e.target.value)}
        //       />
        //       <button type="submit">Login</button>
        //     </form>
        //   </div>
        // </div>
        <div className="login-popup-overlay">
          <div className="login-popup">
            <button className="close-popup" onClick={() => setShowLogin(false)}>
              ×
            </button>
            <h2 className="login-title">Welcome Back</h2>
            <p className="login-subtitle">Enter your email to log in</p>

            <input
              className="login-input"
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            {loginError && (
              <div className="login-error">
                This email does not exist. Request sent to manager
              </div>
            )}

            <button className="login-button" onClick={handleLogin}>
              Login
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Header;
