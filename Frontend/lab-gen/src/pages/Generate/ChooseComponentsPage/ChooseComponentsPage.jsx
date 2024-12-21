import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

const ChooseComponentsPage = () => {
  const [components, setComponents] = useState([]);
  const [template, setTemplate] = useState('');
  const history = useHistory();

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
    history.push('/upload-files');
  };

  const handleBack = () => {
    history.push('/');
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

      <button onClick={handleBack}>Back</button>
      <button onClick={handleContinue}>Continue</button>
    </div>
  );
};

export default ChooseComponentsPage;
