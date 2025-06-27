import "./App.css";
import HomePage from "./Pages/HomePage/HomePage";
import React, { useEffect, useState } from "react";
import { GoogleOAuthProvider } from "@react-oauth/google";
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container } from 'react-bootstrap';

import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import ParticipantsPage from "./Pages/ParticipantsPage/ParticipantsPage";
import ContactUsPage from "./Pages/ContactUsPage/ContactUsPage";
import Header from "./Components/Header/Header";
import AccountPage from "./Pages/AccountPage/AccountPage";
import PublicationsPage from "./Pages/PublicationsPage/PublicationsPage";
import { AuthProvider } from "./Context/AuthContext";
import { useWebsite } from "./Context/WebsiteContext";
import { getHomepageDetails } from "./services/websiteService";
import { NotificationProvider } from "./Context/NotificationContext";
import { EditModeProvider } from "./Context/EditModeContext";

function App() {
  const { websiteData, setWebsite } = useWebsite();
  const [loading, setLoading] = useState(true);

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
            about_us: data.data.about_us,
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
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: "100vh" }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  const components = [...new Set(websiteData.components)];

  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <NotificationProvider>
          <EditModeProvider>
            <Router>
              <div className="d-flex flex-column min-vh-100">
                <Header
                  components={components}
                  title={websiteData.websiteName}
                  logo={websiteData.logo}
                />
                <Container fluid className="flex-grow-1 py-4">
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
                    <Route path="/LabMembers" element={<ParticipantsPage />} />
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
                </Container>
              </div>
            </Router>
          </EditModeProvider>
        </NotificationProvider>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}

export default App;
