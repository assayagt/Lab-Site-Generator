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
  const { websiteData, setWebsite } = useWebsite();
  useEffect(() => {
    // Function to fetch websites from the API
    const fetchWebsites = async () => {
      try {
        const data = await getCustomWebsites(sessionStorage.getItem("sid")); // Replace with your API URL
        if (data.response === "false") {
          throw new Error('Failed to fetch websites');
        }
        console.log(data);
        setWebsites(data.data); 
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchWebsites();
  }, []);


  // This function would navigate to the individual website page
  const handleWebsiteClick = (websiteId) => {
    const selectedWebsite = websites.find((site) => site.id === websiteId);
    setWebsite(selectedWebsite); // Save data to context
  };

  return (
    <div className="myAccountPage">
      <div className="accountInfo">
        <h2>My Account</h2>
      </div>

      <div className="myWebsites">
        <h3>Your Websites</h3>
        {websites.length > 0 ? (
          <ul className="websiteList">
            {websites.map((website) => (
              <li key={website.id} className="websiteItem">
                <span>{website.name} - {website.domain}</span>
                <button onClick={() => handleWebsiteClick(website.id)}>View Website</button>
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
