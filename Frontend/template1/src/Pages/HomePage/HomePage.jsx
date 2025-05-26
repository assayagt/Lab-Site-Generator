import React, { useState, useEffect } from "react";
import "./HomePage.css";
import AboutUs from "../../Components/AboutUs/AboutUs";
import { useAuth } from "../../Context/AuthContext";
import { useEditMode } from "../../Context/EditModeContext";

function HomePage(props) {
  const { fetchToken } = useAuth();
  function fetchData() {
    const storedSid = sessionStorage.getItem("sid");
    if (!storedSid) {
      fetchToken();
    }
  }
  // useEffect(() => {
  //   const storedSid = sessionStorage.getItem("sid");
  //   if (!storedSid) {
  //     fetchToken(); // ✅ Run fetchToken once on mount if sid is missing
  //   }
  // }, []); // Empty array = run only once
  const { editMode } = useEditMode(); // Get edit mode state

  return (
    <div className="HomePage">
      {fetchData()}

      {/* Keep the welcome message always at the top */}
      <div className="subTitle">Welcome to our lab website.</div>

      {/* Main section with dynamic layout */}
      <div
        className={`main_section_homePage ${
          props.about_us ? "hasAboutUs" : "noAboutUs"
        }`}
      >
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
