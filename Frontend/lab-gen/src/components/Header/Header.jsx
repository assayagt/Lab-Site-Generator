import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import logoIcon from "../../images/launcher.svg";
import "./Header.css";
import { useAuth } from "../../Context/AuthContext";
import logOutIcon from "../../images/logout.svg";
import myWebsitesIcon from "../../images/my_website.svg";
import accountIcon from "../../images/account_avatar.svg";
import LoginPopup from '../Popups/LoginPopup'; 
import { useWebsite } from "../../Context/WebsiteContext";



function Header(props) {
  const {logout } = useAuth();
  const { resetWebsiteData} = useWebsite();
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  const navigate = useNavigate();

  const handleLogin = () => {
    setShowLoginPopup(true);  
  };

  const handleLogout = async() => {
    let data= await logout();  
    if(data===true){
      resetWebsiteData();
      sessionStorage.clear();
      navigate("/");
      // window.location.reload();
    }
    else{
      console.log("sad");
    }
  };

  const doSomething = () => {
     
  };

  const onIconClick = () => {
    navigate("/my-account")
  };

  return (
    <div className="header">
      <img alt="Logo" src={logoIcon} className="img_logo" />
      <h1>{props.title}</h1>
      <div className="menu">
            <div className="hidden-box">
            <div className="personal_menu">
                <div className="icon_photo">
                    {!sessionStorage.getItem('isLoggedIn')?<img src ={accountIcon} alt= "icon" onClick={onIconClick}></img>:
                    <img src ={accountIcon} alt= "icon" ></img>
                    }
                </div>
                <hr className="hr_line" />
                {sessionStorage.getItem('isLoggedIn') ? (
                <div className="choose_item">
                    <button className ="my_sites_button" onClick={doSomething}>
                        <img className = "my_sites_icon "src ={myWebsitesIcon} alt= "logout"></img>
                        My Websites
                    </button> 
                    <button className ="logout_button" onClick={handleLogout}>
                        <img src ={logOutIcon} alt= "logout"></img>
                        Logout
                    </button>
                </div>

                ) : ( <div className="choose_item">
                    <button className ="login_button"onClick={handleLogin}>Login</button>
                    </div>
                )}
                </div>
            </div>
      </div>

      {/* Conditional rendering of the login popup */}
      {showLoginPopup && <LoginPopup onClose={() => setShowLoginPopup(false)} />}

    </div>
  );
}
export default Header;
