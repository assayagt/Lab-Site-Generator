// Layout Option 1 - Sidebar Style
import React, { useEffect } from "react";
import "./HomePage2.css";
import AboutUs from "../../Components/AboutUs/AboutUs2";
import NewsSection from "../../Components/NewsSection/NewsSection";
import { useAuth } from "../../Context/AuthContext";
import { useEditMode } from "../../Context/EditModeContext";

function HomePage(props) {
  const { fetchToken } = useAuth();
  const { editMode } = useEditMode();

  function fetchData() {
    const storedSid = sessionStorage.getItem("sid");
    if (!storedSid) {
      fetchToken();
    }
  }

  useEffect(() => {
    const storedSid = sessionStorage.getItem("sid");
    if (!storedSid) {
      fetchToken();
    }
  }, []);

  return (
    <div className="homepage layout-sidebar">
      {fetchData()}

      {/* Full-width hero with background image */}
      <div
        className="homepage__hero-section"
        style={{ backgroundImage: `url(${props.photo})` }}
      >
        <div className="homepage__hero-overlay">
          <div className="homepage__hero-content">
            <h1 className="homepage__main-title">
              Welcome to Our Research Lab
            </h1>
            <p className="homepage__welcome-subtitle">
              Welcome to our lab website.
            </p>
            <p className="homepage__hero-description">
              Advancing scientific discovery through innovative research and
              collaboration
            </p>
          </div>
        </div>
      </div>

      <div className="homepage__main-layout">
        {/* Left Sidebar */}
        <div className="homepage__sidebar">
          {(props.about_us || editMode) && (
            <div className="sidebar-section">
              <h3 className="sidebar-title">About Our Lab</h3>
              <AboutUs info={props.about_us} />
            </div>
          )}

          {(props.news || editMode) && (
            <div className="sidebar-section">
              <h3 className="sidebar-title">Latest News</h3>
              <NewsSection info={props.news} domain={props.domain} />
            </div>
          )}
        </div>

        {/* Main Content */}
        <div className="homepage__main-content">
          <div className="homepage__highlights_t2">
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
                  View Publications →
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
                  Meet the Team →
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
