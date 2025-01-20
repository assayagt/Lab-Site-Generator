import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './MyAccountPage.css';

const MyAccountPage = () => {
 

  const [websites, setWebsites] = useState([
    { id: 1, name: 'Website 1', domain: 'website1.com' },
    { id: 2, name: 'Website 2', domain: 'website2.com' },
    { id: 3, name: 'Website 3', domain: 'website3.com' },
    // This would be dynamically fetched from the server
  ]);

  const navigate = useNavigate();

  // This function would navigate to the individual website page
  const handleWebsiteClick = (websiteId) => {
    
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
