import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Use useNavigate instead of useHistory

const ChooseComponentsPage = () => {
  const [components, setComponents] = useState([]);
  const [template, setTemplate] = useState('');
  const navigate = useNavigate(); // Use useNavigate

  const handleComponentChange = (component) => {
    setComponents((prev) => {
      if (prev.includes(component)) {
        return prev.filter((item) => item !== component);
      }
      return [...prev, component];
    });
  };

  const handleTemplateClick = (templateName) => {
    setTemplate(templateName);
  };

  const handleContinue = () => {
    if (components.length === 0 || !template) {
      alert('Please select components and a template!');
      return;
    }
    navigate('/upload-files'); // Use navigate to go to the next page
  };

  return (
    <div>
      <h2>Choose Components</h2>
      <div>
        <label>
          <input
            type="checkbox"
            onChange={() => handleComponentChange('Header')}
          />
          Header
        </label>
        <label>
          <input
            type="checkbox"
            onChange={() => handleComponentChange('Footer')}
          />
          Footer
        </label>
        <label>
          <input
            type="checkbox"
            onChange={() => handleComponentChange('Sidebar')}
          />
          Sidebar
        </label>
      </div>

      <h3>Choose a Template</h3>
      <div>
        <img
          src="template1.jpg"
          alt="Template 1"
          onClick={() => handleTemplateClick('Template 1')}
        />
        <img
          src="template2.jpg"
          alt="Template 2"
          onClick={() => handleTemplateClick('Template 2')}
        />
      </div>

      <button onClick={handleContinue}>Continue</button>
    </div>
  );
};

export default ChooseComponentsPage;
