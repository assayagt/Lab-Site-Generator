import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
    AboutUs: '', // About Us content
    ContactUs: '', // Contact Us content
    email: '', // Added email state
    phoneNumber: '', // Added phone number state
    address: '',
    publicationsFile: null,
    participantsFile: null,
  });

  useEffect(() => {
    if (sessionStorage.getItem('isLoggedIn') !== 'true') {
      navigate('/');
    }
  }, [navigate]);

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
    const component_new = component.replace(" ", '').toLowerCase();

    // if (!formData.files[component_new] && !formData[`${component_new}` && component_new !== 'contactus']) {
    //   alert(`Please upload a file or provide content for ${component}`);
    //   return;
    // }

    const formDataToSend = new FormData();
    formDataToSend.append('domain', formData.domain);
    formDataToSend.append('website_name', formData.websiteName);
    if (component === 'Contact Us') {
      const contactUsData = {
        phone: formData.phoneNumber,
        address: formData.address,
        email: formData.email,
      };
      formDataToSend.append('contactus_content', JSON.stringify(contactUsData)); // Send the contact data as a JSON string
    }


    else if (formData.files[component_new]) {
      formDataToSend.append(component_new, formData.files[component_new]);
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
        {websiteData.components
            .filter(component => websiteData.generated ? component !== 'Publications' : true)
            .map((component) => (
            <div key={component} className="file-upload-section">
              <div className="file-upload-item">
                <div className="file-upload_title">{component}</div>
                <div>
                  {component === 'About Us' ? (
                    <div className="about_contact_section">
                      <input
                        className="about_contact_input"
                        name="AboutUs"
                        placeholder={`Enter content for ${component}`}
                        value={formData.AboutUs}
                        onChange={handleInputChange}
                      />
                      <button
                        className="about_contact_button"
                        onClick={() => handleSubmit(component)}
                      >
                        Save
                      </button>
                    </div>
                  ) : (component !== 'Contact Us' && websiteData.generated===false) ? (
                    <button
                      className="downloadTemplate"
                      onClick={() => handleDownload(component)}
                    >
                      Download Template
                    </button>
                  ) : (
                    <div> </div> // This block is for Contact Us
                  )}
                </div>

                {component === 'Contact Us' && (
                  <div className="contact_us_section">
                    <input
                      className="contact_us_input"
                      name="email"
                      placeholder="Enter your email"
                      value={formData.email}
                      onChange={handleInputChange}
                    />
                    <input
                      className="contact_us_input"
                      name="phoneNumber"
                      placeholder="Enter your phone number"
                      value={formData.phoneNumber}
                      onChange={handleInputChange}
                    />
                    <input
                      className="contact_us_input"
                      name="address"
                      placeholder="Enter your address"
                      value={formData.address}
                      onChange={handleInputChange}
                    />
                  
                    <button
                      className="about_contact_button"
                      onClick={() => handleSubmit(component)}
                    >
                      Save
                    </button>
                  </div>
                )}

                 {component === 'Participants' && (websiteData.generated) && (
                    <div>
                      hello
                    </div>
                 )
                    }           
                {(component !== 'About Us' && component !== 'Contact Us' && websiteData.generated===false)  && (
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
