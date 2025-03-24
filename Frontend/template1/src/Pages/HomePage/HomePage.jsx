import React from "react";
import "./HomePage.css";
import AboutUs from "../../Components/AboutUs/AboutUs";
import { useAuth } from "../../Context/AuthContext";


function HomePage(props) {
  
  const { fetchToken } = useAuth();
  function fetchData() {
    const storedSid = sessionStorage.getItem('sid');
    if (!storedSid) {
      fetchToken();  
    }    
  }

  return (
    <div className="HomePage">
      {fetchData()}
      
      {/* Keep the welcome message always at the top */}
      <div className="subTitle">Welcome to our lab website.</div>

      {/* Main section with dynamic layout */}
      <div className={`main_section_homePage ${props.about_us ? "hasAboutUs" : "noAboutUs"}`}>
        {props.about_us && (
          <div className="aboutUsContainer">
            <AboutUs info={props.about_us} />
          </div>
        )}
        <img src={props.photo} className="homeImg" alt="home_page_photo" />
      </div>
    </div>
  );
}

export default HomePage;