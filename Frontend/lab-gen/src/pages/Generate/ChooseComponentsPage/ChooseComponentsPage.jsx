import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../../components/Header/Header';
import Tamplate from "../../../images/tamplate.svg";
import { useWebsite } from '../../../Context/WebsiteContext';
import './ChooseComponentsPage.css';
import { useAuth } from '../../../Context/AuthContext';
import {createCustomSite,changeComponents} from '../../../services/Generator'

const ChooseComponentsPage = () => {
  const [saved, setSaved] = useState(false); 
  const navigate = useNavigate(); 
  const { websiteData, setWebsite } = useWebsite(); 
  const [components, setComponents] = useState(websiteData.components || []);
  const [template, setTemplate] = useState(websiteData.template || '');
  const [domain, setDomain] = useState(websiteData.domain || '');
  const [websiteName, setWebsiteName] = useState(websiteData.websiteName || '');
  const [savedDomainName, setSaveDomainName] = useState(false || websiteData.domain); 
  const {isLoggedIn} = useAuth();
  const [domainError, setDomainError] = useState(false); // New state for domain error message

  useEffect(() => {
    if (!isLoggedIn) {
      navigate("/");
    }
  }, []);

  const handleComponentChange = (component) => {
    setComponents(prevComponents =>
      prevComponents.includes(component)
        ? prevComponents.filter(item => item !== component)
        : [...prevComponents, component]
    );
  };

  const handleSaveNameAndDomain = async() => {
    let data = await createCustomSite(domain,websiteName);
    if(data){
      setWebsite({ ...websiteData, domain, websiteName });
      setSaveDomainName(true);
    }
        
  };

  const handleTemplateClick = (templateName) => {
    if (templateName === template) {
      setTemplate(''); 
    } else {
      setTemplate(templateName);
    }
  };

  const handleDomainChange = (event) => {
    setDomain(event.target.value);
    setSaveDomainName(false);
  };

  const handleNameChange = (event) => {
    setWebsiteName(event.target.value);
    setSaveDomainName(false);
  };

  const handleSaveComponents = () => {
    if (components.length === 0) {
      alert('Please select components');
      return;
    }

    let data = changeComponents(domain,components);
    if(data.response=="true"){
      setWebsite({ ...websiteData, components });
      setSaved(true);
      alert('Components saved successfully!');
    }
    
  };

  const handleContinue = () => {
    if (components.length === 0 || !template) {
      alert('Please select components and a template!');
      return;
    }
    setWebsite({ ...websiteData, template });
    navigate('/upload-files'); 
  };

  const isValidDomain = (domain) => {
    const regex = /^(?!:\/\/)([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}$/;
    return regex.test(domain);
};

  const isDomainAndNameValid = domain && websiteName &&savedDomainName;

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
                onBlur={() => { // Optional: You can check domain validity onBlur as well
                  if (!isValidDomain(domain)) {
                    setDomainError(true);
                  }
                  else{
                    setDomainError(false);
                  }
                }}
                placeholder="Enter your website domain"
                className={domainError?"input_name_domain error_domain" :"input_name_domain"}
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
            <button
              className="save_domain_name_button"
              onClick={handleSaveNameAndDomain}
            >
              Save
            </button>
          </div>
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
              className={`template ${template !== '' ? 'selected' : ''}`}
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
