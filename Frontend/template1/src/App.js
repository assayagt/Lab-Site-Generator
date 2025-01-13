import './App.css';
import HomePage from './Pages/HomePage/HomePage';
import React, {useEffect, useState } from "react";


import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom'; // Import Routes, Navigate
import ParticipantsPage from "./Pages/ParticipantsPage/ParticipantsPage"
import ContactUsPage from './Pages/ContactUsPage/ContactUsPage';
import Header from './Components/Header/Header';
import AccountPage from './Pages/AccountPage/AccountPage';
import PublicationsPage from './Pages/PublicationsPage/PublicationsPage';
//import publications from "./publications.json"
import { AuthProvider } from './Context/AuthContext';
import { WebsiteProvider, useWebsite } from './Context/WebsiteContext';
import { getHomepageDetails,getApprovedPublications  } from  "./services/websiteService"

function App() {


  const { websiteData, setWebsite } = useWebsite();
  const [loading, setLoading] = useState(true);
  const [publications, setPublications] = useState([]); // State for fetched publications

  useEffect(() => {
    const fetchHomepageDetails = async () => {
      const domain = 'example.com'; // Replace with actual domain logic
  
      try {
        const data = await getHomepageDetails(domain);
  
        if (data.response === true) {
          const mappedData = {
            domain: data.data.siteDomain, 
            websiteName: data.data.name, 
            components: data.data.pageComponents, 
            template: data.data.templateType, 
            logo: data.data.logoPath, 
            home_picture: data.data.homePageImage, 
            about_us: data.data.about_us, 
          };
  
          setWebsite(mappedData); 
            const approvedPublications = await getApprovedPublications(mappedData.domain);
          setPublications(approvedPublications); 
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false); 
      }
    };
  
    fetchHomepageDetails();
  }, [setWebsite]);

  if (loading) {
    return <div>Loading...</div>; // Show loading indicator
  }

  const components = websiteData.components || [];

  return (
    <AuthProvider>
      <WebsiteProvider>
        <Router>
              <Header components={components} title={websiteData.websiteName}></Header>
              <Routes>
                <Route path="/" element={<HomePage/>} />
                <Route
                  path="/Participants"
                  element= {<ParticipantsPage />}
                />
                <Route
                  path="/ContactUs"
                  element= {<ContactUsPage address = "Ben Gurion University of the Negev" email ="roni@bgu.ac.il" phone="+972 523456789"/>}
                />
            <Route
                  path="/Account"
                  element= {<AccountPage/>}
                />
                <Route
                  path="/Publications"
                  element= {<PublicationsPage publications={publications}/>}
                />
              </Routes>
        </Router>
      </WebsiteProvider>
    </AuthProvider>
    

    
  );
}

export default App;
