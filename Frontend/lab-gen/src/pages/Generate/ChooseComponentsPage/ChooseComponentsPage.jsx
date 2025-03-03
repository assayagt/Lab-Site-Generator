import React from 'react';
import useChooseComponents from './useChooseComponents';
import Tamplate from "../../../images/tamplate.svg";
import './ChooseComponentsPage.css';

const ChooseComponentsPage = () => {
  const {
    domain,
    websiteName,
    components,
    template,
    isChanged,
    domainError,
    step,
    setStep,
    showContentSidebar,
    setShowContentSidebar,
    handleContinue,
    handleDomainChange,
    handleNameChange,
    handleComponentChange,
    handleTemplateClick,
    handleSaveComponents,
    handleSaveNameAndDomain,
    isValidDomain,
    setDomainError,
    websiteData,
    handleFileChange,
    aboutUsContent,
    setAboutUsContent,
    handleAboutUsChange,
    about_usSave,
    contactUs_usSave,
    saveAboutUs,
    saveContactUs,
    contactUsData,
    handleContactUsChange,
    handleDownload,
    handleSubmit,
    participants,
    setParticipants,
    degreeOptions,
    selectedComponent,
    setSelectedComponent,
    handleNavClick,
    showAddForm,
    setShowAddForm,
    newParticipant,
    setNewParticipant,
    handleInputChangeParticipant,
    addParticipant,
    toggleLabManager,
    toggleAlumni,
    handleParticipantChange,
    componentsSaved,handleGenerate
  } = useChooseComponents();
  


  

  const MediaForm = () => (
    <div className="file-upload-item">
      <div className="media_section">
      <h2 className="file-upload_title">Media</h2>
        <div className="media_item">
            <label className="media_label">Logo
              <input
                  className="media_input"
                  type="file"
                  onChange={(e) => handleFileChange(e, 'logo')}
              />
            </label>
          <button
              className="media_button"
              onClick={() => handleSubmit('logo')}
            >
              Save
            </button>
        </div>
        <div className="media_item">         
           <label className="media_label">Home Page Photo
           <input
              className="media_input"
              type="file"
              onChange={(e) => handleFileChange(e, 'homepagephoto')}
            />
           </label>
            
          <button
              className="media_button"
              onClick={() => handleSubmit('homepagephoto')}
            >
              Save
            </button>
        </div>
      </div>
    </div>
  );

  return (
    <div className="choose_components_main">
      {step === 1 &&(
        <div className="intro_card">
          <h2>Get Started</h2>
          <label>Enter your website domain:</label>
          <input
            type="text"
            value={domain}
            onChange={handleDomainChange}
            className={domainError ? "input_name_domain error_domain" : "input_name_domain"}
              onBlur={() => {
              if (!isValidDomain(domain)) {
                setDomainError(true);
              } else {
                setDomainError(false);
              }
            }}
          />
          <label>Enter your website name:</label>
          <input
            type="text"
            value={websiteName}
            onChange={handleNameChange}
            className={"input_name_domain"}
          />
          <button className="continue_button" onClick={handleContinue}>
            Continue
          </button>
        </div>
      )}
  
      {step >= 2 && (
        <div className="main_layout">
          {/* Sidebar is always visible when step >= 2 */}
          <div className="sidebar">
            <ul>
              <li 
                className={step === 2 ? "selected" : ""} 
                onClick={() => setStep(2)}
              >
                Domain & Name
              </li>
              <li 
                className={step === 3 ? "selected" : ""} 
                onClick={() => setStep(3)}
              >
                Choose Components
              </li>
              <li 
                className={step === 4 ? "selected" : ""} 
                onClick={() => setStep(4)}
              >
                Choose Template
              </li>
              <li 
                className={step === 5 ? "selected" : ""} 
                onClick={() => setStep(5)}
              >
                Upload Media
              </li>

              <li onClick={() => setShowContentSidebar(!showContentSidebar && websiteData.created && componentsSaved)}>
                Manage Content ▼
              </li>
              
              {showContentSidebar && (
                <ul className="content-submenu">
                  {components.includes("About Us") && (
                    <li className={step === 6 ? "selected" : ""} onClick={() => setStep(6)}>
                      About Us
                    </li>
                  )}
                  {components.includes("Contact Us") && (
                    <li className={step === 7 ? "selected" : ""} onClick={() => setStep(7)}>
                      Contact Us
                    </li>
                  )}
                  {components.includes("Participants") && (
                    <li className={step === 8 ? "selected" : ""} onClick={() => setStep(8)}>
                      Participants
                    </li>
                  )}
                <li className="generate_section">
                  <button className="generate_button" onClick={handleGenerate}>
                    Generate Website
                  </button>
                </li>
              </ul>
            )}
            </ul>
          </div>
  
          {/* Render the selected content */}
          <div className="content">
          {step === 2 && (
            <div className="domain_section">
              <h2>Edit Domain And Website Name:</h2>
              
              <div className="input_container">
                <input
                  type="text"
                  value={domain}
                  onChange={handleDomainChange}
                  className={`input_name_domain ${domainError ? "error_domain" : "edit"}`}
                  id="domainInput"
                  placeholder=" " // Necessary for floating label effect
                />
                <label htmlFor="domainInput" className="floating_label">
                  Enter domain name
                </label>
              </div>

              <div className="input_container">
                <input
                  type="text"
                  value={websiteName}
                  onChange={handleNameChange}
                  className="input_name_domain edit"
                  id="websiteNameInput"
                  placeholder=" "
                />
                <label htmlFor="websiteNameInput" className="floating_label">
                  Enter website name
                </label>
              </div>

              {websiteData.created && (
                <button className="save_domain_name_button" onClick={handleSaveNameAndDomain}>
                  Save
                </button>
              )}
            </div>
          )}
  
            {step === 3 && (
              <div className="components_section">
                <h2>Choose Components</h2>
                <label>
              <input
                type="checkbox"
                checked={components.includes('About Us')}
                onChange={() => handleComponentChange('About Us')}
              />
              About Us
            </label>
            <label>
              <input
                type="checkbox"
                checked={components.includes('Participants')}
                onChange={() => handleComponentChange('Participants')}
              />
              Participants
            </label>
            <label>
              <input
                type="checkbox"
                checked={components.includes('Contact Us')}
                onChange={() => handleComponentChange('Contact Us')}
              />
              Contact Us
            </label>
            <label>
              <input
                type="checkbox"
                checked={components.includes('Publications')}
                onChange={() => handleComponentChange('Publications')}
              />
              Publications
            </label>
            <label className="disabled">
              <input type="checkbox" disabled />
              News
            </label>
            <label className="disabled">
              <input type="checkbox" disabled />
              Media
            </label>
            <label className="disabled">
              <input type="checkbox" disabled />
              Page for each participant
            </label>

            {websiteData.created && (
              <button
                className="save_domain_name_button"
                onClick={handleSaveComponents}
              >
                Save Components
              </button>
            )}
              </div>
            )}
  
            {step === 4 && (
              <div className="template_section">
                <h2>Choose a Template</h2>
                <img
                  className={`template ${template !== '' ? 'selected' : ''}`}
                  src={Tamplate}
                  alt="Template"
                  onClick={() => handleTemplateClick('Template 1')}
                />
              </div>
            )}
            {step === 5 && (
              <MediaForm/>
            )}
            {step === 6 &&
            (<div className="file-upload-item">
              <div className="about_contact_section">
              <h3 className="file-upload_title">About Us</h3>
              <div className="input_container">
                <textarea
                  className="about_contact_input textarea"
                  name="AboutUs"
                  placeholder="Enter content for About Us"
                  value={aboutUsContent}
                  onChange={handleAboutUsChange}
                />
                <label htmlFor="aboutUsInput" className="floating_label">
                  Enter content for About Us
                </label>
                </div>
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
            </div>)}

            {step === 7 &&
            (
              <div className="file-upload-item">
             
              <div className="contact_us_section">
              <h3 className="file-upload_title">Contact Us</h3>
              <div className="input_container">
                <input
                  className="contact_us_input"
                  name="email"
                  placeholder="Enter your email"
                  value={contactUsData.email}
                  onChange={handleContactUsChange}
                />
                <label htmlFor="emailInput" className="floating_label">
                    Enter your email
                </label>
                </div>
                <div className="input_container">
                <input
                  className="contact_us_input"
                  name="phoneNumber"
                  placeholder="Enter your phone number"
                  value={contactUsData.phoneNumber}
                  onChange={handleContactUsChange}
                />
                 <label htmlFor="phoneInput" className="floating_label">
                    Enter your phone number
                </label>
                </div>
                <div className="input_container">
                <input
                  className="contact_us_input"
                  name="address"
                  placeholder="Enter your address"
                  value={contactUsData.address}
                  onChange={handleContactUsChange}
                />
                 <label htmlFor="addressInput" className="floating_label">
                  Enter your address
                </label>
                </div>
    
    {contactUs_usSave!=''? (
              <button
              className="about_contact_button"
              onClick={saveContactUs}
            >
              Saved
            </button>
            ):(
              <button
              className="about_contact_button"
              onClick={saveContactUs}
            >
              Save
            </button>
            )
            }
                
              </div>
            </div>
            )
            }
{step === 8 && 
  (<div className="file-upload-item">
    <div className="file-upload_title">Participants</div>

    {!websiteData.generated ? (
      // Table format before website is generated
      <div>
        <table className="participants-table">
          <thead>
            <tr>
              <th></th> {/* Placeholder for "+" button */}
              <th>Full Name</th>
              <th>Email</th>
              <th>Degree</th>
              <th>Manager</th>
              <th>Site Creator</th>
            </tr>
          </thead>
          <tbody>
            {/* First row: Logged-in user */}
            <tr>
              <td></td>
              <td>
                <input
                  type="text"
                  value={participants[0]?.fullName || ''}
                  onChange={(e) => handleParticipantChange(0, 'fullName', e.target.value)}
                  className='input_parti'
                  placeholder='Name'
                />
              </td>
              <td>{participants[0]?.email || sessionStorage.getItem("userEmail")}</td>
              <td>
                <select
                  name="degree"
                  value={participants[0]?.degree || ''}
                  onChange={(e) => handleParticipantChange(0, 'degree', e.target.value)}
                  className='input_parti'
                  
                >
                  <option value="">Select Degree</option>
                  {degreeOptions.map((degree, index) => (
                    <option key={index} value={degree}>{degree}</option>
                  ))}
                </select>
              </td>
              <td>
                <input type="checkbox" checked={true} disabled />
              </td>
              <td>
                <input type="checkbox" checked={true} disabled />
              </td>
            </tr>

            {/* Additional participants */}
            {participants.slice(1).map((participant, index) => (
              <tr key={index}>
                <td></td> {/* Empty cell for consistency */}
                <td>
                  <input
                    className='input_parti'
                    placeholder='Full Name'
                    type="text"
                    value={participant.fullName}
                    onChange={(e) => handleParticipantChange(index+1, 'fullName', e.target.value)}
                  />
                </td>
                <td>
                  <input
                    className='input_parti'
                    placeholder='Email'
                    type="text"
                    value={participant.email||''}
                    onChange={(e) => handleParticipantChange(index+1, 'email', e.target.value)}
                  />
                </td>
                <td>
                  <select
                    className='input_parti'
                    name="degree"
                    value={participant.degree}
                    onChange={(e) => handleParticipantChange(index+1, 'degree', e.target.value)}
                  >
                    <option value="">Select Degree</option>
                    {degreeOptions.map((degree, i) => (
                      <option key={i} value={degree}>{degree}</option>
                    ))}
                  </select>
                </td>
                <td>
                  <input
                    type="checkbox"
                    checked={participant.isLabManager}
                    onChange={(e) => handleParticipantChange(index+1, 'isLabManager', !participant.isLabManager)}
                  />
                </td>
                <td>
                  <input type="checkbox" disabled />
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* "+" Button to add new participants */}
        <button className="add-row-button" onClick={addParticipant}>
          + Add Row
        </button>
      </div>
    ) : (
      // When website is generated
      <div>
        <table className="participants-table">
          <thead>
            <tr>
              <th>Full Name</th>
              <th>Degree</th>
              <th>Manager</th>
              <th>Alumni</th>
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
                <td>
                  <input
                    type="checkbox"
                    checked={participant.alumni}
                    onChange={() => toggleAlumni(index)}
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* "+" Button to add an empty row */}
        <button className="add-row-button" onClick={addParticipant}>
          + Add Participant
        </button>
      </div>
    )}
  </div>)
}

            
          </div>
        </div>
      )}
    </div>
  );
  
};

export default ChooseComponentsPage;
