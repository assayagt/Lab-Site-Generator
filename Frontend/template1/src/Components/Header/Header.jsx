import React, { useState, useContext, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Header.css";
import accountIcon from "../../images/account_avatar.svg";
import { useAuth } from "../../Context/AuthContext";
import { NotificationContext } from "../../Context/NotificationContext";
import { useEditMode } from "../../Context/EditModeContext";
import { fetchUserNotifications } from "../../services/UserService";
import { GoogleLogin } from "@react-oauth/google";

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
    return sessionStorage.getItem("isLoggedIn") === "true";
  });
  const [isNavbarExpanded, setIsNavbarExpanded] = useState(false);
  const [showAccountMenu, setShowAccountMenu] = useState(false);
  const { editMode, toggleEditMode } = useEditMode();

  const handleClick = (item) => {
    setIsNavbarExpanded(false);
    setShowAccountMenu(false);
    if (item === "Home") {
      navigate("/");
    } else {
      navigate(`/${item.replace(" ", "")}`);
    }
  };
  useEffect(() => {
    if (!isLoggedIn && location.pathname === "/Account") {
      navigate("/");
    }
  }, [isLoggedIn, location.pathname]);

  const handleLogin = async (e) => {
    e.preventDefault();
    let data = await login(email);
    if (data) {
      setShowLogin(false);
      setLoginError("");
      setIsLoggedIn(true);
      const notifications = await fetchUserNotifications(email);
      updateNotifications(notifications);
    } else {
      setIsLoggedIn(false);
      setShowLogin(true);
      setLoginError("Login failed. Please check your username.");
    }
    setEmail("");
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const token = credentialResponse.credential; // ✅ SEND THE RAW TOKEN

      // const email = decoded.email;

      const success = await login(token); // This still hits your backend
      if (success) {
        setShowLogin(false);
        setLoginError("");
        setIsLoggedIn(true);
        const notifications = await fetchUserNotifications(email);
        updateNotifications(notifications);
      } else {
        setLoginError(true);
      }
    } catch (err) {
      console.error("Google login error:", err);
      setLoginError(true);
    }
  };
  const handleLogout = () => {
    const success = logout();
    if (success) {
      sessionStorage.removeItem("isLoggedIn");
      sessionStorage.removeItem("userEmail");
      setIsLoggedIn(false);
      if (editMode) {
        toggleEditMode();
      }
      location.pathname === "/Account" ? navigate("/") : navigate("/");
    }
  };

  return (
    <div className="header">
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

      <div className={`navbar ${isNavbarExpanded ? "expanded" : ""}`}>
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
        <button
          className="hamburger-menu"
          onClick={() => {
            setIsNavbarExpanded((prev) => !prev);
            setShowAccountMenu(false);
          }}
        >
          <span />
          <span />
          <span />
        </button>

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

        <div
          className="menu"
          onClick={() => {
            setShowAccountMenu((prev) => !prev);
            setIsNavbarExpanded(false);
          }}
        >
          {isLoggedIn && hasNewNotifications && notifications.length !== 0 && (
            <div className="notification-dot"></div>
          )}

          {showAccountMenu && (
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
                      onClick={() => {
                        navigate("Account");
                        setShowAccountMenu(false);
                      }}
                    >
                      My Account
                    </button>
                    <button
                      className="logout_button"
                      onClick={() => {
                        handleLogout();
                        setShowAccountMenu(false);
                      }}
                    >
                      Logout
                    </button>
                  </div>
                ) : (
                  <div className="choose_item">
                    <button
                      className="login_button"
                      onClick={() => {
                        setShowLogin(true);
                        setShowAccountMenu(false);
                      }}
                    >
                      Login
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {showLogin && (
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
            {/* <button className="login-button" onClick={handleLogin}>
              Login
            </button> */}
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() => {
                setLoginError(true);
                console.log("Login Failed");
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default Header;
