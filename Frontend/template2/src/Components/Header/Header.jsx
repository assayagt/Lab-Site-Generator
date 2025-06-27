import React, { useState, useContext, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Navbar, Container, Nav, Button, Form, Offcanvas, Badge } from 'react-bootstrap';
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
  const [showAccountMenu, setShowAccountMenu] = useState(false);
  const { editMode, toggleEditMode } = useEditMode();

  const handleClick = (item) => {
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
    <Navbar bg="light" expand="lg" className="shadow-sm">
      <Container>
        <Navbar.Brand href="/" className="d-flex align-items-center">
          <img
            src={props.logo}
            alt="logo"
            height="40"
            className="me-2"
          />
          <span className="fw-bold">{props.title}</span>
        </Navbar.Brand>

        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            {props.components
              .filter((item) => item !== "About Us")
              .map((item, index) => (
                <Nav.Link
                  key={index}
                  onClick={() => handleClick(item)}
                  className="text-dark"
                >
                  {item}
                </Nav.Link>
              ))}
          </Nav>

          <div className="d-flex align-items-center">
            {isLoggedIn && (
              <Form.Check
                type="switch"
                id="edit-mode-switch"
                label="Edit Mode"
                checked={editMode}
                onChange={toggleEditMode}
                className="me-3"
              />
            )}

            <div className="position-relative">
              <Button
                variant="outline-secondary"
                onClick={() => setShowAccountMenu(!showAccountMenu)}
                className="d-flex align-items-center"
              >
                <img
                  src={accountIcon}
                  alt="account"
                  height="24"
                  className="me-2"
                />
                {isLoggedIn && hasNewNotifications && notifications.length !== 0 && (
                  <Badge bg="danger" className="position-absolute top-0 start-100 translate-middle">
                    {notifications.length}
                  </Badge>
                )}
              </Button>

              {showAccountMenu && (
                <div className="position-absolute end-0 mt-2 bg-white shadow rounded p-3" style={{ zIndex: 1000 }}>
                  {isLoggedIn ? (
                    <>
                      <Button
                        variant="outline-primary"
                        className="w-100 mb-2"
                        onClick={() => {
                          navigate("Account");
                          setShowAccountMenu(false);
                        }}
                      >
                        My Account
                      </Button>
                      <Button
                        variant="outline-danger"
                        className="w-100"
                        onClick={() => {
                          handleLogout();
                          setShowAccountMenu(false);
                        }}
                      >
                        Logout
                      </Button>
                    </>
                  ) : (
                    <div className="p-2">
                      <GoogleLogin
                        onSuccess={handleGoogleSuccess}
                        onError={() => setLoginError(true)}
                        useOneTap
                      />
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;
