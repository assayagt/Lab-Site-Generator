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
  const [components, setComponents] = useState(websiteData.components || []);
  const [template, setTemplate] = useState(websiteData.template || '');
  const [domain, setDomain] = useState(websiteData.domain || '');
  const [websiteName, setWebsiteName] = useState(websiteData.websiteName || '');

  // Handle checkbox changes for components
  const handleComponentChange = (component) => {
    setComponents(prevComponents =>
      prevComponents.includes(component)
        ? prevComponents.filter(item => item !== component)
        : [...prevComponents, component]
    );
  };

  // Save website name and domain
  const handleSaveNameAndDomain = () => {
    setWebsite({ ...websiteData, domain, websiteName });
  };

  // Handle template selection and apply border
  const handleTemplateClick = (templateName) => {
    if (templateName === template) {
      setTemplate(''); // Set the selected template
    } else {
      setTemplate(templateName);
    }
  };

  // Handle domain change
  const handleDomainChange = (event) => {
    setDomain(event.target.value);
  };

  // Handle website name input change
  const handleNameChange = (event) => {
    setWebsiteName(event.target.value);
  };

  // Save components to the websiteData
  const handleSaveComponents = () => {
    if (components.length === 0) {
      alert('Please select components');
      return;
    }
    setWebsite({ ...websiteData, components });
    setSaved(true);
    alert('Components saved successfully!');
  };

  // Continue to the next page
  const handleContinue = () => {
    if (components.length === 0 || !template) {
      alert('Please select components and a template!');
      return;
    }
    setWebsite({ ...websiteData, template });
    navigate('/upload-files'); // Navigate to the next page
  };

  const isDomainAndNameValid = domain && websiteName;

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
                value={domain}
                onChange={handleDomainChange}
                placeholder="Enter your website domain"
                className="input_name_domain"
              />
            </div>
            <div className="website_domain_name">
              <label>Enter your website name:</label>
              <input
                type="text"
                value={websiteName}
                onChange={handleNameChange}
                placeholder="Enter your website name"
                className="input_name_domain"
              />
            </div>
            <button
              className="save_domain_name_button"
              onClick={handleSaveNameAndDomain}
            >
              Save
            </button>
          </div>

          {/* Conditionally disable the "Choose Components" section */}
          <div className={`create_custom_website ${isDomainAndNameValid ? '' : 'disabled_section'}`}>
            <h2>Choose Components</h2>
            <label>
              <input
                type="checkbox"
                checked={components.includes('About Us')}
                onChange={() => handleComponentChange('About Us')}
                disabled={!isDomainAndNameValid} // Disable if domain or name is not valid
              />
              About Us
            </label>
            <label>
              <input
                type="checkbox"
                checked={components.includes('Participants')}
                onChange={() => handleComponentChange('Participants')}
                disabled={!isDomainAndNameValid} // Disable if domain or name is not valid
              />
              Participants
            </label>
            <label>
              <input
                type="checkbox"
                checked={components.includes('Contact Us')}
                onChange={() => handleComponentChange('Contact Us')}
                disabled={!isDomainAndNameValid} // Disable if domain or name is not valid
              />
              Contact Us
            </label>
            <label>
              <input
                type="checkbox"
                checked={components.includes('Publications')}
                onChange={() => handleComponentChange('Publications')}
                disabled={!isDomainAndNameValid} // Disable if domain or name is not valid
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
              <button
                className="save_domain_name_button"
                onClick={handleSaveComponents}
                disabled={!isDomainAndNameValid} // Disable if domain or name is not valid
              >
                Save Components
              </button>
            </div>
          </div>
        </div>

        <div>
          <h2>Choose a Template</h2>
          <div>
            <img
              className={`template ${template === 'Template 1' ? 'selected' : ''}`}
              src={Tamplate}
              alt="Template 1"
              onClick={() => handleTemplateClick('Template 1')}
            />
          </div>
          <button
            className="continue_button"
            onClick={handleContinue}
            disabled={!isDomainAndNameValid} // Disable if domain or name is not valid
          >
            Continue
          </button>
          {saved && <div className="saved_message">Your components and template have been saved!</div>}
        </div>
      </div>
    </div>
  );
};

export default ChooseComponentsPage;
