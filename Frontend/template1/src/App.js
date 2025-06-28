import "./App.css";
import HomePage from "./Pages/HomePage/HomePage";
import HomePage2 from "./Pages/HomePage/HomePage2";
import MediaPage from "./Pages/MediaPage/MediaPage";
import MediaPage2 from "./Pages/MediaPage/MediaPage2";
import InactivityPopup from "./Components/PopUp/InactivityPopup";
import React, { useEffect, useState, useRef } from "react";
import { GoogleOAuthProvider } from "@react-oauth/google";
import ParticipantProfile from "./Pages/ParticipantProfile/ParticipantProfile";
import ParticipantProfile2 from "./Pages/ParticipantProfile/ParticipantProfile2";

import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useLocation, useNavigate } from "react-router-dom";

import ParticipantsPage2 from "./Pages/ParticipantsPage/ParticipantsPage2";

import ParticipantsPage from "./Pages/ParticipantsPage/ParticipantsPage";
import ContactUsPage from "./Pages/ContactUsPage/ContactUsPage";
import ContactUsPage2 from "./Pages/ContactUsPage/ContactUsPage2";
import Header from "./Components/Header/Header";
import Header2 from "./Components/Header2/Header2";
import AccountPage from "./Pages/AccountPage/AccountPage";

import PublicationsPage from "./Pages/PublicationsPage/PublicationsPage";
import PublicationsPage2 from "./Pages/PublicationsPage/PublicationsPage2";

import { AuthProvider, useAuth } from "./Context/AuthContext";
import { useWebsite } from "./Context/WebsiteContext";
import { getHomepageDetails } from "./services/websiteService";
import { NotificationProvider } from "./Context/NotificationContext";
import { EditModeProvider } from "./Context/EditModeContext";

function AppContent() {
  const { websiteData, setWebsite } = useWebsite();
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth(); // Assuming you have user and logout from AuthContext
  const [loading, setLoading] = useState(true);
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  const [loginError, setLoginError] = useState(false);
  const [userLoggedOut, setUserLoggedOut] = useState(
    sessionStorage.getItem("wasLoggedOutDueToInactivity") === "true"
  ); // Track if user was logged out due to inactivity

  // Reference to the logout timer
  const logoutTimerRef = useRef(null);

  const desiredOrder = [
    "Home",
    "About Us",
    "Lab Members",
    "Publications",
    "Media",
    "Contact Us",
  ];

  // Function to handle auto-logout
  const handleAutoLogout = async () => {
    if (user) {
      // Only logout if user is actually logged in
      const logoutSuccess = await logout();
      if (logoutSuccess) {
        // Clear session storage and user state
        sessionStorage.removeItem("isLoggedIn");
        sessionStorage.removeItem("userEmail");
        sessionStorage.clear();
        console.log("User has been logged out due to inactivity.");
        sessionStorage.setItem("wasLoggedOutDueToInactivity", "true"); // set again after clearing

        window.location.reload(); // <--- This forces a full page refresh
      }
    }
  };

  useEffect(() => {
    const wasLoggedOut = sessionStorage.getItem("wasLoggedOutDueToInactivity");
    if (wasLoggedOut === "true") {
      setUserLoggedOut(true);
      setShowLoginPopup(true);
      if (location.pathname === "/Account") {
        navigate("/");
      }
    }
  }, []);

  // Function to reset the inactivity timer
  const resetTimer = () => {
    if (logoutTimerRef.current) {
      clearTimeout(logoutTimerRef.current);
    }

    // Only set timer if user is logged in
    if (user) {
      logoutTimerRef.current = setTimeout(async () => {
        await handleAutoLogout();
      }, 1 * 60 * 1000); // 2 minutes for testing (change to 60 * 60 * 1000 for 60 minutes)
    }
  };

  // Set up inactivity timer
  useEffect(() => {
    // Events to track user activity
    const events = [
      "load",
      "mousemove",
      "mousedown",
      "click",
      "scroll",
      "keypress",
      "touchstart",
    ];

    // Add event listeners
    events.forEach((event) => {
      window.addEventListener(event, resetTimer);
    });

    // Start the timer initially
    resetTimer();

    // Cleanup function
    return () => {
      events.forEach((event) => {
        window.removeEventListener(event, resetTimer);
      });
      if (logoutTimerRef.current) {
        clearTimeout(logoutTimerRef.current);
      }
    };
  }, [user]); // Re-run when user login status changes

  // Reset the logged out flag when user logs back in
  useEffect(() => {
    if (user) {
      setUserLoggedOut(false);
    }
  }, [user]);

  useEffect(() => {
    const domain = sessionStorage.getItem("domain");

    if (!domain && !sessionStorage.getItem("alreadyRefreshed")) {
      console.warn("🔁 domain is missing, refreshing page once...");
      sessionStorage.setItem("alreadyRefreshed", "true");
      window.location.reload();
    }
  }, []);

  useEffect(() => {
    const fetchHomepageDetails = async () => {
      let domain = window.location.hostname;
      domain = domain.replace(/^https?:\/\//, "");
      domain = domain.replace(":3001", "");

      if (!domain.startsWith("www.")) {
        domain = `www.${domain}`;
      }

      if (!domain.endsWith(".com")) {
        domain = `${domain}.com`;
      }

      sessionStorage.setItem("domain", domain);

      try {
        const data = await getHomepageDetails(domain);

        if (data.response === "true") {
          const mappedData = {
            domain: data.data.domain,
            websiteName: data.data.name,
            components: data.data.components,
            template: data.data.template,
            logo: data.data.logo,
            home_picture: data.data.home_picture,
            about_us: data.data.components.includes("About Us")
              ? data.data.about_us
              : "",
            news: data.data.components.includes("News") ? data.data.news : "",
          };
          setWebsite(mappedData);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHomepageDetails();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  const components = desiredOrder.filter((comp) =>
    websiteData.components.includes(comp)
  );

  return (
    <>
      {/* Show notification if user was logged out due to inactivity */}
      {userLoggedOut && (
        <InactivityPopup
          onClose={() => {
            setShowLoginPopup(false);
            setUserLoggedOut(false);
            sessionStorage.removeItem("wasLoggedOutDueToInactivity");
          }}
        ></InactivityPopup>
      )}

      {websiteData.template === "template1" ? (
        <Header
          components={components}
          title={websiteData.websiteName}
          logo={websiteData.logo}
        />
      ) : (
        <Header2
          components={components}
          title={websiteData.websiteName}
          logo={websiteData.logo}
        />
      )}

      <Routes>
        <Route
          path="/"
          element={
            websiteData.template === "template1" ? (
              <HomePage
                about_us={websiteData.about_us}
                photo={websiteData.home_picture}
                news={websiteData.news}
                domain={websiteData.domain}
              />
            ) : (
              <HomePage2
                about_us={websiteData.about_us}
                photo={websiteData.home_picture}
                news={websiteData.news}
                domain={websiteData.domain}
              />
            )
          }
        />
        <Route
          path="/participant/:email"
          element={
            websiteData.template === "template1" ? (
              <ParticipantProfile />
            ) : (
              <ParticipantProfile2 />
            )
          }
        />
        <Route
          path="/LabMembers"
          element={
            websiteData.template === "template1" ? (
              <ParticipantsPage />
            ) : (
              <ParticipantsPage2 />
            )
          }
        />
        <Route
          path="/ContactUs"
          element={
            websiteData.template === "template1" ? (
              <ContactUsPage
                address="Ben Gurion University of the Negev"
                email="roni@bgu.ac.il"
                phone="+972 523456789"
              />
            ) : (
              <ContactUsPage2
                address="Ben Gurion University of the Negev"
                email="roni@bgu.ac.il"
                phone="+972 523456789"
              />
            )
          }
        />
        <Route path="/Account" element={<AccountPage />} />
        <Route
          path="/Publications"
          element={
            websiteData.template === "template1" ? (
              <PublicationsPage />
            ) : (
              <PublicationsPage2 />
            )
          }
        />
        <Route
          path="/Media"
          element={
            websiteData.template === "template1" ? (
              <MediaPage />
            ) : (
              <MediaPage2 />
            )
          }
        />
      </Routes>
    </>
  );
}

function App() {
  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <Router>
        <AuthProvider>
          <NotificationProvider>
            <EditModeProvider>
              <AppContent />
            </EditModeProvider>
          </NotificationProvider>
        </AuthProvider>
      </Router>
    </GoogleOAuthProvider>
  );
}

export default App;
