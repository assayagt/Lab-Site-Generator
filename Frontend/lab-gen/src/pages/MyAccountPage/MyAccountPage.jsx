import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './MyAccountPage.css';
import { getCustomWebsites } from '../../services/MyAccount';
import { useWebsite } from '../../Context/WebsiteContext';

const MyAccountPage = () => {
  const [websites, setWebsites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { setWebsite } = useWebsite();
  useEffect(() => {
    // Function to fetch websites from the API
    const fetchWebsites = async () => {
      try {
        const data = await getCustomWebsites(sessionStorage.getItem("sid")); // Replace with your API URL
        if (data.response === "false") {
          throw new Error('Failed to fetch websites');
        }
        console.log(data);
        const websitesArray = Object.entries(data.websites || {}).map(([domain, details]) => ({
          domain,
          ...details,
        }));
        setWebsites(websitesArray);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchWebsites();
  }, []);


  // This function would navigate to the individual website page
  const handleWebsiteClick = (websiteDomain) => {
    console.log(websites);
  
    // Find the website by its domain
    const selectedWebsite = websites.find((site) => site.domain === websiteDomain);
    if (selectedWebsite) {
      console.log(selectedWebsite);
  
      // Update the context with the selected website data
      setWebsite({
        components: selectedWebsite.components || [],
        template: selectedWebsite.template || '',
        domain: selectedWebsite.domain || '',
        websiteName: selectedWebsite.site_name || '',
        created: selectedWebsite.created || false,
        generated: selectedWebsite.generated || false,
      });
  
      // Navigate to the specific website's page or a components page
      navigate("/choose-components");
    } else {
      console.error(`Website with domain ${websiteDomain} not found`);
    }
  };
  if (loading) return <p>Loading...</p>;

  return (
    <div className="myAccountPage">
      <div className="accountInfo">
        <h2>My Account</h2>
      </div>

      <div className="myWebsites">
  <h3>Your Websites</h3>
  {websites?.length > 0 ? (
    <ul className="websiteList">
      {websites.map((website, index) => (
        <li key={index} className="websiteItem">
          <span>{website.site_name} - {website.domain}</span>
          <button onClick={() => handleWebsiteClick(website.domain)}>View Website</button>
        </li>
      ))}
    </ul>
  ) : (
    <p>No websites available.</p>
  )}
</div>
    </div>
  );
};

export default MyAccountPage;
