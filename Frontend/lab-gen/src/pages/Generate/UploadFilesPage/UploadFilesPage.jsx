import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../../components/Header/Header';
import { useWebsite } from '../../../Context/WebsiteContext';
import './UploadFilesPage.css';

const UploadFilesPage = () => {
  const navigate = useNavigate();
  const { websiteData, setWebsite } = useWebsite();
  const [formData, setFormData] = useState({
    domain: websiteData.domain || '',
    websiteName: websiteData.websiteName || '',
    components: websiteData.components || [],
    files: {},
    aboutUsContent: '',  // For About Us content
    contactUsContent: '',  // For Contact Us content
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleFileChange = (e, component) => {
    const file = e.target.files[0];
    if (file) {
      setFormData((prev) => ({
        ...prev,
        files: {
          ...prev.files,
          [component]: file,
        },
      }));
    }
  };

  const handleDownload = (component) => {
    const link = document.createElement('a');
    link.href = `/path/to/template/${component}-template.xlsx`; // Modify as needed
    link.download = `${component}-template.xlsx`;
    link.click();
  };

  const handleSubmit = () => {
    if (Object.keys(formData.files).length === 0) {
      alert('Please upload all required files!');
      return;
    }

    // If all files are uploaded, you can save the data and navigate
    setWebsite({ ...formData });  // Save the form data
    alert('Website data saved successfully!');
    navigate('/some-other-page');
  };

  return (
    <div>
      <Header title="LabLauncher" />
      <div className="upload_files_main">
        <h2>Upload Files for Each Component</h2>
        <div>First, download the template, fill it in, and upload it.</div>

        {websiteData.components.map((component) => (
          <div key={component} className="file-upload-section">
            <div>
              <strong>{component}</strong>
              <div>
                {/* Special Handling for About Us and Contact Us */}
                {component === 'About Us' || component === 'Contact Us' ? (
                  <textarea
                    name={component}
                    placeholder={`Enter content for ${component}`}
                    value={formData[component]}
                    onChange={handleInputChange}
                  />
                ) : (
                  <button onClick={() => handleDownload(component)}>Download Template</button>
                )}
              </div>
              {/* Display file input for components other than About Us and Contact Us */}
              {(component !== 'About Us' && component !== 'Contact Us') && (
                <input
                  type="file"
                  onChange={(e) => handleFileChange(e, component)}
                />
              )}
            </div>
          </div>
        ))}

        <div>
          <button onClick={handleSubmit}>Submit</button>
        </div>
      </div>
    </div>
  );
};

export default UploadFilesPage;
