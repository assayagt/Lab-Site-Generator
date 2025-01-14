import React, { useRef, useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Header.css";
import Logo from "../../images/brain.svg";
import accountIcon from "../../images/account_avatar.svg";
import { useAuth } from "../../Context/AuthContext";

function Header(props) {
  const navbarRef = useRef(null);
  const navigate = useNavigate();
  const location = useLocation(); // Get current location
  const { login, logout } = useAuth();
  const [hasNotifications, setHasNotifications] = useState(false); // State for notifications
  const [showLogin, setShowLogin] = useState(false);
  const [email, setEmail] = useState("");
  const [loginError, setLoginError] = useState(""); // State to store login error messages

  let scrollAnimationFrame = null;

  const smoothScroll = (direction) => {
    const navbar = navbarRef.current;
    const scrollSpeed = 1;
    const maxScroll = navbar.scrollWidth - navbar.clientWidth;

    const scrollStep = () => {
      if (direction === "right") {
        if (navbar.scrollLeft < maxScroll) {
          navbar.scrollLeft += scrollSpeed;
          scrollAnimationFrame = requestAnimationFrame(scrollStep);
        }
      } else if (direction === "left") {
        if (navbar.scrollLeft > 0) {
          navbar.scrollLeft -= scrollSpeed;
          scrollAnimationFrame = requestAnimationFrame(scrollStep);
        }
      }
    };

    scrollStep();
  };

  const handleMouseEnter = (e) => {
    const { left, right } = navbarRef.current.getBoundingClientRect();
    const center = (left + right) / 2; // Calculate the center of the navbar
    const mouseX = e.clientX;

    if (mouseX <= center - 150) {
      smoothScroll("left");
    }
    if (mouseX >= center + 150) {
      smoothScroll("right");
    }
  };

  const handleClick = (item) => {
    if (item === "Home") {
      navigate("/");
    } else if (item === "Participants") {
      navigate("/Participants");
    } else if (item === "Contact Us") {
      navigate("/ContactUs");
    } else if (item === "Publications") {
      navigate("/Publications");
    }
  };

  const handleLoginClick = () => {
    console.log("Login clicked");
    setShowLogin(true); // Show login popup
  };

   const handleLogin = (e) => {
    //e.preventDefault();
    if (login(email)) {
      setShowLogin(false); 
      setLoginError(""); 
      //window.location.reload();
    } else {
      setLoginError("Login failed. Please check your username and try again."); 
    }
    setEmail("");
  };

  const handleLogout = () => {
    

    let ans = logout(); 
    if(ans){
       sessionStorage.removeItem("isLoggedIn");
       sessionStorage.removeItem("userEmail");

    if (location.pathname === "/Account") {
      // If user is currently on "/Account", navigate to "/"
      navigate("/");
    } else {
      // Otherwise, reload the page
      window.location.reload();
    }
    }
   
    console.log("Logout clicked");
    
  };

  return (
    <div className="header">
      <img className="header_logo" src={Logo} alt="logoItem" />
      <div className="header_title">{props.title}</div>
      <div className="navbar" ref={navbarRef} onMouseMove={handleMouseEnter}>
        {props.components
          .filter((item) => item !== "About Us")
          .map((item, index, filteredArray) => (
            <div className="navbar-item" key={item.id || index}>
              <button onClick={() => handleClick(item)} className="navbar-item-button">
                {item}
              </button>
              {index !== filteredArray.length - 1 && <div>|</div>}
            </div>
          ))}
      </div>
      <div className="icon_photo">
        <div className="menu">
          {hasNotifications && <div className="notification-dot"></div>}
          <div className="hidden-box">
            <div className="personal_menu">
              <div className="icon_photo">
                <img src={accountIcon} alt="icon" />
              </div>
              <hr className="hr_line" />
              {sessionStorage.getItem("isLoggedIn") ? (
                <div className="choose_item">
                  <button className="my_sites_button" onClick={() => navigate("Account")}>
                    My Account
                  </button>
                  <button className="logout_button" onClick={() => handleLogout()}>
                    Logout
                  </button>
                </div>
              ) : (
                <div className="choose_item">
                  <button className="login_button" onClick={handleLoginClick}>
                    Login
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {showLogin && (
        <div className="login-modal">
          <div className="login-content">
            <div className="close-button" onClick={() => setShowLogin(false)}>X</div>
            <h2>Login</h2>
            {loginError && <div className="login-error">{loginError}</div>} {/* Display login error if present */}
            <form onSubmit={handleLogin}>
              <input type="text" placeholder="Username" value={email} onChange={(e) => setEmail(e.target.value)} />
              <button type="submit">Login</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Header;
///onClick={() => navigate("Account")}