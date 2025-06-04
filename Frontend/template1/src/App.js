import "./App.css";
import HomePage from "./Pages/HomePage/HomePage";
import HomePage2 from "./Pages/HomePage/HomePage2";
import MediaPage from "./Pages/MediaPage/MediaPage";

import React, { useEffect, useState } from "react";
import { GoogleOAuthProvider } from "@react-oauth/google";
import ParticipantProfile from "./Pages/ParticipantProfile/ParticipantProfile";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom"; // Import Routes, Navigate
import ParticipantsPage2 from "./Pages/ParticipantsPage/ParticipantsPage2";

import ParticipantsPage from "./Pages/ParticipantsPage/ParticipantsPage";
import ContactUsPage from "./Pages/ContactUsPage/ContactUsPage";
import ContactUsPage2 from "./Pages/ContactUsPage/ContactUsPage2";
import Header from "./Components/Header/Header";
import Header2 from "./Components/Header2/Header2";
import AccountPage from "./Pages/AccountPage/AccountPage";

import AccountPage2 from "./Pages/AccountPage/AccountPage2";

import PublicationsPage from "./Pages/PublicationsPage/PublicationsPage";
//import publications from "./publications.json"
import { AuthProvider } from "./Context/AuthContext";
import { useWebsite } from "./Context/WebsiteContext";
import { getHomepageDetails } from "./services/websiteService";
import { NotificationProvider } from "./Context/NotificationContext";
import { EditModeProvider } from "./Context/EditModeContext";
import { useAuth } from "./Context/AuthContext";
function App() {
  const { websiteData, setWebsite } = useWebsite();
  const [loading, setLoading] = useState(true);
  const desiredOrder = [
    "Home",
    "About Us",
    "Lab Members",
    "Publications",
    "Media",
    "Contact Us",
  ];
  useEffect(() => {
    const domain = sessionStorage.getItem("domain");

    if (!domain && !sessionStorage.getItem("alreadyRefreshed")) {
      console.warn("🔁 domain is missing, refreshing page once...");

      // prevent infinite reload loop
      sessionStorage.setItem("alreadyRefreshed", "true");
      window.location.reload();
    }
  }, []);
  useEffect(() => {
    const fetchHomepageDetails = async () => {
      let domain = window.location.hostname;
      domain = domain.replace(/^https?:\/\//, "");
      domain = domain.replace(":3001", "");
      console.log(domain);
      // Add "www." if missing
      if (!domain.startsWith("www.")) {
        domain = `www.${domain}`;
      }

      // Add ".com" if missing
      if (!domain.endsWith(".com")) {
        domain = `${domain}.com`;
      }
      console.log(domain);
      sessionStorage.setItem("domain", domain);
      try {
        const data = await getHomepageDetails(domain);

        // const data = await getHomepageDetails("www.localhost.com");
        // if (data.response === "true") {
        //   const mappedData = {
        //     domain: "www.localhost.com",
        //     websiteName: data.data.name,
        //     components: data.data.components,
        //     template: data.data.template,
        //     logo: data.data.logo,
        //     home_picture: data.data.home_picture,
        //     about_us: data.data.about_us,
        //   };
        console.log(data);
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
          console.log(mappedData);
          setWebsite(mappedData);
          console.log(sessionStorage.getItem("domain"));
          // sessionStorage.setItem("domain", mappedData.domain);
        }
        // await fetchToken();
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

  const components = desiredOrder.filter((comp) =>
    websiteData.components.includes(comp)
  );

  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <NotificationProvider>
          <EditModeProvider>
            <Router>
              {websiteData.template === "template1" ? (
                <Header2
                  components={components}
                  title={websiteData.websiteName}
                  logo={websiteData.logo}
                ></Header2>
              ) : (
                <Header2
                  components={components}
                  title={websiteData.websiteName}
                  logo={websiteData.logo}
                ></Header2>
              )}

              <Routes>
                <Route
                  path="/"
                  element={
                    websiteData.template === "template1" ? (
                      <HomePage2
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
                  element={<ParticipantProfile />}
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
                <Route
                  path="/Account"
                  element={
                    websiteData.template === "template1" ? (
                      <AccountPage />
                    ) : (
                      <AccountPage2 />
                    )
                  }
                />
                <Route path="/Publications" element={<PublicationsPage />} />
                <Route path="/Media" element={<MediaPage />} />
              </Routes>
            </Router>
          </EditModeProvider>
        </NotificationProvider>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}

export default App;
