import React, { useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import "./Header.css";
import Logo from "../../images/brain.svg";
import accountIcon from "../../images/account_avatar.svg";


function Header(props) {
  
  const navbarRef = useRef(null); 
  const navigate = useNavigate();

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

    scrollStep(); // Start scrolling
  };

  const handleMouseEnter = (e) => {
    const { left, right, width } = navbarRef.current.getBoundingClientRect();
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
    }
    else if (item === "Contact Us") {
      navigate("/ContactUs"); 
    }
  };

  return (
    <div className="header">
      <img className="header_logo" src={Logo} alt="logoItem"></img>
      <div className="header_title">{props.title}</div>
      <div className="navbar" ref={navbarRef} onMouseMove={handleMouseEnter}>
        {props.components.filter(item => item !== "About Us").map((item, index, filteredArray) => (
          <div className="navbar-item" key={item.id || index}> {/* Use index if there's no id */}
            <button onClick={()=>handleClick(item)} className="navbar-item-button" >
              {item}
            </button>
            {/* Add | only for items that are not the last item */}
            {index !== filteredArray.length - 1 && <div>|</div>}
          </div>
          ))}
      </div>
      <div className="icon_photo">
      <div className="menu">
                  <div className="hidden-box">
                  <div className="personal_menu">
                      <div className="icon_photo">
                          {!sessionStorage.getItem('isLoggedIn')?<img src ={accountIcon} alt= "icon" onClick={console.log("j")}></img>:
                          <img src ={accountIcon} alt= "icon" ></img>
                          }
                      </div>
                      <hr className="hr_line" />
                      {sessionStorage.getItem('isLoggedIn') ? (
                      <div className="choose_item">
                          <button className ="my_sites_button" onClick={console.log("j")}>
                              My Account
                          </button> 
                          <button className ="logout_button" onClick={console.log("j")}>
                              {/* <img src ={} alt= "logout"></img> */}
                              Logout
                          </button>
                      </div>
      
                      ) : ( <div className="choose_item">
                          <button className ="login_button"onClick={console.log("j")}>Login</button>
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
