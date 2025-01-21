import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useWebsite } from '../../../Context/WebsiteContext';
import './UploadFilesPage.css';
import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";
const UploadFilesPage = () => {



  const [participants, setParticipants] = useState([
    { fullName: "Dr. Alice Johnson", degree: "PhD", isLabManager: true },
    { fullName: "Prof. Brian Smith", degree: "PhD", isLabManager: false },
    { fullName: "Dr. Carmen Li", degree: "MD", isLabManager: false },
    { fullName: "Prof. David Wright", degree: "PhD", isLabManager: false },
    { fullName: "Ms. Emily Davis", degree: "MSc", isLabManager: true }
  ]);





  const navigate = useNavigate();
  const { websiteData, setWebsite } = useWebsite();
  const [formData, setFormData] = useState({
    domain: websiteData.domain || '',
    websiteName: websiteData.websiteName || '',
    components: websiteData.components || [],
    files: {},
    publicationsFile: null,
    participantsFile: null,
    logo: null,
    homepagePhoto: null,
  });
  const [selectedComponent, setSelectedComponent] = useState('AboutUs');  // Default to About Us
  const [showAddForm, setShowAddForm] = useState(false);
  const [newParticipant, setNewParticipant] = useState({
    fullName: '',
    degree: '',
    isLabManager: false
  });

  const [aboutUsContent, setAboutUsContent] = useState(() => {
    return sessionStorage.getItem('AboutUs') || ''; // Load from sessionStorage initially
  });

  const [contactUsData, setContactUsData] = useState(() => {
    const savedData = sessionStorage.getItem('ContactUs');
    return savedData ? JSON.parse(savedData) : { email: '', phoneNumber: '', address: '' };
  });


  useEffect(() => {
    if (sessionStorage.getItem('isLoggedIn') !== 'true') {
      navigate('/');
    }
  }, [navigate]);




  const handleNavClick = (componentName) => {
    setSelectedComponent(componentName);
  };




 
  const toggleLabManager = index => {
    const newParticipants = participants.map((participant, idx) => {
      if (idx === index) {
        return { ...participant, isLabManager: !participant.isLabManager };
      }
      return participant;
    });
    setParticipants(newParticipants);
  };

  const handleInputChangeParticipant = (e) => {
    const { name, value, type, checked } = e.target;
    setNewParticipant(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const addParticipant = () => {
    if (newParticipant.fullName && newParticipant.degree) {
      setParticipants([...participants, newParticipant]);
      setNewParticipant({ fullName: '', degree: '', isLabManager: false });
      setShowAddForm(false);
    } else {
      alert("Please fill all fields.");
    }
  };


  const handleAboutUsChange = (e) => {
    setAboutUsContent(e.target.value);
  };

  const saveAboutUs = () => {
    sessionStorage.setItem('AboutUs', aboutUsContent);
    alert('About Us saved in session storage!');
  };

  const handleContactUsChange = (e) => {
    const { name, value } = e.target;
    setContactUsData((prev) => ({
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

    const formDataToSend = new FormData();
    formDataToSend.append('domain', formData.domain);
    formDataToSend.append('website_name', formData.websiteName);
    
    if (formData.files[component_new]) {
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
      const response = await axios.post(`${baseApiUrl}generateWebsite`, {
        domain: formData.domain,
        about_us: aboutUsContent,
        lab_address: contactUsData.address,
        lab_mail:contactUsData.email,
        lab_phone_num:contactUsData.phoneNumber,
      });
      const data =  response.data;
      console.log(data);
      if (data.response==="true") {
        console.log(data.message);
        alert(data);
        sessionStorage.removeItem("AboutUs");
        sessionStorage.removeItem("ContactUs");
      } else {
        alert('Error: ' + data.error);
      }
    } catch (error) {
      alert('Error: ' + error.message);
    }
  };



  const AboutUsForm = () => (
    <div className="file-upload-item">
      <div className="file-upload_title">About Us</div>
      <div className="about_contact_section">
        <input
          className="about_contact_input"
          name="AboutUs"
          placeholder="Enter content for About Us"
          value={aboutUsContent}
          onChange={handleAboutUsChange}
        />
        <button
          className="about_contact_button"
          onClick={saveAboutUs}
        >
          Save
        </button>
      </div>
    </div>
  );
  
  const ContactUsForm = () => (
    <div className="file-upload-item">
      <div className="file-upload_title">Contact Us</div>
      <div className="contact_us_section">
        <input
          className="contact_us_input"
          name="email"
          placeholder="Enter your email"
          value={contactUsData.email}
          onChange={handleContactUsChange}
        />
        <input
          className="contact_us_input"
          name="phoneNumber"
          placeholder="Enter your phone number"
          value={contactUsData.phoneNumber}
          onChange={handleContactUsChange}
        />
        <input
          className="contact_us_input"
          name="address"
          placeholder="Enter your address"
          value={contactUsData.address}
          onChange={handleContactUsChange}
        />
        <button
          className="about_contact_button"
          onClick={() => {
            const contactData = {
              email: contactUsData.email,
              phoneNumber: contactUsData.phoneNumber,
              address: contactUsData.address,
            };
            sessionStorage.setItem('ContactUs', JSON.stringify(contactData));
            alert('Contact Us saved in session storage!');
          }}
        >
          Save
        </button>
      </div>
    </div>
  );
  
  const ParticipantsForm = () => (
    <div className="file-upload-item">
      <div className="file-upload_title">Participants</div>
      {!websiteData.generated ? (
        <div>
          <div>
            <button
              className="downloadTemplate"
              onClick={() => handleDownload('participants')}
            >
              Download Template
            </button>
          </div>
          <div>
            <input
              className="uploadTemplate"
              type="file"
              onChange={(e) => handleFileChange(e, 'participants')}
            />
            <button
              className="uploadTemplateButton"
              onClick={() => handleSubmit('participants')}
            >
              Upload Template
            </button>
          </div>
        </div>
      ) : (
        <div>
          <table className="participants-table">
            <thead>
              <tr>
                <th>Full Name</th>
                <th>Degree</th>
                <th>Manager</th>
              </tr>
            </thead>
            <tbody>
              {participants.map((participant, index) => (
                <tr key={index}>
                  <td>{participant.fullName}</td>
                  <td>{participant.degree}</td>
                  <td>
                    <input
                      type="checkbox"
                      checked={participant.isLabManager}
                      onChange={() => toggleLabManager(index)}
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {showAddForm ? (
            <div>
              <input
                type="text"
                placeholder="Full Name"
                name="fullName"
                value={newParticipant.fullName}
                onChange={handleInputChangeParticipant}
              />
              <input
                type="text"
                placeholder="Degree"
                name="degree"
                value={newParticipant.degree}
                onChange={handleInputChangeParticipant}
              />
              <label>
                Manager
                <input
                  type="checkbox"
                  name="isLabManager"
                  checked={newParticipant.isLabManager}
                  onChange={handleInputChangeParticipant}
                />
              </label>
              <button onClick={addParticipant}>Save</button>
              <button onClick={() => setShowAddForm(false)}>Cancel</button>
            </div>
          ) : (
            <button onClick={() => setShowAddForm(true)}>+ Add Participant</button>
          )}
        </div>
      )}
    </div>
  );


  const MediaForm = () => (
    <div className="file-upload-item">
      <div className="file-upload_title">Media</div>
      <div>
        <div>
          Logo
          <input
            className="media_input"
            type="file"
            onChange={(e) => handleFileChange(e, 'logo')}
          />
          <button
            className="media_button"
            onClick={() => handleSubmit('logo')}
          >
            Save
          </button>
        </div>
        <div>
          Home Page Photo
          <input
            className="media_input"
            type="file"
            onChange={(e) => handleFileChange(e, 'homepagePhoto')}
          />
          <button
            className="media_button"
            onClick={() => handleSubmit('homepagePhoto')}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );


  return (

    <div className="container">
    <div className="sidebar">
      <ul>
        <li onClick={() => handleNavClick('AboutUs')}>About Us</li>
        <li onClick={() => handleNavClick('ContactUs')}>Contact Us</li>
        <li onClick={() => handleNavClick('Participants')}>Participants</li>
        <li onClick={() => handleNavClick('Media')}>Media</li>
      </ul>
      {
        websiteData.generated ? (
          <div>
            <button onClick={console.log("save")}>Save changes</button>
          </div>
        ) : (
          <div>
            <button onClick={handleGenerate}>Generate</button>
          </div>
        )
      }
      
    </div>
    <div className="main-content">
      {selectedComponent === 'AboutUs' && (
    <div className="file-upload-item">
      <div className="file-upload_title">About Us</div>
      <div className="about_contact_section">
        <input
          className="about_contact_input"
          name="AboutUs"
          placeholder="Enter content for About Us"
          value={aboutUsContent}
          onChange={handleAboutUsChange}
        />
        <button
          className="about_contact_button"
          onClick={saveAboutUs}
        >
          Save
        </button>
      </div>
    </div>
  )
    }
      {selectedComponent === 'ContactUs' && 
      (
        <div className="file-upload-item">
          <div className="file-upload_title">Contact Us</div>
          <div className="contact_us_section">
            <input
              className="contact_us_input"
              name="email"
              placeholder="Enter your email"
              value={contactUsData.email}
              onChange={handleContactUsChange}
            />
            <input
              className="contact_us_input"
              name="phoneNumber"
              placeholder="Enter your phone number"
              value={contactUsData.phoneNumber}
              onChange={handleContactUsChange}
            />
            <input
              className="contact_us_input"
              name="address"
              placeholder="Enter your address"
              value={contactUsData.address}
              onChange={handleContactUsChange}
            />
            <button
              className="about_contact_button"
              onClick={() => {
                const contactData = {
                  email: contactUsData.email,
                  phoneNumber: contactUsData.phoneNumber,
                  address: contactUsData.address,
                };
                sessionStorage.setItem('ContactUs', JSON.stringify(contactData));
                alert('Contact Us saved in session storage!');
              }}
            >
              Save
            </button>
          </div>
        </div>
      )
      
      }
      {selectedComponent === 'Participants' && <ParticipantsForm />}
      {selectedComponent === 'Media' && <MediaForm />}
    </div>
  </div>
  );


  
};

export default UploadFilesPage;
