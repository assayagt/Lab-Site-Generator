import React from "react";
import { useState, useEffect } from "react";
import useChooseComponents from "./useChooseComponents";
import Tamplate from "../../../images/tamplate.svg";
import "./ChooseComponentsPage.css";
import ErrorPopup from "../../../components/Popups/ErrorPopup";
import LoadingPopup from "../../../components/Popups/LoadingPopup";
import SuccessPopup from "../../../components/Popups/SuccessPopup";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
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
    isLoading,
    succsessMessage,
    setSuccsessMessage,
    handleGoogleScolarChange,
    googleLink,
    setSave,
    save,
  } = useChooseComponents();

  // Fix leaflet icon issues (put this near the top of the component file)
  L.Marker.prototype.options.icon = L.icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  });

  // Inside the ChooseComponentsPage component definition (add after useChooseComponents hook)
  const [mapCoordinates, setMapCoordinates] = useState(null);

  useEffect(() => {
    const fetchCoordinates = async () => {
      if (!contactUsData.address) return;
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
            contactUsData.address
          )}&format=json`
        );
        const data = await response.json();
        if (data.length > 0) {
          setMapCoordinates({
            lat: parseFloat(data[0].lat),
            lng: parseFloat(data[0].lon),
          });
        }
      } catch (err) {
        console.error("Geocoding error:", err);
      }
    };
    fetchCoordinates();
  }, [contactUsData.address]);

  const LocationSelector = () => {
    useMapEvents({
      click: async (e) => {
        const { lat, lng } = e.latlng;
        setMapCoordinates({ lat, lng });
        try {
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json&accept-language=en`
          );
          const data = await response.json();
          if (data && data.display_name) {
            handleContactUsChange({
              target: { name: "address", value: data.display_name },
            });
          }
        } catch (err) {
          console.error("Reverse geocoding error:", err);
        }
      },
    });
    return null;
  };

  return (
    <div className="choose_components_main">
      {step === 1 && (
        <div className="intro_card">
          <h2>Get Started</h2>
          <label>Enter your website domain:</label>
          <div
            className={`domain-input-group ${
              domainError ? "error_wrapper" : ""
            }`}
          >
            <span className="domain-prefix">lsg.cs.bgu.ac.il/labs/</span>

            <input
              type="text"
              value={domain}
              onChange={handleDomainChange}
              className="input_suffix"
              // className={
              //   domainError
              //     ? "input_name_domain error_domain"
              //     : "input_name_domain"
              // }
              onBlur={() => {
                if (!isValidDomain(domain)) {
                  setDomainError(true);
                } else {
                  setDomainError(false);
                }
              }}
            />
            {domainError && (
              <span className="error-message">Invalid domain</span>
            )}
          </div>

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
                  {components?.includes("Media") && (
                    <li
                      className={step === 10 ? "selected" : ""}
                      onClick={() => setStep(10)}
                    >
                      Upload Pictures
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
                      {websiteData.generated ? save : "Generate Website"}
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
                <label>
                  <input
                    type="checkbox"
                    checked={components?.includes("Media")}
                    onChange={() => handleComponentChange("Media")}
                  />
                  Media
                </label>
                <label>
                  <input
                    type="checkbox"
                    checked={components?.includes("Page for Participant")}
                    onChange={() =>
                      handleComponentChange("Page for Participant")
                    }
                  />
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
                {!websiteData.generated && (
                  <input
                    type="text"
                    value={googleLink}
                    onChange={(e) => handleGoogleScolarChange(e.target.value)}
                    className="input_creator_info"
                    placeholder="Your Google Scholar Profile link"
                  />
                )}
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
                      name="phone_num"
                      placeholder="Enter your phone number"
                      value={contactUsData.phone_num}
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
                  <div className="map_container">
                    <MapContainer
                      center={
                        mapCoordinates
                          ? [mapCoordinates.lat, mapCoordinates.lng]
                          : [31.2615, 34.7978] // BGU as default
                      }
                      zoom={15}
                      style={{
                        height: "300px",
                        width: "95%",
                        marginTop: "20px",
                        borderRadius: "10px",
                      }}
                    >
                      <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        attribution="&copy; OpenStreetMap contributors"
                      />
                      {mapCoordinates && (
                        <Marker
                          position={[mapCoordinates.lat, mapCoordinates.lng]}
                        />
                      )}
                      <LocationSelector />
                    </MapContainer>
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
                                  title="Remove participant"
                                >
                                  <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    viewBox="0 0 16 16"
                                  >
                                    <path
                                      fill="currentColor"
                                      d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
                                    />
                                    <path
                                      fill="currentColor"
                                      d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
                                    />
                                  </svg>
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
                              className="modal-content-item-select"
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
                              className="x-button"
                              onClick={() => setShowAddForm(false)}
                            >
                              X
                            </button>
                            <button
                              className="modal-buttons-add_member"
                              onClick={() => {
                                setShowAddForm(false);
                                addParticipantGen();
                              }}
                            >
                              Save
                            </button>
                          </div>
                        </div>
                        <SuccessPopup
                          message={succsessMessage}
                          onClose={() => setSuccsessMessage("")}
                        />
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
            {step === 10 && (
              <div className="file-upload-item">
                <div className="media_section">
                  <h3 className="file-upload_title">Gallery Images</h3>
                  <div className="media_item">
                    <label className="media_label">
                      Upload Images
                      <input
                        className="media_input"
                        type="file"
                        multiple
                        accept="image/*"
                        onChange={(e) => handleFileChange(e, "gallery")}
                      />
                    </label>
                    <button
                      className="media_button"
                      type="button"
                      onClick={(e) => {
                        e.preventDefault();
                        handleSubmit("gallery");
                      }}
                    >
                      {mediaSaveStatus.gallery ? "Saved" : "Save"}
                    </button>
                  </div>
                </div>
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
      {isLoading && (
        <LoadingPopup message="Generating your website, please wait..." />
      )}
    </div>
  );
};

export default ChooseComponentsPage;
