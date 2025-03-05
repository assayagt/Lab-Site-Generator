// import React, { useState, useEffect } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { useWebsite } from '../../../Context/WebsiteContext';
// import './ChooseComponentsPage.css';
// import Tamplate from "../../../images/tamplate.svg";
// import { createCustomSite, changeComponents, changeDomain, changeName } from '../../../services/Generator';
// import { getAllAlumni,getAllLabManagers,getAllLabMembers,createNewSiteManager, removeSiteManager,addLabMember,setSiteContactInfo, setSiteAboutUs ,saveLogo,saveHomePicture,addAlumni} from '../../../services/Generator';

// const ChooseComponentsPage = () => {
//   const navigate = useNavigate();
//   const { websiteData, setWebsite } = useWebsite();
//   const [domain, setDomain] = useState(websiteData.domain || '');
//   const [websiteName, setWebsiteName] = useState(websiteData.websiteName || '');
//   const [components, setComponents] = useState(websiteData.components || []);
//   const [template, setTemplate] = useState(websiteData.template || '');
//   const [isChanged, setIsChanged] = useState(false);
//   const [domainError, setDomainError] = useState(false);
//   const [hasContinued, setHasContinued] = useState(false);  
//   const [step, setStep] = useState(!domain? 1:3);
//   const [saved, setSaved] = useState(false);
//   const [showContentSidebar, setShowContentSidebar] = useState(false);

//   const [initialDomain, setInitialDomain] = useState(websiteData.domain || ''); 
//   const [initialWebsiteName, setInitialWebsiteName] = useState(websiteData.websiteName || ''); 
//   const [formData, setFormData] = useState({
//     domain: websiteData.domain || '',
//     websiteName: websiteData.websiteName || '',
//     components: websiteData.components || [],
//     files: {},
//     publicationsFile: null,
//     participantsFile: null,
//     logo: null,
//     homepagephoto: null,
//   });

//   const [participants, setParticipants] = useState([]);
//   const degreeOptions = ["Ph.D.", "M.Sc.",  "B.Sc.", "Postdoc"];
//   const [selectedComponent, setSelectedComponent] = useState('AboutUs');  // Default to About Us
//   const [showAddForm, setShowAddForm] = useState(false);
//   const [newParticipant, setNewParticipant] = useState({
//     fullName: '',
//     email:'',
//     degree: '',
//     isLabManager: false
//   });

//   const [aboutUsContent, setAboutUsContent] = useState(() => {
//     return sessionStorage.getItem('AboutUs') || ''; // Load from sessionStorage initially
//   });

//   const [contactUsData, setContactUsData] = useState(() => {
//     const savedData = sessionStorage.getItem('ContactUs');
//     return savedData ? JSON.parse(savedData) : { email: '', phoneNumber: '', address: '' };
//   });
//   const [about_usSave, setAboutUsSaved] = useState(false);
//   const [contactUs_usSave, setcontactUs] = useState(false);



  
//   useEffect(() => {
//     if (sessionStorage.getItem('isLoggedIn') !== 'true') {
//       navigate("/");
//     }
//   }, [navigate]);

//   const handleContinue = async() => {
//     if (!domain || !websiteName) {
//       alert("Please enter a domain and website name");
//       return;
//     }
//     let data = await createCustomSite(domain, websiteName, components, template);
//     if (data.response === "true") {
//       setWebsite({ 
//         ...websiteData, 
//         domain,
//         websiteName,
//         components,
//         template, 
//         created: true  // Update the created field
//       });
//       setHasContinued(true); // Set hasContinued to true
//       setIsChanged(false); // Reset the change state after continuing
//       setStep(2);
//     }
//   };

//   const handleDomainChange = (event) => {
//     setDomain(event.target.value);
//     setIsChanged(true); // Mark as changed when domain is modified
//   };

//   const handleNameChange = (event) => {
//     setWebsiteName(event.target.value);
//     setIsChanged(true); // Mark as changed when websiteName is modified
//   };

//   const handleComponentChange = (component) => {
//     setComponents(prevComponents =>
//       prevComponents.includes(component)
//         ? prevComponents.filter(item => item !== component)
//         : [...prevComponents, component]
//     );
//     setIsChanged(true);
//   };

//   const handleTemplateClick = (templateName) => {
//     setTemplate(templateName === template ? '' : templateName);
//     setIsChanged(true);
//   };

//   const isValidDomain = (domain) => {
//     const regex = /^(?!:\/\/)([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}$/;
//     return regex.test(domain);
//   };
//   const handleSaveComponents = async() => {
//     if (components.length === 0) {
//       alert('Please select components');
//       return;
//     }

//     let data = await changeComponents(domain, components);
//     if (data.response === "true") {
//       console.log(components);
//       setWebsite({ ...websiteData, components });
//       setSaved(true);
//       alert('Components saved successfully!');
//       setIsChanged(false); // Reset the change state after saving components
//     }
//     else{
//       console.log(data);
//     }
//   };

//   const handleSaveNameAndDomain = async () => {
//     if (domain !== initialDomain) {
//       if (!isValidDomain(domain)) {
//         setDomainError(true);
//         return;
//       }
//       let data = await changeDomain(initialDomain, domain);
//       if (data) {
//         setWebsite({ ...websiteData, domain });
//         setInitialDomain(domain); 
//         setIsChanged(false); // Mark as changed when domain is modified
//       }
//     }
//     if (websiteName !== initialWebsiteName) {
//       let data = await changeName(domain, websiteName); 
//       if (data) {
//         setWebsite({ ...websiteData, websiteName });
//         setInitialWebsiteName(websiteName); 
//         setIsChanged(false); // Mark as changed when websiteName is modified
//       }
//     }
//   };

//     const handleSubmit = async (component) => {
//       const component_new = component.replace(" ", '').toLowerCase();
  
//       const formDataToSend = new FormData();
//       formDataToSend.append('domain', formData.domain);
//       formDataToSend.append('website_name', formData.websiteName);
      
//       if (formData.files[component_new]) {
//         formDataToSend.append(component_new, formData.files[component_new]);
//       }
  
//       try {
//         const response = await fetch('http://127.0.0.1:5000/api/uploadFile', {
//           method: 'POST',
//           body: formDataToSend,
//         });
//         const data = await response.json();
//         if (response.ok) {
//           alert($'{component} data saved successfully!');
//           setWebsite({ ...formData });
//           if (websiteData.generated) {
        
//             const saveLogoResponse = await saveLogo(sessionStorage.getItem("sid"), websiteData.domain);
//             console.log(saveLogoResponse);
//             const savePhotoResponse = await saveHomePicture(sessionStorage.getItem("sid"), websiteData.domain);
//             console.log(savePhotoResponse)
//         }
//         } else {
//           alert('Error: ' + data.error);
//         }
//       } catch (error) {
//         alert('Error: ' + error.message);
//       }
//     };

//     const handleFileChange = (e, component) => {
//       const file = e.target.files[0];
//       if (file) {
//         setFormData((prev) => ({
//           ...prev,
//           files: {
//             ...prev.files,
//             [component]: file,
//           },
//         }));
//       }
//     };
  

//   const MediaForm = () => (
//     <div className="file-upload-item">
//       <div className="file-upload_title">Media</div>
//       <div>
//         <div>
//           Logo
//           <input
//             className="media_input"
//             type="file"
//             onChange={(e) => handleFileChange(e, 'logo')}
//           />
//           <button
//             className="media_button"
//             onClick={() => handleSubmit('logo')}
//           >
//             Save
//           </button>
//         </div>
//         <div>
//           Home Page Photo
//           <input
//             className="media_input"
//             type="file"
//             onChange={(e) => handleFileChange(e, 'homepagephoto')}
//           />
//           <button
//             className="media_button"
//             onClick={() => handleSubmit('homepagephoto')}
//           >
//             Save
//           </button>
//         </div>
//       </div>
//     </div>
//   );


//   return (
//     <div className="choose_components_main">
//       {step === 1 &&(
//         <div className="intro_card">
//           <h2>Get Started</h2>
//           <label>Enter your website domain:</label>
//           <input
//             type="text"
//             value={domain}
//             onChange={handleDomainChange}
//             className={domainError ? "input_name_domain error_domain" : "input_name_domain"}
//               onBlur={() => {
//               if (!isValidDomain(domain)) {
//                 setDomainError(true);
//               } else {
//                 setDomainError(false);
//               }
//             }}
//           />
//           <label>Enter your website name:</label>
//           <input
//             type="text"
//             value={websiteName}
//             onChange={handleNameChange}
//             className={"input_name_domain"}
//           />
//           <button className="continue_button" onClick={handleContinue}>
//             Continue
//           </button>
//         </div>
//       )}
  
//       {step >= 2 && (
//         <div className="main_layout">
//           {/* Sidebar is always visible when step >= 2 */}
//           <div className="sidebar">
//             <ul>
//               <li onClick={() => setStep(2)}>Domain & Name</li>
//               <li onClick={() => setStep(3)}>Choose Components</li>
//               <li onClick={() => setStep(4)}>Choose Template</li>
//               <li onClick={() => setStep(5)}>Upload Media</li> 
//               {/* Manage Content (Expands Below) */}
//         <li onClick={() => setShowContentSidebar(!showContentSidebar)}>
//           Manage Content ▼
//         </li>

//         {/* Expanded Content Options */}
//         {showContentSidebar && (
//           <ul className="content-submenu">
//             <li onClick={() => setStep(6)}>About Us</li>
//             <li onClick={() => setStep(7)}>Contact Us</li>
//             <li onClick={() => setStep(8)}>Participants</li>
//             <li onClick={() => setStep(9)}>Publications</li>
//           </ul>
//         )}
//             </ul>
//           </div>
  
//           {/* Render the selected content */}
//           <div className="content">
//           {step === 2 && (
//             <div className="domain_section">
//               <h2>Edit Domain And Website Name:</h2>
              
//               <div className="input_container">
//                 <input
//                   type="text"
//                   value={domain}
//                   onChange={(e) => setDomain(e.target.value)}
//                   className={input_name_domain ${domainError ? "error_domain" : "edit"}}
//                   id="domainInput"
//                   placeholder=" " // Necessary for floating label effect
//                 />
//                 <label htmlFor="domainInput" className="floating_label">
//                   Enter domain name
//                 </label>
//               </div>

//               <div className="input_container">
//                 <input
//                   type="text"
//                   value={websiteName}
//                   onChange={(e) => setWebsiteName(e.target.value)}
//                   className="input_name_domain edit"
//                   id="websiteNameInput"
//                   placeholder=" "
//                 />
//                 <label htmlFor="websiteNameInput" className="floating_label">
//                   Enter website name
//                 </label>
//               </div>

//               {websiteData.created && (
//                 <button className="save_domain_name_button" onClick={handleSaveNameAndDomain}>
//                   Save
//                 </button>
//               )}
//             </div>
//           )}
  
//             {step === 3 && (
//               <div className="components_section">
//                 <h2>Choose Components</h2>
//                 <label>
//               <input
//                 type="checkbox"
//                 checked={components.includes('About Us')}
//                 onChange={() => handleComponentChange('About Us')}
//               />
//               About Us
//             </label>
//             <label>
//               <input
//                 type="checkbox"
//                 checked={components.includes('Participants')}
//                 onChange={() => handleComponentChange('Participants')}
//               />
//               Participants
//             </label>
//             <label>
//               <input
//                 type="checkbox"
//                 checked={components.includes('Contact Us')}
//                 onChange={() => handleComponentChange('Contact Us')}
//               />
//               Contact Us
//             </label>
//             <label>
//               <input
//                 type="checkbox"
//                 checked={components.includes('Publications')}
//                 onChange={() => handleComponentChange('Publications')}
//               />
//               Publications
//             </label>
//             <label className="disabled">
//               <input type="checkbox" disabled />
//               News
//             </label>
//             <label className="disabled">
//               <input type="checkbox" disabled />
//               Media
//             </label>
//             <label className="disabled">
//               <input type="checkbox" disabled />
//               Page for each participant
//             </label>

//             {websiteData.created && (
//               <button
//                 className="save_domain_name_button"
//                 onClick={handleSaveComponents}
//               >
//                 Save Components
//               </button>
//             )}
//               </div>
//             )}
  
//             {step === 4 && (
//               <div className="template_section">
//                 <h2>Choose a Template</h2>
//                 <img
//                   className={template ${template !== '' ? 'selected' : ''}}
//                   src={Tamplate}
//                   alt="Template"
//                   onClick={() => handleTemplateClick('Template 1')}
//                 />
//               </div>
//             )}
//             {step === 5 && (
//               <MediaForm/>
//             )}

            
//           </div>
//         </div>
//       )}
//     </div>
//   );
  
// };

// export default ChooseComponentsPage;