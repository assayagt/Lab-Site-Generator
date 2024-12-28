import React, { useRef, useEffect } from "react";
import "./Header.css";
import Logo from "../images/brain.svg";

function Header(props) {
  const navbarRef = useRef(null); // Reference to the navbar container
  let scrollAnimationFrame = null; // Reference for the animation frame

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
    console.log(center);
    const mouseX = e.clientX;

    if (mouseX <= center - 100) {
      smoothScroll("left");
    }
    if (mouseX >= center + 100) {
      smoothScroll("right");
    }
  };

  return (
    <div className="header">
      <img className="header_logo" src={Logo} alt="logoItem"></img>
      <div className="header_title">{props.title}</div>
      <div className="navbar" ref={navbarRef} onMouseMove={handleMouseEnter}>
        {props.components.map((item, index) => (
          <div className="navbar-item" key={item.id}>
            <div>{item}</div>
            {/* Add | only for items that are not the last item */}
            {index !== props.components.length - 1 && <div>|</div>}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Header;
