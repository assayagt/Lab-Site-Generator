import React, { useState, useContext, useEffect, useRef } from "react";
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
  const { login, logout, fetchToken } = useAuth();
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

  // Create refs for the menu and navbar
  const accountMenuRef = useRef(null);
  const navbarRef = useRef(null);
  const hamburgerRef = useRef(null);

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

  // Add click outside listener to close menus
  useEffect(() => {
    function handleClickOutside(event) {
      // Close account menu if click is outside
      if (
        accountMenuRef.current &&
        !accountMenuRef.current.contains(event.target) &&
        showAccountMenu
      ) {
        setShowAccountMenu(false);
      }

      // Close navbar if click is outside (for mobile)
      if (
        navbarRef.current &&
        !navbarRef.current.contains(event.target) &&
        !hamburgerRef.current.contains(event.target) &&
        isNavbarExpanded
      ) {
        setIsNavbarExpanded(false);
      }
    }

    // Add event listener
    document.addEventListener("mousedown", handleClickOutside);

    // Clean up
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [showAccountMenu, isNavbarExpanded]);

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

      <div
        ref={navbarRef}
        className={`navbar ${isNavbarExpanded ? "expanded" : ""}`}
      >
        {props.components
          .filter((item) => item !== "About Us")
          .map((item, index, filteredArray) => (
            <div className="navbar-item" key={index}>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleClick(item);
                }}
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
          ref={hamburgerRef}
          className="hamburger-menu-1"
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
          ref={accountMenuRef}
          className={`menu ${showAccountMenu ? "active" : ""}`}
          onClick={(e) => {
            e.stopPropagation();
            setShowAccountMenu((prev) => !prev);
            setIsNavbarExpanded(false);
          }}
        >
          {isLoggedIn && hasNewNotifications && notifications.length !== 0 && (
            <div className="notification-dot"></div>
          )}

          {showAccountMenu && (
            <div
              className="hidden-box"
              onClick={(e) => e.stopPropagation()} // Prevent clicks inside menu from closing it
            >
              <div className="personal_menu">
                <div className="icon_photo2">
                  <img src={accountIcon} alt="icon" />
                </div>
                <hr className="hr_line" />

                {isLoggedIn ? (
                  <div className="choose_item">
                    <button
                      className="my_sites_button"
                      onClick={(e) => {
                        e.stopPropagation();
                        navigate("Account");
                        setShowAccountMenu(false);
                      }}
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
                      className="notifications_button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleNavigation();
                        setShowAccountMenu(false);
                      }}
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
                        <span
                          style={{
                            marginLeft: "8px",
                            fontSize: "12px",
                            backgroundColor: "#e74c3c",
                            color: "white",
                            padding: "2px 6px",
                            borderRadius: "12px",
                          }}
                        >
                          {notifications.length}
                        </span>
                      )}
                    </button>
                    <button
                      className="logout_button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleLogout();
                        setShowAccountMenu(false);
                      }}
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
                  <div className="choose_item">
                    <button
                      className="login_button"
                      onClick={(e) => {
                        e.stopPropagation();
                        if (sessionStorage.getItem("sid") === null) {
                          fetchToken();
                        }
                        setShowLogin(true);
                        setShowAccountMenu(false);
                      }}
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
            </div>
          )}
        </div>
      </div>

      {showLogin && (
        <div
          className="login-popup-overlay"
          onClick={(e) => {
            // Close login popup when clicking outside
            if (e.target.className === "login-popup-overlay") {
              setShowLogin(false);
            }
          }}
        >
          <div className="login-popup">
            <button className="close-popup" onClick={() => setShowLogin(false)}>
              ×
            </button>
            <h2 className="login-title">Welcome Back</h2>
            <p className="login-subtitle">Enter your email to log in</p>
            {loginError && (
              <div className="login-error">
                This email does not exist. Request sent to manager
              </div>
            )}
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
      )}
    </div>
  );
}

export default Header;
