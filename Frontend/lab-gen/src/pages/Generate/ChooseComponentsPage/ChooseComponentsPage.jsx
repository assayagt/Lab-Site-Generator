import React from "react";
import useChooseComponents from "./useChooseComponents";
import Tamplate from "../../../images/tamplate.svg";
import "./ChooseComponentsPage.css";
import ErrorPopup from "../../../components/Popups/ErrorPopup";
const ChooseComponentsPage = () => {
  const {
    domain,
    websiteName,
    components,
    template,
    removeParticipant,
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
    handleAboutUsChange,
    about_usSave,
    contactUs_usSave,
    saveAboutUs,
    saveContactUs,
    contactUsData,
    handleContactUsChange,
    handleSubmit,
    participants,
    degreeOptions,
    showAddForm,
    setShowAddForm,
    newParticipant,
    handleInputChangeParticipant,
    addParticipant,
    toggleLabManager,
    toggleAlumni,
    handleParticipantChange,
    componentsSaved,
    handleGenerate,
    addParticipantGen,
    isComponentsSaved,
    errorMessage,
    setErrorMessage,
    handleSveTemplate,
    isTempSaved,
    setTempSaved,
    mediaSaveStatus,
    buttonText,
    setButtonText,
    showTransferPopup,
    setShowTransferPopup,
    setNewCreatorEmail,
    newCreatorEmail,
    confirmQuitAsCreator,
    newRoleAfterResignation,
    setNewRoleAfterResignation,
  } = useChooseComponents();

  return (
    <div className="choose_components_main">
      {step === 1 && (
        <div className="intro_card">
          <h2>Get Started</h2>
          <label>Enter your website domain:</label>
          <input
            placeholder="www.example.com"
            type="text"
            value={domain}
            onChange={handleDomainChange}
            className={
              domainError
                ? "input_name_domain error_domain"
                : "input_name_domain"
            }
            onBlur={() => {
              if (!isValidDomain(domain)) {
                setDomainError(true);
              } else {
                setDomainError(false);
              }
            }}
          />
          {domainError && (
            <p className="error_message">
              Please enter a valid domain name (e.g., example.com)
            </p>
          )}
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

              <li
                onClick={() =>
                  setShowContentSidebar(
                    !showContentSidebar &&
                      websiteData.created &&
                      componentsSaved
                  )
                }
              >
                Manage Content ▼
              </li>

              {showContentSidebar && (
                <ul className="content-submenu">
                  <li
                    className={step === 6 ? "selected" : ""}
                    onClick={() => setStep(6)}
                  >
                    Information
                  </li>
                  {components?.includes("About Us") && (
                    <li
                      className={step === 7 ? "selected" : ""}
                      onClick={() => setStep(7)}
                    >
                      About Us
                    </li>
                  )}
                  {components?.includes("Contact Us") && (
                    <li
                      className={step === 8 ? "selected" : ""}
                      onClick={() => setStep(8)}
                    >
                      Contact Us
                    </li>
                  )}
                  {components?.includes("Lab Members") && (
                    <li
                      className={step === 9 ? "selected" : ""}
                      onClick={() => setStep(9)}
                    >
                      Lab Members
                    </li>
                  )}
                  <div className="generate_section_button">
                    <button
                      className="generate_button"
                      onClick={handleGenerate}
                    >
                      Generate Website
                    </button>
                  </div>
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
                    className={`input_name_domain ${
                      domainError ? "error_domain" : "edit"
                    }`}
                    id="domainInput"
                    disabled
                    placeholder="www.example.com" // Necessary for floating label effect
                    onBlur={() => {
                      if (!isValidDomain(domain)) {
                        setDomainError(true);
                      } else {
                        setDomainError(false);
                      }
                    }}
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
                  <button
                    className="save_domain_name_button"
                    onClick={handleSaveNameAndDomain}
                  >
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
                    checked={components?.includes("About Us")}
                    onChange={() => handleComponentChange("About Us")}
                  />
                  About Us
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={components?.includes("Lab Members")}
                    onChange={() => handleComponentChange("Lab Members")}
                  />
                  Lab Members
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={components?.includes("Contact Us")}
                    onChange={() => handleComponentChange("Contact Us")}
                  />
                  Contact Us
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={components?.includes("Publications")}
                    onChange={() => handleComponentChange("Publications")}
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
                    {isComponentsSaved ? "Saved" : "Save Components"}
                  </button>
                )}
              </div>
            )}

            {step === 4 && (
              <div className="template_section">
                <h2>Choose a Template</h2>
                <div className="template_section_choose">
                  <img
                    className={`template ${template !== "" ? "selected" : ""}`}
                    src={Tamplate}
                    alt="Template"
                    onClick={() => handleTemplateClick("template1")}
                  />
                  <button
                    className="save_template_button"
                    onClick={handleSveTemplate}
                  >
                    {isTempSaved ? "Saved" : "Save Template"}
                  </button>
                </div>
              </div>
            )}
            {step === 5 && (
              <div className="file-upload-item">
                <div className="media_section">
                  <h2 className="file-upload_title">Media</h2>
                  <div className="media_item">
                    <label className="media_label">
                      Logo
                      <input
                        className="media_input"
                        type="file"
                        onChange={(e) => handleFileChange(e, "logo")}
                      />
                    </label>
                    <button
                      type="button"
                      className="media_button"
                      onClick={(e) => {
                        e.preventDefault(); // ✅ this prevents the page from reloading
                        handleSubmit("logo");
                      }}
                    >
                      {mediaSaveStatus.logo ? "Saved" : "Save"}
                    </button>
                  </div>
                  <div className="media_item">
                    <label className="media_label">
                      Home Page Photo
                      <input
                        className="media_input"
                        type="file"
                        onChange={(e) => handleFileChange(e, "homepagephoto")}
                      />
                    </label>

                    <button
                      className="media_button"
                      type="button"
                      onClick={(e) => {
                        e.preventDefault(); // ✅ prevent default form behavior
                        handleSubmit("homepagephoto");
                      }}
                    >
                      {mediaSaveStatus.homepagephoto ? "Saved" : "Save"}
                    </button>
                  </div>
                </div>
              </div>
            )}
            {step === 6 && (
              <div className="creator_info_card">
                <h2>Creator Information</h2>
                {/* <label>Full Name</label> */}
                <input
                  type="text"
                  value={participants[0]?.fullName || ""}
                  onChange={(e) =>
                    handleParticipantChange(0, "fullName", e.target.value)
                  }
                  className="input_creator_info"
                  placeholder="Your full name"
                />

                {/* <label>Email</label> */}
                <input
                  type="text"
                  value={
                    participants[0]?.email ||
                    sessionStorage.getItem("userEmail")
                  }
                  className="input_creator_info"
                  disabled
                />

                {/* <label>Degree</label> */}
                <select
                  name="degree"
                  value={participants[0]?.degree || ""}
                  onChange={(e) =>
                    handleParticipantChange(0, "degree", e.target.value)
                  }
                  className="input_creator_info"
                >
                  <option value="">Select Degree</option>
                  {degreeOptions.map((degree, index) => (
                    <option key={index} value={degree}>
                      {degree}
                    </option>
                  ))}
                </select>

                <button
                  className="about_contact_button"
                  onClick={() => setButtonText("Saved")}
                >
                  {buttonText}
                </button>
              </div>
            )}
            {step === 7 && (
              <div className="file-upload-item">
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
                  {about_usSave != "" ? (
                    <button
                      className="about_contact_button"
                      onClick={saveAboutUs}
                    >
                      Saved
                    </button>
                  ) : (
                    <button
                      className="about_contact_button"
                      onClick={saveAboutUs}
                    >
                      Save
                    </button>
                  )}
                </div>
              </div>
            )}

            {step === 8 && (
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

                  {contactUs_usSave != "" ? (
                    <button
                      className="about_contact_button"
                      onClick={saveContactUs}
                    >
                      Saved
                    </button>
                  ) : (
                    <button
                      className="about_contact_button"
                      onClick={saveContactUs}
                    >
                      Save
                    </button>
                  )}
                </div>
              </div>
            )}
            <ErrorPopup
              message={errorMessage}
              onClose={() => setErrorMessage("")}
            />

            {step === 9 && (
              <div className="file-upload-item">
                <h3 className="file-upload_title">Lab Members</h3>

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
                          {!websiteData.generated && <th>Remove</th>}{" "}
                          {/* Show column only if site is not generated */}
                        </tr>
                      </thead>
                      <tbody>
                        {/* First row: Logged-in user (cannot be deleted) */}
                        <tr>
                          <td></td>
                          <td>
                            <input
                              type="text"
                              value={participants[0]?.fullName || ""}
                              onChange={(e) =>
                                handleParticipantChange(
                                  0,
                                  "fullName",
                                  e.target.value
                                )
                              }
                              className="input_parti"
                              placeholder="Name"
                            />
                          </td>
                          <td>
                            {participants[0]?.email ||
                              sessionStorage.getItem("userEmail")}
                          </td>
                          <td>
                            <select
                              name="degree"
                              value={participants[0]?.degree || ""}
                              onChange={(e) =>
                                handleParticipantChange(
                                  0,
                                  "degree",
                                  e.target.value
                                )
                              }
                              className="input_parti"
                            >
                              <option value="">Select Degree</option>
                              {degreeOptions.map((degree, index) => (
                                <option key={index} value={degree}>
                                  {degree}
                                </option>
                              ))}
                            </select>
                          </td>
                          <td>
                            <input type="checkbox" checked={true} disabled />
                          </td>
                          <td>
                            <input type="checkbox" checked={true} disabled />
                          </td>
                          <td></td> {/* Empty cell to align delete icons */}
                        </tr>

                        {/* Additional participants */}
                        {participants.slice(1).map((participant, index) => (
                          <tr key={index}>
                            <td></td>
                            <td>
                              <input
                                className="input_parti"
                                placeholder="Full Name"
                                type="text"
                                value={participant.fullName}
                                onChange={(e) =>
                                  handleParticipantChange(
                                    index + 1,
                                    "fullName",
                                    e.target.value
                                  )
                                }
                              />
                            </td>
                            <td>
                              <input
                                className="input_parti"
                                placeholder="Email"
                                type="text"
                                value={participant.email || ""}
                                onChange={(e) =>
                                  handleParticipantChange(
                                    index + 1,
                                    "email",
                                    e.target.value
                                  )
                                }
                              />
                            </td>
                            <td>
                              <select
                                className="input_parti"
                                name="degree"
                                value={participant.degree}
                                onChange={(e) =>
                                  handleParticipantChange(
                                    index + 1,
                                    "degree",
                                    e.target.value
                                  )
                                }
                              >
                                <option value="">Select Degree</option>
                                {degreeOptions.map((degree, i) => (
                                  <option key={i} value={degree}>
                                    {degree}
                                  </option>
                                ))}
                              </select>
                            </td>
                            <td>
                              <input
                                type="checkbox"
                                checked={participant.isLabManager}
                                onChange={(e) =>
                                  handleParticipantChange(
                                    index + 1,
                                    "isLabManager",
                                    !participant.isLabManager
                                  )
                                }
                              />
                            </td>
                            <td>
                              <input type="checkbox" disabled />
                            </td>
                            <td>
                              {/* Delete button (only before website is generated) */}
                              {!websiteData.generated && (
                                <button
                                  className="delete-button"
                                  onClick={() => removeParticipant(index + 1)}
                                >
                                  🗑️
                                </button>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>

                    {/* "+" Button to add new participants */}
                    <button className="add-row-button" onClick={addParticipant}>
                      + Add Member
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
                                disabled={
                                  participant.email ===
                                  sessionStorage.getItem("userEmail")
                                }
                                onChange={() => toggleLabManager(index)}
                              />
                            </td>
                            <td>
                              <input
                                type="checkbox"
                                checked={participant.alumni}
                                onChange={() => toggleAlumni(index)}
                                disabled={
                                  participant.email ===
                                  sessionStorage.getItem("userEmail")
                                }
                              />
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>

                    {/* "Add Participant" button opens the modal */}
                    <button
                      className="add-row-button"
                      onClick={() => setShowAddForm(true)}
                    >
                      + Add Member
                    </button>

                    {/* Modal Popup Form */}
                    {showAddForm && (
                      <div
                        className="modal-overlay"
                        onClick={() => setShowAddForm(false)}
                      >
                        <div
                          className="modal-content"
                          onClick={(e) => e.stopPropagation()}
                        >
                          <h3>Add New Participant</h3>
                          <label>
                            Participant's full name:
                            <input
                              type="text"
                              placeholder="Full Name"
                              name="fullName"
                              value={newParticipant.fullName}
                              onChange={handleInputChangeParticipant}
                              className="modal-content-item"
                            />
                          </label>

                          <label>
                            Participant's email:
                            <input
                              type="text"
                              placeholder="Email"
                              name="email"
                              value={newParticipant.email}
                              onChange={handleInputChangeParticipant}
                              className="modal-content-item"
                            />
                          </label>

                          <label>
                            Participant's degree:
                            <select
                              name="degree"
                              value={newParticipant.degree}
                              onChange={handleInputChangeParticipant}
                            >
                              <option value="">Select Degree</option>
                              {degreeOptions.map((degree, index) => (
                                <option key={index} value={degree}>
                                  {degree}
                                </option>
                              ))}
                            </select>
                          </label>

                          <div className="modal-buttons">
                            <button
                              onClick={() => {
                                setShowAddForm(false);
                                addParticipantGen();
                              }}
                            >
                              Save
                            </button>
                            <button
                              className="cancel-button"
                              onClick={() => setShowAddForm(false)}
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
      {showTransferPopup && (
        <div
          className="modal-overlay"
          onClick={() => setShowTransferPopup(false)}
        >
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Transfer Ownership</h3>
            <select
              onChange={(e) => setNewCreatorEmail(e.target.value)}
              value={newCreatorEmail}
              className="modal-content-item"
            >
              <option value="">Select a participant</option>
              {participants
                .filter((p) => p.email !== sessionStorage.getItem("userEmail"))
                .map((p, index) => (
                  <option key={index} value={p.email}>
                    {p.fullName} ({p.email})
                  </option>
                ))}
            </select>
            <label>
              Select your new role:
              <select
                value={newRoleAfterResignation}
                onChange={(e) => setNewRoleAfterResignation(e.target.value)}
                className="modal-content-item"
              >
                <option value="manager">Manager</option>
                <option value="member">Member</option>
                <option value="alumni">Alumni</option>
              </select>
            </label>
            <div className="modal-buttons">
              <button
                className="cancel-button"
                onClick={() => setShowTransferPopup(false)}
              >
                Cancel
              </button>
              <button onClick={confirmQuitAsCreator}>Confirm</button>
            </div>
          </div>
        </div>
      )}
      <ErrorPopup message={errorMessage} onClose={() => setErrorMessage("")} />
    </div>
  );
};

export default ChooseComponentsPage;
