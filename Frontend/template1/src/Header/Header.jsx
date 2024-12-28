import React, { useRef, useEffect } from "react";
import "./Header.css"
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

    if(mouseX<=center-100){
      smoothScroll("left");

    }
    if(mouseX>=center+100){
      smoothScroll("right");
    }
    
  };

  // Handle mouse leave to start scrolling back to the left
  const handleMouseLeave = () => {
    //  smoothScroll("left");
  };

  return (
    <div className="header">
      <div   className="navbar"
      ref={navbarRef}
      onMouseMove={handleMouseEnter}
      onMouseLeave={handleMouseLeave}>
        {(props.components).map((item)=>
         <div className="navbar-item" key={item.id}>
         {item}
        </div>
        )}
      </div>
     
    </div>
  );
}
export default Header;
