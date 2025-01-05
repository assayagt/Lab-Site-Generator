import React, { useRef, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Header.css";
import Logo from "../../images/brain.svg";
import accountIcon from "../../images/account_avatar.svg";

function Header(props) {
  const navbarRef = useRef(null); 
  const navigate = useNavigate();

  const [hasNotifications, setHasNotifications] = useState(false); // State for notifications

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
    }
   else if (item === "Publications") {
    navigate("/Publications"); 
  }
  };

  // Simulate fetching notifications
  useEffect(() => {
    // // Simulate an API call or notification check
    // const timer = setTimeout(() => {
    //   setHasNotifications(!hasNotifications); // Set to true when there are notifications
    // }, 2000);

    // return () => clearTimeout(timer);
  }, [hasNotifications]);

  return (
    <div className="header">
      <img className="header_logo" src={Logo} alt="logoItem" />
      <div className="header_title">{props.title}</div>
      <div className="navbar" ref={navbarRef} onMouseMove={handleMouseEnter}>
        {props.components
          .filter((item) => item !== "About Us")
          .map((item, index, filteredArray) => (
            <div className="navbar-item" key={item.id || index}>
              <button
                onClick={() => handleClick(item)}
                className="navbar-item-button"
              >
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
                  <img
                    src={accountIcon}
                    alt="icon"
                    onClick={() => navigate("Account")}
                  />
                
              </div>
              <hr className="hr_line" />
              {sessionStorage.getItem("isLoggedIn") ? (
                <div className="choose_item">
                  <button
                    className="my_sites_button"
                    onClick={() => console.log("My Account clicked")}
                  >
                    My Account
                  </button>
                  <button
                    className="logout_button"
                    onClick={() => console.log("Logout clicked")}
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <div className="choose_item">
                  <button
                    className="login_button"
                    onClick={() => console.log("Login clicked")}
                  >
                    Login
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Header;
