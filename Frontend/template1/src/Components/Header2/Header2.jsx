// Header.jsx
import React, { useState, useContext, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Header2.css";
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
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showAccountMenu, setShowAccountMenu] = useState(false);
  const { editMode, toggleEditMode } = useEditMode();

  const handleClick = (item) => {
    setSidebarOpen(false);
    setShowAccountMenu(false);
    if (item === "Home") {
      navigate("/");
    } else {
      navigate(`/${item.replace(" ", "")}`);
    }
  };

  // Add the notifications navigation function
  const handleNotificationsClick = () => {
    navigate("/Account?section=notifications");
    setShowAccountMenu(false);
  };

  useEffect(() => {
    if (!isLoggedIn && location.pathname === "/Account") {
      navigate("/");
    }
  }, [isLoggedIn, location.pathname]);

  // Close sidebar when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      const sidebar = document.getElementById("sidebar");
      const hamburger = document.getElementById("hamburger-button");

      if (
        sidebar &&
        !sidebar.contains(event.target) &&
        hamburger &&
        !hamburger.contains(event.target)
      ) {
        setSidebarOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  // Prevent body scrolling when sidebar is open
  useEffect(() => {
    if (sidebarOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "auto";
    }

    return () => {
      document.body.style.overflow = "auto";
    };
  }, [sidebarOpen]);

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
      const token = credentialResponse.credential;
      const success = await login(token);
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
    <>
      <header className="header2">
        <div className="header__logo-container" onClick={() => navigate("/")}>
          <img className="header__logo" src={props.logo} alt="logo" />
          <h1 className="header__title">{props.title}</h1>
        </div>

        <div className="header__actions">
          {isLoggedIn && (
            <div className="edit-mode-toggle">
              <span className="edit-mode-label">Edit Mode</span>
              <label className="switch">
                <input
                  type="checkbox"
                  checked={editMode}
                  onChange={toggleEditMode}
                />
                <span className="slider"></span>
              </label>
            </div>
          )}

          <div className="account-menu">
            <button
              className="account-button"
              onClick={() => setShowAccountMenu(!showAccountMenu)}
            >
              <img src={accountIcon} alt="Account" />
              {isLoggedIn &&
                hasNewNotifications &&
                notifications.length !== 0 && (
                  <span className="notification-dot"></span>
                )}
            </button>

            {showAccountMenu && (
              <div className="account-dropdown">
                {isLoggedIn ? (
                  <>
                    <button
                      onClick={() => {
                        navigate("Account");
                        setShowAccountMenu(false);
                      }}
                    >
                      My Account
                    </button>
                    <button onClick={handleNotificationsClick}>
                      Notifications
                      {hasNewNotifications && notifications.length !== 0 && (
                        <span className="notification-indicator" />
                      )}
                    </button>
                    <button
                      onClick={() => {
                        handleLogout();
                        setShowAccountMenu(false);
                      }}
                    >
                      Logout
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => {
                      setShowLogin(true);
                      setShowAccountMenu(false);
                    }}
                  >
                    Login
                  </button>
                )}
              </div>
            )}
          </div>

          <button
            id="hamburger-button"
            className={`hamburger-menu ${sidebarOpen ? "active" : ""}`}
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </header>

      {/* Sidebar Navigation */}
      <div
        className={`sidebar-overlay-header ${sidebarOpen ? "active" : ""}`}
        onClick={() => setSidebarOpen(false)}
      ></div>

      <nav
        id="sidebar-header"
        className={`sidebar-header ${sidebarOpen ? "open" : ""}`}
      >
        <div className="sidebar__header">
          <h2>Menu</h2>
          <button
            className="close-sidebar"
            onClick={() => setSidebarOpen(false)}
          >
            ×
          </button>
        </div>

        <div className="sidebar__content">
          {props.components
            .filter((item) => item !== "About Us")
            .map((item, index) => (
              <button
                key={index}
                onClick={() => handleClick(item)}
                className="sidebar__nav-item"
              >
                {item}
              </button>
            ))}
        </div>

        {isLoggedIn && (
          <div className="sidebar__footer">
            <div className="sidebar__edit-mode">
              <span>Edit Mode</span>
              <label className="switch">
                <input
                  type="checkbox"
                  checked={editMode}
                  onChange={toggleEditMode}
                />
                <span className="slider"></span>
              </label>
            </div>
          </div>
        )}
      </nav>

      {/* Login Modal */}
      {showLogin && (
        <div className="login-overlay">
          <div className="login-modal">
            <button className="close-modal" onClick={() => setShowLogin(false)}>
              ×
            </button>
            <h2>Welcome Back</h2>
            <p>Enter your email to log in</p>
            {/* <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            /> */}
            {loginError && (
              <div className="login-error">
                This email does not exist. Request sent to manager
              </div>
            )}
            <div className="google-login-container">
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={() => {
                  setLoginError(true);
                  console.log("Login Failed");
                }}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Header;
