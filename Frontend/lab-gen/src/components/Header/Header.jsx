import React, { useRef, useState, useEffect } from "react";
import logoIcon from "../../images/launcher.svg";
import "./Header.css"

function Header(props){
    const [IsLoginOpen, setisLoginOpen] = useState(false);


    return(
        <div className = "header">
            <img alt = "Logo" src = {logoIcon} className="img_logo"/>
            <h1>{props.title}</h1>
            <div className="menu"> 
            <div class="hidden-box">I appear on hover!</div>

            </div>

        </div>
    );
}
export default Header;
