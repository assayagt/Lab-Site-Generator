import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useWebsite } from '../../../Context/WebsiteContext';
import './UploadFilesPage.css';
import axios from "axios";
import { getAllAlumni,getAllLabManagers,getAllLabMembers,createNewSiteManager, removeSiteManager,addLabMember,setSiteContactInfo, setSiteAboutUs ,saveLogo,saveHomePicture} from '../../../services/Generator';
const baseApiUrl = "http://127.0.0.1:5000/api/";
const UploadFilesPage = () => {


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


  const [participants, setParticipants] = useState([]);
  const degreeOptions = ["P.hD.", "M.Sc.",  "B.Sc.", "Postdoc"];


  const [selectedComponent, setSelectedComponent] = useState('AboutUs');  // Default to About Us
  const [showAddForm, setShowAddForm] = useState(false);
  const [newParticipant, setNewParticipant] = useState({
    fullName: '',
    email:'',
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
  const [about_usSave, setAboutUsSaved] = useState(false);
  const [contactUs_usSave, setcontactUs] = useState(false);


  useEffect(() => {
    const fetchParticipants = async () => {
      let domain = websiteData.domain;
      try {
        const [managers, members, alumni] = await Promise.all([
          getAllLabManagers(domain),
          getAllLabMembers(domain),
          getAllAlumni(domain),
        ]);
  
      
        const allParticipants = [
          ...managers.map((participant) => ({ ...participant, isLabManager: true })),
          ...members.map((participant) => ({ ...participant, isLabManager: false })),
          ...alumni.map((participant) => ({ ...participant, isLabManager: false }))
        ];
  
        setParticipants(allParticipants);
      } catch (err) {
        console.error('Error fetching participants:', err);
      }
    };
  
    fetchParticipants();
  }, [websiteData.domain]);


  useEffect(() => {
    if (sessionStorage.getItem('isLoggedIn') !== 'true') {
      navigate('/');
    }
  }, [navigate]);




  const handleNavClick = (componentName) => {
    setSelectedComponent(componentName);
  };


  const toggleLabManager = async (index) => {
    const updatedParticipants = [...participants];
    const participant = updatedParticipants[index];
  
    const email = participant.email;
    const isLabManager = participant.isLabManager;
  
    
    try {
      if (!isLabManager) {
        
        let data = await createNewSiteManager(sessionStorage.getItem("sid"), email, websiteData.domain);
        if(data.response==="true"){
          participant.isLabManager = !isLabManager;
          setParticipants(updatedParticipants);
        }
      } else {
        // Removing as a site manager
        let data =await removeSiteManager(sessionStorage.getItem("sid"), email, websiteData.domain);
        if(data.response==="true"){
          participant.isLabManager = !isLabManager;
          setParticipants(updatedParticipants);
        }
      }
  
    
    } catch (error) {
      console.error('Error toggling lab manager:', error);
      alert('An error occurred while updating the lab manager.');
    }
  };
  
  const handleInputChangeParticipant = (e) => {
    const { name, value, type, checked } = e.target;
    setNewParticipant(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const addParticipant = async () => {
    if (newParticipant.fullName && newParticipant.degree && newParticipant.email) {
     
      try {
        const response = await addLabMember(
          sessionStorage.getItem("sid"), // Manager's User ID, assuming this is stored in sessionStorage
          newParticipant.email, // Email of the new participant
          newParticipant.fullName, // Full name of the new participant
          newParticipant.degree, // Degree of the new participant
          websiteData.domain // Domain of the lab
        );
  
        if (response.response === 'true') {
          alert('Lab member added successfully');
        
          setParticipants([...participants, { ...newParticipant, isLabManager: false }]);
          setNewParticipant({ fullName: '', degree: '', email: '' }); 
          setShowAddForm(false);
        } else {
          alert(`Error: ${response.message}`);
        }
      } catch (error) {
        console.error('Error adding participant:', error);
        alert('An error occurred while adding the lab member.');
      }
    } else {
      alert("Please fill all fields.");
    }
  };

  


  const handleAboutUsChange = (e) => {
    setAboutUsSaved(false);
    setAboutUsContent(e.target.value);
  };

  const saveAboutUs = async () => {
    sessionStorage.setItem('AboutUs', aboutUsContent);
    if (websiteData.generated) {
      const response = await setSiteAboutUs(sessionStorage.getItem('sid'), websiteData.domain, aboutUsContent);
      if (response.response === 'true') {
        alert('About Us saved successfully');
      } else {
        alert('Error updating About Us: ' + response.message);
      }
    } 
      setAboutUsSaved(true);
    
  };

  const handleContactUsChange = (e) => {
    setcontactUs(false);
    const { name, value } = e.target;
    setContactUsData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const saveContactUs = async () => {
    sessionStorage.setItem('ContactUs', JSON.stringify(contactUsData));
    if (websiteData.generated) {
      const response = await setSiteContactInfo(sessionStorage.getItem('sid'), websiteData.domain, contactUsData.address, contactUsData.email, contactUsData.phoneNumber);
      if (response.response === 'true') {
        alert('Contact information saved successfully');
      } else {
        alert('Error updating Contact Information: ' + response.message);
      }
    } 
      setcontactUs(true);
    

  }
  
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
        if (websiteData.generated) {
      
          const saveLogoResponse = await saveLogo(sessionStorage.getItem("sid"), sessionStorage.getItem("domain"));
          console.log(saveLogoResponse);
          const savePhotoResponse = await saveHomePicture((sessionStorage.getItem("sid"), sessionStorage.getItem("domain")));
          console.log(savePhotoResponse)
      }
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
            <div className='add-participant-form'>
              <label>Participant's full name:</label>
              <input
                type="text"
                placeholder="Full Name"
                name="fullName"
                value={newParticipant.fullName}
                onChange={handleInputChangeParticipant}
              />
              <label>Participant's degree:</label>
              <select name="degree" value={newParticipant.degree} onChange={handleInputChangeParticipant}>
                <option value="">Select Degree</option>
                {degreeOptions.map((degree, index) => (
                  <option key={index} value={degree}>{degree}</option>
                ))}
              </select>
              <label>Participant's email:</label>
              <input
                type="text"
                placeholder="Email"
                name="email"
                value={newParticipant.email}
                onChange={handleInputChangeParticipant}
              />
            
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
        {about_usSave!=''? (
          <button
          className="about_contact_button"
          onClick={saveAboutUs}
        >
          Saved
        </button>
        ):(
          <button
          className="about_contact_button"
          onClick={saveAboutUs}
        >
          Save
        </button>
        )
        }
        
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
              onClick={saveContactUs}
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
