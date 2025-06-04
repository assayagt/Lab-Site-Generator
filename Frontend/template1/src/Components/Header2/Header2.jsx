import React, { useState, useContext, useEffect, useRef } from "react";
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
  const { login, logout, fetchToken } = useAuth();
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

  // Create refs for menu components
  const accountMenuRef = useRef(null);

  const handleClick = (item) => {
    setSidebarOpen(false);
    setShowAccountMenu(false);
    if (item === "Home") {
      navigate("/");
    } else {
      navigate(`/${item.replace(" ", "")}`);
    }
  };

  // Add the notifications navigation function from old header
  const handleNavigation = () => {
    // Create a custom event for section navigation
    const event = new CustomEvent("NAVIGATE_TO_SECTION", {
      detail: { section: "notifications" },
    });
    // If already on Account page, update URL and dispatch custom event
    if (location.pathname === "/Account") {
      navigate("/Account?section=notifications", { replace: true });
      // Dispatch the event to notify the Account component
      document.dispatchEvent(event);
    } else {
      // If not on Account page, just navigate normally
      navigate("/Account?section=notifications");
    }
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

      // Close account menu if click is outside
      if (
        accountMenuRef.current &&
        !accountMenuRef.current.contains(event.target) &&
        showAccountMenu
      ) {
        setShowAccountMenu(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showAccountMenu]);

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

          <div className="account-menu" ref={accountMenuRef}>
            <button
              className="account-button"
              onClick={(e) => {
                e.stopPropagation();
                setShowAccountMenu(!showAccountMenu);
                setSidebarOpen(false);
              }}
            >
              <img src={accountIcon} alt="Account" />
              {isLoggedIn &&
                hasNewNotifications &&
                notifications.length !== 0 && (
                  <span className="notification-dot"></span>
                )}
            </button>

            {showAccountMenu && (
              <div
                className="account-dropdown"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="dropdown-header">
                  <img
                    src={accountIcon}
                    alt="Account"
                    className="dropdown-avatar"
                  />
                </div>
                <div className="dropdown-divider"></div>
                {isLoggedIn ? (
                  <div className="dropdown-menu">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate("Account");
                        setShowAccountMenu(false);
                      }}
                      className="dropdown-item"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                      </svg>
                      My Account
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleNavigation();
                      }}
                      className="dropdown-item"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M22 17H2a3 3 0 0 0 3-3V9a7 7 0 0 1 14 0v5a3 3 0 0 0 3 3zm-8.27 4a2 2 0 0 1-3.46 0"></path>
                      </svg>
                      Notifications
                      {notifications && notifications.length > 0 && (
                        <span className="notification-badge">
                          {notifications.length}
                        </span>
                      )}
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleLogout();
                        setShowAccountMenu(false);
                      }}
                      className="dropdown-item"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                        <polyline points="16 17 21 12 16 7"></polyline>
                        <line x1="21" y1="12" x2="9" y2="12"></line>
                      </svg>
                      Logout
                    </button>
                  </div>
                ) : (
                  <div className="dropdown-menu">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        if (sessionStorage.getItem("sid") === null) {
                          fetchToken();
                        }
                        setShowLogin(true);
                        setShowAccountMenu(false);
                      }}
                      className="dropdown-item"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"></path>
                        <polyline points="10 17 15 12 10 7"></polyline>
                        <line x1="15" y1="12" x2="3" y2="12"></line>
                      </svg>
                      Login
                    </button>
                  </div>
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
        <div
          className="login-overlay"
          onClick={(e) => {
            if (e.target.className === "login-overlay") {
              setShowLogin(false);
            }
          }}
        >
          <div className="login-modal">
            <button className="close-modal" onClick={() => setShowLogin(false)}>
              ×
            </button>
            <h2>Welcome Back</h2>
            <p>Enter your email to log in</p>
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
                ux_mode="popup"
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default Header;
