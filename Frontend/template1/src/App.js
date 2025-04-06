import "./App.css";
import HomePage from "./Pages/HomePage/HomePage";
import React, { useEffect, useState } from "react";

import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom"; // Import Routes, Navigate
import ParticipantsPage from "./Pages/ParticipantsPage/ParticipantsPage";
import ContactUsPage from "./Pages/ContactUsPage/ContactUsPage";
import Header from "./Components/Header/Header";
import AccountPage from "./Pages/AccountPage/AccountPage";
import PublicationsPage from "./Pages/PublicationsPage/PublicationsPage";
//import publications from "./publications.json"
import { AuthProvider } from "./Context/AuthContext";
import { useWebsite } from "./Context/WebsiteContext";
import { getHomepageDetails } from "./services/websiteService";
import { NotificationProvider } from "./Context/NotificationContext";
import { EditModeProvider } from "./Context/EditModeContext";
function App() {
  const { websiteData, setWebsite } = useWebsite();

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHomepageDetails = async () => {
      let pathParts = window.location.pathname.split('/');
      let domain = pathParts[2]; // "/labs-beta/beta4/" → ['', 'labs-beta', 'beta4', '']
      console.log("Detected lab domain:", domain);
      console.log(domain);
      // Add "www." if missing
      //if (!domain.startsWith("www.")) {
      //  domain = `www.${domain}`;
      //}

      // Add ".com" if missing
      //if (!domain.endsWith(".com")) {
      //  domain = `${domain}.com`;
      //}
      console.log(domain);
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
            about_us: data.data.about_us,
          };
          setWebsite(mappedData);
          sessionStorage.setItem("domain", mappedData.domain);
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
    return <div>Loading...</div>; // Show loading indicator
  }

  const components = [...new Set(websiteData.components)];

  return (
    <AuthProvider>
      <NotificationProvider>
        <EditModeProvider>
          <Router>
            <Header
              components={components}
              title={websiteData.websiteName}
              logo={websiteData.logo}
            ></Header>
            <Routes>
              <Route
                path="/"
                element={
                  <HomePage
                    about_us={websiteData.about_us}
                    photo={websiteData.home_picture}
                  />
                }
              />
              <Route path="/Participants" element={<ParticipantsPage />} />
              <Route
                path="/ContactUs"
                element={
                  <ContactUsPage
                    address="Ben Gurion University of the Negev"
                    email="roni@bgu.ac.il"
                    phone="+972 523456789"
                  />
                }
              />
              <Route path="/Account" element={<AccountPage />} />
              <Route path="/Publications" element={<PublicationsPage />} />
            </Routes>
          </Router>
        </EditModeProvider>
      </NotificationProvider>
    </AuthProvider>
  );
}

export default App;
