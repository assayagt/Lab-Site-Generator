import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useLocation, useNavigate } from "react-router-dom";
import React, { useEffect, useState, useRef } from "react";
import WelcomePage from "./pages/WelcomePage/WelcomePage";
import ChooseComponentsPage from "./pages/Generate/ChooseComponentsPage/ChooseComponentsPage";
import { AuthProvider, useAuth } from "./Context/AuthContext";
import { WebsiteProvider } from "./Context/WebsiteContext";
import MyAccountPage from "./pages/MyAccountPage/MyAccountPage";
import Header from "./components/Header/Header";
import { GoogleOAuthProvider } from "@react-oauth/google";

function AppContent() {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [isLoggedIn, setIsLoggedIn] = useState(
    sessionStorage.getItem("isLoggedIn") === "true"
  );
  const [userLoggedOut, setUserLoggedOut] = useState(
    sessionStorage.getItem("wasLoggedOutDueToInactivity") === "true"
  );

  // Reference to the logout timer
  const logoutTimerRef = useRef(null);

  // Function to handle auto-logout
  const handleAutoLogout = async () => {
    if (isLoggedIn) {
      // Only logout if user is actually logged in
      const logoutSuccess = await logout();
      if (logoutSuccess) {
        // Clear session storage and user state
        sessionStorage.removeItem("isLoggedIn");
        sessionStorage.removeItem("userEmail");
        sessionStorage.setItem("wasLoggedOutDueToInactivity", "true");
        console.log("User has been logged out due to inactivity.");

        // Update local state
        setIsLoggedIn(false);
        setUserLoggedOut(true);

        // Navigate to homepage instead of reloading
        navigate("/");
      }
    }
  };

  // Check if user was logged out due to inactivity on component mount
  useEffect(() => {
    const wasLoggedOut = sessionStorage.getItem("wasLoggedOutDueToInactivity");
    if (wasLoggedOut === "true") {
      setUserLoggedOut(true);
      // Navigate to homepage if user was on a protected page
      if (
        location.pathname === "/my-account" ||
        location.pathname === "/choose-components"
      ) {
        navigate("/");
      }
    }
  }, [location.pathname, navigate]);

  // Function to reset the inactivity timer
  const resetTimer = () => {
    if (logoutTimerRef.current) {
      clearTimeout(logoutTimerRef.current);
    }

    // Only set timer if user is logged in
    if (isLoggedIn) {
      logoutTimerRef.current = setTimeout(async () => {
        await handleAutoLogout();
      }, 60 * 60 * 1000); // 60 minutes (change to 1 * 60 * 1000 for 1 minute testing)
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
  }, [isLoggedIn]); // Re-run when user login status changes

  // Reset the logged out flag when user logs back in
  useEffect(() => {
    if (isLoggedIn) {
      setUserLoggedOut(false);
      sessionStorage.removeItem("wasLoggedOutDueToInactivity");
    }
  }, [isLoggedIn]);

  // Listen for sessionStorage changes to update local state
  useEffect(() => {
    const handleStorageChange = () => {
      const loggedIn = sessionStorage.getItem("isLoggedIn") === "true";
      setIsLoggedIn(loggedIn);
    };

    // Listen for storage events (from other tabs)
    window.addEventListener("storage", handleStorageChange);

    // Also check periodically in case sessionStorage is updated in same tab
    const interval = setInterval(handleStorageChange, 1000);

    return () => {
      window.removeEventListener("storage", handleStorageChange);
      clearInterval(interval);
    };
  }, []);

  return (
    <>
      <Header
        title="LabLauncher"
        showInactivityMessage={userLoggedOut}
        onMessageDismiss={() => setUserLoggedOut(false)}
      />
      <Routes>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/choose-components" element={<ChooseComponentsPage />} />
        <Route path="/my-account" element={<MyAccountPage />} />
      </Routes>
    </>
  );
}

function App() {
  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <WebsiteProvider>
          <Router>
            <AppContent />
          </Router>
        </WebsiteProvider>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}

export default App;
