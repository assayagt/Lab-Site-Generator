import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Tamplate from "../../../images/tamplate.svg";
import { useWebsite } from '../../../Context/WebsiteContext';
import './ChooseComponentsPage.css';
import { createCustomSite, changeComponents, changeDomain, changeName } from '../../../services/Generator';

const ChooseComponentsPage = () => {
  const [saved, setSaved] = useState(false);
  const navigate = useNavigate();
  const { websiteData, setWebsite } = useWebsite();
  const [components, setComponents] = useState(websiteData.components || []);
  const [template, setTemplate] = useState(websiteData.template || '');
  const [domain, setDomain] = useState(websiteData.domain || '');
  const [websiteName, setWebsiteName] = useState(websiteData.websiteName || '');
  const [domainError, setDomainError] = useState(false);
  const [hasContinued, setHasContinued] = useState(false);  
  const [isChanged, setIsChanged] = useState(false);  

  const [initialDomain, setInitialDomain] = useState(websiteData.domain || ''); 
  const [initialWebsiteName, setInitialWebsiteName] = useState(websiteData.websiteName || ''); 


  useEffect(() => {
    console.log(sessionStorage.getItem('isLoggedIn'));
    if (sessionStorage.getItem('isLoggedIn')!=='true') {
      navigate("/");
    }
  }, [ navigate]);

  const handleComponentChange = (component) => {
    setComponents(prevComponents =>
      prevComponents.includes(component)
        ? prevComponents.filter(item => item !== component)
        : [...prevComponents, component]
    );
    setIsChanged(true); 
  };

  const handleSaveNameAndDomain = async () => {
    if (domain !== initialDomain) {
      if (!isValidDomain(domain)) {
        setDomainError(true);
        return;
      }
      let data = await changeDomain(initialDomain, domain);
      if (data) {
        setWebsite({ ...websiteData, domain });
        setInitialDomain(domain); 
        setIsChanged(false); // Mark as changed when domain is modified
      }
    }
    if (websiteName !== initialWebsiteName) {
      let data = await changeName(domain, websiteName); 
      if (data) {
        setWebsite({ ...websiteData, websiteName });
        setInitialWebsiteName(websiteName); 
        setIsChanged(false); // Mark as changed when websiteName is modified
      }
    }
  };

  const handleTemplateClick = (templateName) => {
    if (templateName === template) {
      setTemplate('');
    } else {
      setTemplate(templateName);
    }
    setIsChanged(true); // Mark as changed when template is modified
  };

  const handleDomainChange = (event) => {
    setDomain(event.target.value);
    setIsChanged(true); // Mark as changed when domain is modified
  };

  const handleNameChange = (event) => {
    setWebsiteName(event.target.value);
    setIsChanged(true); // Mark as changed when websiteName is modified
  };

  const handleSaveComponents = () => {
    if (components.length === 0) {
      alert('Please select components');
      return;
    }

    let data = changeComponents(domain, components);
    if (data.response === "true") {
      setWebsite({ ...websiteData, components });
      setSaved(true);
      alert('Components saved successfully!');
      setIsChanged(false); // Reset the change state after saving components
    }
  };

  const handleContinue = async () => {
    if (components.length === 0 || !template) {
      alert('Please select components and a template!');
      return;
    }

    // If no changes have been made, just navigate without saving
    if (!isChanged) {
      navigate("/upload-files");
      return;
    }
    console.log(components)
    let data = await createCustomSite(domain, websiteName, components, template);
    if (data.response === "true") {
      setWebsite({ 
        ...websiteData, 
        domain,
        websiteName,
        components,
        template, 
        created: true  // Update the created field
      });
      setHasContinued(true); // Set hasContinued to true
      setIsChanged(false); // Reset the change state after continuing
      navigate("/upload-files");
    }
  };

  const isValidDomain = (domain) => {
    const regex = /^(?!:\/\/)([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}$/;
    return regex.test(domain);
  };

  return (
    <div>
      <div className="choose_components_main">
        <div className="grid1">
          <div className="create_custom_website">
            <div className="website_domain_name">
              <label>Enter your website domain:</label>
              <div>
                <input
                  type="text"
                  value={domain}
                  onChange={handleDomainChange}
                  onBlur={() => {
                    if (!isValidDomain(domain)) {
                      setDomainError(true);
                    } else {
                      setDomainError(false);
                    }
                  }}
                  placeholder="Enter your website domain"
                  className={domainError ? "input_name_domain error_domain" : "input_name_domain"}
                />
                {domainError && <div className="domain-error-message">Please enter a valid domain</div>}
              </div>
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

            {websiteData.created && (
              <button
                className="save_domain_name_button"
                onClick={handleSaveNameAndDomain}
              >
                Save
              </button>
            )}
          </div>

          <div className="create_custom_website">
            <h2>Choose Components</h2>
            <label>
              <input
                type="checkbox"
                checked={components.includes('About Us')}
                onChange={() => handleComponentChange('About Us')}
              />
              About Us
            </label>
            <label>
              <input
                type="checkbox"
                checked={components.includes('Participants')}
                onChange={() => handleComponentChange('Participants')}
              />
              Participants
            </label>
            <label>
              <input
                type="checkbox"
                checked={components.includes('Contact Us')}
                onChange={() => handleComponentChange('Contact Us')}
              />
              Contact Us
            </label>
            <label>
              <input
                type="checkbox"
                checked={components.includes('Publications')}
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

            {websiteData.created && (
              <button
                className="save_domain_name_button"
                onClick={handleSaveComponents}
              >
                Save Components
              </button>
            )}
          </div>
        </div>

        <div>
          <h2>Choose a Template</h2>
          <div>
            <img
              className={`template ${template !== '' ? 'selected' : ''}`}
              src={Tamplate}
              alt="Template 1"
              onClick={() => handleTemplateClick('Template 1')}
            />
          </div>
          <button
            className="continue_button"
            onClick={handleContinue}
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
