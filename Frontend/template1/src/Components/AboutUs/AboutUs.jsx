import React from "react";
import "./AboutUs.css"

function AboutUs(props) {

  return (
     <div className="AboutUsComponent">
        <div className="aboutUsTitle">
            About Us
        </div>
        <div className="aboutUsParagraph">
            {props.info}
        </div>
        <div></div>
     </div>

  );
}

export default AboutUs;