// HomePage.jsx
import React, { useEffect } from "react";
import "./HomePage2.css";
import AboutUs from "../../Components/AboutUs/AboutUs2";
import { useAuth } from "../../Context/AuthContext";
import { useEditMode } from "../../Context/EditModeContext";

function HomePage(props) {
  const { fetchToken } = useAuth();
  const { editMode } = useEditMode();

  useEffect(() => {
    const storedSid = sessionStorage.getItem("sid");
    if (!storedSid) {
      fetchToken(); // Run fetchToken once on mount if sid is missing
    }
  }, []); // Empty array = run only once

  return (
    <div className="homepage">
      <div className="homepage__container">
        {/* Hero section */}
        <div className="homepage__hero">
          <div className="homepage__content">
            <h1 className="homepage__title">Welcome to Our Research Lab</h1>
            <p className="homepage__subtitle">
              Advancing scientific discovery through innovative research and
              collaboration
            </p>

            {/* About Us directly in the hero section */}
            {(props.about_us || editMode) && (
              <div className="homepage__about-container">
                <AboutUs info={props.about_us} />
              </div>
            )}
          </div>

          <div className="homepage__image-container">
            <img
              src={props.photo}
              className="homepage__image"
              alt="Laboratory research"
            />
          </div>
        </div>

        {/* Research Highlights - Only showing Publications and Lab Members */}
        <div className="homepage__highlights">
          <h2 className="homepage__section-title">Research Highlights</h2>
          <div className="homepage__cards">
            <div className="research-card">
              <div className="research-card__icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                </svg>
              </div>
              <h3 className="research-card__title">Recent Publications</h3>
              <p className="research-card__description">
                Our team has published groundbreaking research in leading
                scientific journals
              </p>
              <a href="/Publications" className="research-card__link">
                View Publications
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M5 12h14"></path>
                  <path d="m12 5 7 7-7 7"></path>
                </svg>
              </a>
            </div>

            <div className="research-card">
              <div className="research-card__icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                  <circle cx="9" cy="7" r="4"></circle>
                  <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
              </div>
              <h3 className="research-card__title">Lab Members</h3>
              <p className="research-card__description">
                Meet our diverse team of researchers, faculty, and students
              </p>
              <a href="/LabMembers" className="research-card__link">
                Meet the Team
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M5 12h14"></path>
                  <path d="m12 5 7 7-7 7"></path>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
