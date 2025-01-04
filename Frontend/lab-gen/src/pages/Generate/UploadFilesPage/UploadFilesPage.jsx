import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useWebsite } from '../../../Context/WebsiteContext';
import './UploadFilesPage.css';

const UploadFilesPage = () => {
  const navigate = useNavigate();
  const { websiteData,setWebsite} = useWebsite();
  const [formData, setFormData] = useState({
    domain: websiteData.domain || '',
    websiteName: websiteData.websiteName || '',
    components: websiteData.components || [],
    files: {},
    AboutUs: '',  
    ContactUs: '',  
    publicationsFile: null,
    participantsFile: null,
    
  });

  useEffect(() => {
    if (sessionStorage.getItem('isLoggedIn')!=='true') {
      navigate("/");
    }
  }, [ navigate]);


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

  const handleSubmit = async (component) => {
    let component_new = component.replace(" ", '')
    if (!formData.files[component_new] && !formData[`${component_new}`]) {
      alert(`Please upload a file or provide content for ${component}`);
      return;
    }
  
    const formDataToSend = new FormData();
    formDataToSend.append('domain', formData.domain);
    formDataToSend.append('website_name', formData.websiteName);
  
    // Ensure the correct content is being appended for each component
    if (formData[`${component_new}`]) {
      console.log(`${component_new.toLowerCase()}_content`)
      formDataToSend.append(`${component_new.toLowerCase()}_content`, formData[component_new]);
    }
  
    if (formData.files[component_new]) {
      formDataToSend.append(component, formData.files[component]);
    }
    
    try {
      const response = await fetch('http://127.0.0.1:5000/api/uploadFile', {
        method: 'POST',
        body: formDataToSend,
      });
      const data = await response.json();
      if (response.ok) {
        alert(`${component} data saved successfully!`);
        setWebsite({ ...formData });
      } else {
        alert('Error: ' + data.error);
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  const handleGenerate = async () => {
    
    try {
      // Call the backend to generate the website
      const response = await fetch('http://127.0.0.1:5000/api/generateWebsite', {
        method: 'POST',
       
      });
      const data = await response.json();
      if (response.ok) {
        console.log(data.message);
        alert(data);
        
      } else {
        alert('Error: ' + data.error);
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };

  return (
    <div>
      <div className="upload_files_page">
        <h2 className="upload_title">Upload Files for Each Component</h2>
        <div className="upload_instruction">
          First, download the template, fill it in, and upload it.
        </div>
        <div className="upload_files_main">
          {websiteData.components.map((component) => (
            <div key={component} className="file-upload-section">
              <div className="file-upload-item">
                <div className="file-upload_title">{component}</div>
                <div>
                  {component === 'About Us' || component === 'Contact Us' ? (
                    <div className="about_contact_section">
                      <input
                        className="about_contact_input"
                        name={`${component.replace(" ", '')}`}
                        placeholder={`Enter content for ${component}`}
                        value={formData[`${component.replace(" ", '')}`]}
                        onChange={handleInputChange}
                      />
                      <button
                        className="about_contact_button"
                        onClick={() => handleSubmit(component)}
                      >
                        Save
                      </button>
                    </div>
                  ) : (
                    <button
                      className="downloadTemplate"
                      onClick={() => handleDownload(component)}
                    >
                      Download Template
                    </button>
                  )}
                </div>

                {(component === 'Publications' || component === 'Participants') && (
                  <div>
                    <input
                      className="downloadTemplate"
                      type="file"
                      onChange={(e) => handleFileChange(e, component)}
                    />
                    <button
                      className="downloadTemplate"
                      onClick={() => handleSubmit(component)}
                    >
                      Save
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}

          <div>
            <button onClick={handleGenerate}>Generate</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadFilesPage;
