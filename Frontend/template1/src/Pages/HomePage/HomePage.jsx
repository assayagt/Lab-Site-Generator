import React, { useState, useEffect } from "react";
import "./HomePage.css";
import AboutUs from "../../Components/AboutUs/AboutUs";
import NewsSection from "../../Components/NewsSection/NewsSection";
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
      <div className="main_section_homePage_entire">
        <div
          className={`main_section_homePage ${
            props.about_us ? "hasAboutUs" : "hasAboutUs"
          }`}
        >
          {
            <div className="section_news">
              {(props.about_us || editMode) && (
                <div className="aboutUsContainer">
                  <AboutUs info={props.about_us} />
                </div>
              )}
              {props.news && (
                <div className="newsWrapper">
                  <h2 className="timeline-title">News</h2>

                  <NewsSection info={props.news} domain={props.domain} />
                </div>
              )}
            </div>
          }

          <img src={props.photo} className="homeImg" alt="home_page_photo" />
        </div>
      </div>
    </div>
  );
}

export default HomePage;
