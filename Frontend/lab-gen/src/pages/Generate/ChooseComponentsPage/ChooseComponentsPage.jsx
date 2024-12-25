import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../../components/Header/Header';
import Tamplate from "../../../images/tamplate.svg";
import { useWebsite } from '../../../Context/WebsiteContext';
import './ChooseComponentsPage.css';

const ChooseComponentsPage = () => {
  const [saved, setSaved] = useState(false); // Track if components are saved
  const navigate = useNavigate(); // Use navigate for routing
  const { websiteData, setWebsite } = useWebsite(); // Get website data and setter from context


  // Handle checkbox changes for components
  const handleComponentChange = (component) => {
    setWebsite({ components: websiteData.components.includes(component)
      ? websiteData.components.filter(item => item !== component)
      : [...websiteData.components, component] });
  };

  const handleTemplateClick = (templateName) => {
    setWebsite({ template: templateName });
  };

  // Handle domain change
  const handleDomainChange = (event) => {
    setWebsite({ domain: event.target.value });
  };

  // Handle website name input change
  const handleNameChange = (event) => {
    setWebsite({ websiteName: event.target.value });
  };

  const handleSaveComponents = () => {
    if (websiteData.components.length === 0) {
      alert('Please select components');
      return;
    }
    setSaved(true);
    alert('Components saved successfully!');
  };

  // Continue to the next page
  const handleContinue = () => {
    if (websiteData.components.length === 0 || !websiteData.template) {
      alert('Please select components and a template!');
      return;
    }
    navigate('/upload-files'); // Use navigate to go to the next page
  };

  return (
    <div>
      <Header title="LabLauncher" />
      <div className="choose_components_main">
        <div className="grid1">
          <div className="create_custom_website">
            <div className="website_domain_name">
              <label>Enter your website domain:</label>
              <input
                type="text"
                value={websiteData.domain}
                onChange={handleDomainChange}
                placeholder="Enter your website domain"
                className="input_name_domain"
              />
            </div>
            <div className="website_domain_name">
              <label>Enter your website name:</label>
              <input
                type="text"
                value={websiteData.websiteName}
                onChange={handleNameChange}
                placeholder="Enter your website name"
                className="input_name_domain"
              />
            </div>
            <button className="save_domain_name_button">Save</button>
          </div>
          <div className="create_custom_website">
            <h2>Choose Components</h2>
            <label>
              <input
                type="checkbox"
                onChange={() => handleComponentChange('About Us')}
              />
              About Us
            </label>
            <label>
              <input
                type="checkbox"
                onChange={() => handleComponentChange('Participants')}
              />
              Participants
            </label>
            <label>
              <input
                type="checkbox"
                onChange={() => handleComponentChange('Contact Us')}
              />
              Contact Us
            </label>
            <label>
              <input
                type="checkbox"
                onChange={() => handleComponentChange('Publications')}
              />
              Publications
            </label>
            <label className="disabled">
              <input type="checkbox" disabled />
              News
            </label>
            <label className="disabled">
              <input type="checkbox" disabled />
              Media
            </label>
            <label className="disabled">
              <input type="checkbox" disabled />
              Page for each participant
            </label>
            <div>
              <button className="save_domain_name_button" onClick={handleSaveComponents}>
                Save Components
              </button>
            </div>
          </div>
        </div>
        <div>
          <h2>Choose a Template</h2>
          <div>
            <img
              className="tamplate"
              src={Tamplate}
              alt="Template 1"
              onClick={() => handleTemplateClick('Template 1')}
            />
          </div>
          <button onClick={handleContinue}>Continue</button>
          {saved && <p>Your components and template have been saved!</p>}
        </div>
      </div>
    </div>
  );
};

export default ChooseComponentsPage;
