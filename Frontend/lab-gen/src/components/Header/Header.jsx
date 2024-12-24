import React, { useRef, useState, useEffect } from "react";
import logoIcon from "../../images/launcher.svg";
import "./Header.css";
import { useAuth } from "../../Context/AuthContext";

function Header(props){
    const { isLoggedIn, userEmail, login, logout } = useAuth();
    const handleLogin = () => {
        login(""); 
      };
    
      const handleLogout = () => {
        logout();  
      };
    
    return(
        <div className = "header">
            <img alt = "Logo" src = {logoIcon} className="img_logo"/>
            <h1>{props.title}</h1>
            <div className="menu"> 
            
            <div class="hidden-box">
                <div className="personal_menu">
                    <div className="icon_photo"></div>
                    <hr className="hr_line"/>
                    <div className="choose item">

                    </div>

                </div>
                
            </div>

            </div>

        </div>
    );
}
export default Header;
