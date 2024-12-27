import React, { useState } from 'react';
import Header from '../../../components/Header/Header';
import { useWebsite } from '../../../Context/WebsiteContext';
import './UploadFilesPage.css';

const UploadFilesPage = () => {
  const { websiteData, setWebsite } = useWebsite();
  const [formData, setFormData] = useState({
    domain: websiteData.domain || '',
    websiteName: websiteData.websiteName || '',
    components: websiteData.components || [],
    files: {},
    aboutUsContent: '',  
    contactUsContent: '',  
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
    setWebsite({ ...formData }); 
    alert('Website data saved successfully!');
  };

  return (
    <div>
      <Header title="LabLauncher" />
      <div className="upload_files_page">
        <h2 className='upload_title'> Upload Files for Each Component</h2>
        <div className='upload_instruction'>First, download the template, fill it in, and upload it.</div>
        <div className="upload_files_main">
        {websiteData.components.map((component) => (
          <div key={component} className="file-upload-section">
            <div className = "file-upload-item" >
              <div className = "file-upload_title">{component}</div>
              <div>
                {component === 'About Us' || component === 'Contact Us' ? (
                  <div className = "about_contact_section">
                    <input className = "about_contact_input"
                      name={component}
                      placeholder={`Enter content for ${component}`}
                      value={formData[component]}
                      onChange={handleInputChange}
                    />
                    <button className = "about_contact_button">Save</button>
                  </div>
                ) : (
                  <button onClick={() => handleDownload(component)}>Download Template</button>
                )}
              </div>
              {(component !== 'About Us' && component !== 'Contact Us') && (
                <div>
                  <input
                    type="file"
                    onChange={(e) => handleFileChange(e, component)}
                  />
                  <button onClick={handleSubmit}>Submit</button>
                </div>
              )}
            </div>
          </div>
        ))}

        <div>
          <button >Generate</button>
        </div>
      </div>
    </div>
    </div>
  );
};

export default UploadFilesPage;
