import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Use useNavigate instead of useHistory
import Header from '../../../components/Header/Header';
import Tamplate from "../../../images/tamplate.svg"
import "./ChooseComponentsPage.css";

const ChooseComponentsPage = () => {
  const [components, setComponents] = useState([]);
  const [template, setTemplate] = useState('');
  const [domain, setDomain] = useState('');
  const [websiteName, setWebsiteName] = useState(''); // Corrected state for website name
  const [saved, setSaved] = useState(false); // New state to track if components are saved

  const navigate = useNavigate(); // Use useNavigate

  // Handle checkbox changes for components
  const handleComponentChange = (component) => {
    setComponents((prev) => {
      if (prev.includes(component)) {
        return prev.filter((item) => item !== component);
      }
      return [...prev, component];
    });
  };

  // Handle template selection
  const handleTemplateClick = (templateName) => {
    setTemplate(templateName);
  };

  // Handle domain change
  const handleDomainChange = (event) => {
    setDomain(event.target.value);
  };
  
  // Handle website name input change
  const handleNameChange = (event) => {
    setWebsiteName(event.target.value);
  };

  const handleSaveComponents = () => {
    if (components.length === 0 ) {
      alert('Please select components');
      return;
    }
    setSaved(true); 
    alert('Components saved successfully!');
  };

  // Continue to the next page
  const handleContinue = () => {
    if (components.length === 0 || !template) {
      alert('Please select components and a template!');
      return;
    }
    navigate('/upload-files'); // Use navigate to go to the next page
  };

  return (
    <div>
      <Header title="LabLauncher" />
      <div className = "choose_components_main">
        <div className='grid1'>
            <div className='create_custom_website'>
              <div className='website_domain_name'>
                <label>Enter your website domain:</label>
                <input
                  type="text"
                  value={domain} 
                  onChange={handleDomainChange} 
                  placeholder="Enter your website domain"
                  className='input_name_domain'
                />
              </div>
              <div className='website_domain_name'>
                <label>Enter your website name:</label>
                <input
                  type="text"
                  value={websiteName} 
                  onChange={handleNameChange} 
                  placeholder="Enter your website name"
                  className='input_name_domain'
                />
              </div>
              <button className='save_domain_name_button'>Save</button>
            </div>
          <div className='create_custom_website'>
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
                onChange={() => handleComponentChange('Participants')}
              />
              Publications
            </label>
            <label className='disabled'>
              <input
                type="checkbox"
                disabled
              />
              News
            </label>
            <label className='disabled'>
              <input
                type="checkbox"
                disabled
              />
              Media
            </label>
            <label className='disabled'>
              <input
                type="checkbox"
                disabled
              />
              Page for each participant
            </label>
            <div>
              <button  className='save_domain_name_button' onClick={handleSaveComponents}>Save Components</button>
            </div>
          </div>
        </div>
      <div>
        <h3>Choose a Template</h3>
        <div>
            <img className='tamplate'
              src= {Tamplate}
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
