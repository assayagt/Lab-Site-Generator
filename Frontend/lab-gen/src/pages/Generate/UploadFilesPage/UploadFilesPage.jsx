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



  const [selectedComponent, setSelectedComponent] = useState('AboutUs');  // Default to About Us

  const handleNavClick = (componentName) => {
    setSelectedComponent(componentName);
  };


  const [participants, setParticipants] = useState([
    { fullName: "Dr. Alice Johnson", degree: "PhD", isLabManager: true },
    { fullName: "Prof. Brian Smith", degree: "PhD", isLabManager: false },
    { fullName: "Dr. Carmen Li", degree: "MD", isLabManager: false },
    { fullName: "Prof. David Wright", degree: "PhD", isLabManager: false },
    { fullName: "Ms. Emily Davis", degree: "MSc", isLabManager: true }
  ]);

  const [showAddForm, setShowAddForm] = useState(false);
  const [newParticipant, setNewParticipant] = useState({
    fullName: '',
    degree: '',
    isLabManager: false
  });

  const toggleLabManager = index => {
    const newParticipants = participants.map((participant, idx) => {
      if (idx === index) {
        return { ...participant, isLabManager: !participant.isLabManager };
      }
      return participant;
    });
    setParticipants(newParticipants);
  };

  const handleInputChangepart = (e) => {
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






  const AboutUsForm = () => (
    <div className="file-upload-item">
      <div className="file-upload_title">About Us</div>
        <div className="about_contact_section">
                          <input
                            className="about_contact_input"
                            name="AboutUs"
                            placeholder={`Enter content for About Us`}
                            value={formData.AboutUs}
                            onChange={handleInputChange}
                          />
                          <button
                            className="about_contact_button"
                            onClick={() => handleSubmit('About Us')}
                          >
                            Save
                          </button>
        </div>
    </div>
    
  );
  
  const ContactUsForm = () => (
    <div className="file-upload-item">
      <div className="file-upload_title">Contact us</div>
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
                          onClick={() => handleSubmit('Contact Us')}
                        >
                          Save
                        </button>
                      </div>
                      </div>
  );
  
  const PublicationsForm = () => (
    <div className="file-upload-item">
      <div className="file-upload_title">Publications</div>
      <button
         className="downloadTemplate"
                   onClick={() => handleDownload('Publications')}
                   >
                     Download Template
                   </button>
                   <div>
                     <input
                       className="downloadTemplate"
                       type="file"
                       onChange={(e) => handleFileChange(e, 'Publications')}
                     />
                     <button
                       className="downloadTemplate"
                       onClick={() => handleSubmit('Publications')}
                     >
                       Save
                     </button>
                   </div>
    </div>
  );
  
  const ParticipantsForm = () => (
    <div className="file-upload-item">
      <div className="file-upload_title">Participants</div>
      {websiteData.generated &&
      (<div>
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
                               onChange={handleInputChangepart}
                             />
                             <input
                               type="text"
                               placeholder="Degree"
                               name="degree"
                               value={newParticipant.degree}
                               onChange={handleInputChangepart}
                             />
                           <label>
                               Manager
                               <input
                               type="checkbox"
                                 name="isLabManager"
                                 checked={newParticipant.isLabManager}
                                 onChange={handleInputChangepart}
                              />
                             </label>
                             <button onClick={addParticipant}>Save</button>
                             <button onClick={() => setShowAddForm(false)}>Cancel</button>
                           </div>
                       ) : (
                           <button onClick={() => setShowAddForm(true)}>+ Add Participant</button>
                         )}
                       </div>)
      }
    </div>
  );
  
  return (

    <div className="container">
    <div className="sidebar">
      <ul>
        <li onClick={() => handleNavClick('AboutUs')}>About Us</li>
        <li onClick={() => handleNavClick('ContactUs')}>Contact Us</li>
        {!websiteData.generated && ( <li onClick={() => handleNavClick('Publications')}>Publications</li>)}
        <li onClick={() => handleNavClick('Participants')}>Participants</li>
      </ul>
    </div>
    <div className="main-content">
      {selectedComponent === 'AboutUs' && <AboutUsForm />}
      {selectedComponent === 'ContactUs' && <ContactUsForm />}
      {selectedComponent === 'Publications' && <PublicationsForm />}
      {selectedComponent === 'Participants' && <ParticipantsForm />}
    </div>
  </div>
  );


  
    // <div>
    //   <div className="upload_files_page">
    //     <h2 className="upload_title">Upload Files for Each Component</h2>
    //     <div className="upload_instruction">
    //       First, download the template, fill it in, and upload it.
    //     </div>
    //     <div className="upload_files_main">
    //     {websiteData.components
    //         .filter(component => websiteData.generated ? component !== 'Publications' : true)
    //         .map((component) => (
    //         <div key={component} className="file-upload-section">
    //           <div className="file-upload-item">
    //             <div className="file-upload_title">{component}</div>
    //             <div>
    //               {component === 'About Us' ? (
    //                 <div className="about_contact_section">
    //                   <input
    //                     className="about_contact_input"
    //                     name="AboutUs"
    //                     placeholder={`Enter content for ${component}`}
    //                     value={formData.AboutUs}
    //                     onChange={handleInputChange}
    //                   />
    //                   <button
    //                     className="about_contact_button"
    //                     onClick={() => handleSubmit(component)}
    //                   >
    //                     Save
    //                   </button>
    //                 </div>
    //               ) : (component !== 'Contact Us' && websiteData.generated===false) ? (
    //                 <button
    //                   className="downloadTemplate"
    //                   onClick={() => handleDownload(component)}
    //                 >
    //                   Download Template
    //                 </button>
    //               ) : (
    //                 <div> </div> // This block is for Contact Us
    //               )}
    //             </div>

    //             {component === 'Contact Us' && (
    //               <div className="contact_us_section">
    //                 <input
    //                   className="contact_us_input"
    //                   name="email"
    //                   placeholder="Enter your email"
    //                   value={formData.email}
    //                   onChange={handleInputChange}
    //                 />
    //                 <input
    //                   className="contact_us_input"
    //                   name="phoneNumber"
    //                   placeholder="Enter your phone number"
    //                   value={formData.phoneNumber}
    //                   onChange={handleInputChange}
    //                 />
    //                 <input
    //                   className="contact_us_input"
    //                   name="address"
    //                   placeholder="Enter your address"
    //                   value={formData.address}
    //                   onChange={handleInputChange}
    //                 />
                  
    //                 <button
    //                   className="about_contact_button"
    //                   onClick={() => handleSubmit(component)}
    //                 >
    //                   Save
    //                 </button>
    //               </div>
    //             )}

    //              {component === 'Participants' && (websiteData.generated) && (
    //                 <div>
    //                 <table className="participants-table">
    //                   <thead>
    //                     <tr>
    //                       <th>Full Name</th>
    //                       <th>Degree</th>
    //                       <th>Manager</th>
    //                     </tr>
    //                   </thead>
    //                   <tbody>
    //                     {participants.map((participant, index) => (
    //                       <tr key={index}>
    //                         <td>{participant.fullName}</td>
    //                         <td>{participant.degree}</td>
    //                         <td>
    //                           <input
    //                             type="checkbox"
    //                             checked={participant.isLabManager}
    //                             onChange={() => toggleLabManager(index)}
    //                           />
    //                         </td>
    //                       </tr>
    //                     ))}
    //                   </tbody>
    //                 </table>
    //                 {showAddForm ? (
    //                   <div>
    //                     <input
    //                       type="text"
    //                       placeholder="Full Name"
    //                       name="fullName"
    //                       value={newParticipant.fullName}
    //                       onChange={handleInputChangepart}
    //                     />
    //                     <input
    //                       type="text"
    //                       placeholder="Degree"
    //                       name="degree"
    //                       value={newParticipant.degree}
    //                       onChange={handleInputChangepart}
    //                     />
    //                     <label>
    //                       Manager
    //                       <input
    //                         type="checkbox"
    //                         name="isLabManager"
    //                         checked={newParticipant.isLabManager}
    //                         onChange={handleInputChangepart}
    //                       />
    //                     </label>
    //                     <button onClick={addParticipant}>Save</button>
    //                     <button onClick={() => setShowAddForm(false)}>Cancel</button>
    //                   </div>
    //                 ) : (
    //                   <button onClick={() => setShowAddForm(true)}>+ Add Participant</button>
    //                 )}
    //               </div>
    //              )
    //                 }           
    //             {(component !== 'About Us' && component !== 'Contact Us' && websiteData.generated===false)  && (
    //               <div>
    //                 <input
    //                   className="downloadTemplate"
    //                   type="file"
    //                   onChange={(e) => handleFileChange(e, component)}
    //                 />
    //                 <button
    //                   className="downloadTemplate"
    //                   onClick={() => handleSubmit(component)}
    //                 >
    //                   Save
    //                 </button>
    //               </div>
    //             )}
    //           </div>
    //         </div>
    //       ))}

    //       <div>
    //         <button onClick={handleGenerate}>Generate</button>
    //       </div>
    //     </div>
    //   </div>
    // </div>
  //);
};

export default UploadFilesPage;
