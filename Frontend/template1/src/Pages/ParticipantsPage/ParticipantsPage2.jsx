// ParticipantsPage.jsx
import React, { useState, useEffect } from "react";
import "./ParticipantsPage2.css";
import accountIcon from "../../images/account_avatar.svg";
import {
  getAllAlumni,
  getAllLabManagers,
  getAllLabMembers,
  addLabMemberFromWebsite,
  createNewSiteManagerFromLabWebsite,
  addAlumniFromLabWebsite,
  removeManagerPermission,
  removeAlumniFromLabWebsite,
} from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import ErrorPopup from "../../Components/PopUp/ErrorPopup";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";
import { FaLinkedin, FaEnvelope, FaExternalLinkAlt } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { useWebsite } from "../../Context/WebsiteContext";

const ParticipantsPage = () => {
  const { websiteData, setWebsite } = useWebsite();
  const navigate = useNavigate();
  const [selectedDegree, setSelectedDegree] = useState("All");
  const [participants, setParticipants] = useState([]);
  const [alumni, setAlumni] = useState([]);
  const [loading, setLoading] = useState(true);
  const { editMode } = useEditMode();
  const [showAddForm, setShowAddForm] = useState(false);
  const [popupMessage, setPopupMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [newParticipant, setNewParticipant] = useState({
    fullName: "",
    email: "",
    degree: "",
    isManager: false,
    isAlumni: false,
  });

  const degreeOrder = {
    "Ph.D.": 1,
    "M.Sc.": 2,
    "B.Sc.": 3,
    "Research Assistant": 4,
    "Faculty Member": 5,
  };

  const staticDegreeOptions = [
    "Ph.D.",
    "M.Sc.",
    "B.Sc.",
    "Research Assistant",
    "Faculty Member",
    "Alumni",
  ];

  const degreeOptions = staticDegreeOptions;

  const fetchParticipants = async () => {
    setLoading(true);
    try {
      const domain = sessionStorage.getItem("domain");

      const [managers, members, alumniData] = await Promise.all([
        getAllLabManagers(domain),
        getAllLabMembers(domain),
        getAllAlumni(domain),
      ]);

      // Tag each manager and member properly
      const taggedManagers = managers.map((m) => ({
        ...m,
        isManager: true,
        isAlumni: false,
      }));
      const taggedMembers = members.map((m) => ({
        ...m,
        isManager: false,
        isAlumni: false,
      }));

      // Merge them into a single participants array
      setParticipants([...taggedManagers, ...taggedMembers]);

      // Mark alumni explicitly too
      const taggedAlumni = (alumniData || []).map((a) => ({
        ...a,
        isAlumni: true,
        isManager: false,
      }));
      setAlumni(taggedAlumni);
    } catch (err) {
      console.error("Error fetching participants:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchParticipants();
  }, []);

  const groupedParticipants = participants.reduce((acc, participant) => {
    const { degree } = participant;
    if (!acc[degree]) acc[degree] = [];
    acc[degree].push(participant);
    return acc;
  }, {});

  const editModeOption = (member) => {
    return (
      editMode &&
      !member.is_creator && (
        <div className="member-card__edit-options">
          <label className="edit-option">
            <input
              type="checkbox"
              checked={member.isManager}
              onChange={() => handleToggleManager(member)}
            />
            <span>Manager</span>
          </label>
          <label className="edit-option">
            <input
              type="checkbox"
              checked={member.isAlumni}
              onChange={() => handleToggleAlumni(member)}
            />
            <span>Alumni</span>
          </label>
        </div>
      )
    );
  };

  const handleToggleManager = async (member) => {
    const userId = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    try {
      if (!member.isManager) {
        // Promote to manager
        const response = await createNewSiteManagerFromLabWebsite(
          userId,
          member.email,
          domain
        );
        if (response?.response === "true") {
          setParticipants((prev) =>
            prev.map((p) =>
              p.email === member.email ? { ...p, isManager: !p.isManager } : p
            )
          );
        } else {
          setErrorMessage("Failed to promote to manager: " + response?.message);
        }
      } else {
        // Demote from manager
        const response = await removeManagerPermission(
          userId,
          member.email,
          domain
        );
        if (response?.manager_email) {
          setParticipants((prev) =>
            prev.map((p) =>
              p.email === member.email ? { ...p, isManager: !p.isManager } : p
            )
          );
        } else {
          setErrorMessage(
            "Failed to remove manager permission: " + response?.message
          );
        }
      }
    } catch (err) {
      setErrorMessage("Error toggling manager: " + err);
    }
  };

  const handleToggleAlumni = async (member) => {
    const userId = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    try {
      if (!member.isAlumni) {
        // Promote to alumni
        const response = await addAlumniFromLabWebsite(
          userId,
          member.email,
          domain
        );
        if (response?.response === "true") {
          if (!member.isAlumni) {
            setParticipants(
              (prev) => prev.filter((p) => p.email !== member.email) // remove from participants
            );
            setAlumni((prev) => [
              ...prev,
              { ...member, isAlumni: true, isManager: false },
            ]);
          }
        } else {
          setErrorMessage("Failed to promote to alumni: " + response?.message);
        }
      } else {
        const response = await removeAlumniFromLabWebsite(
          sessionStorage.getItem("sid"),
          member.email,
          sessionStorage.getItem("domain")
        );

        if (response?.response === "true") {
          setAlumni((prev) => prev.filter((p) => p.email !== member.email)); // Remove from alumni

          setParticipants((prev) => [
            ...prev,
            { ...member, isAlumni: false }, // Add back to participants
          ]);
        }
      }
    } catch (err) {
      setErrorMessage("Error toggling alumni:", err);
    }
  };

  const filteredParticipants =
    selectedDegree === "All"
      ? groupedParticipants
      : selectedDegree === "Alumni"
      ? { Alumni: alumni }
      : { [selectedDegree]: groupedParticipants[selectedDegree] || [] };

  const handleInputChangeParticipant = (e) => {
    const { name, value, type, checked } = e.target;
    setNewParticipant((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const NavigateProfile = (email) => {
    if (websiteData.components.includes("Page for Participant")) {
      navigate(`/participant/${encodeURIComponent(email)}`);
    }
  };

  const handleAddParticipant = async () => {
    const { fullName, email, degree, isManager, isAlumni } = newParticipant;
    const userId = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    if (!fullName || !email || !degree) {
      setErrorMessage("Please fill in all fields.");
      return;
    }

    try {
      const addMemberResponse = await addLabMemberFromWebsite(
        userId,
        email,
        fullName,
        degree,
        domain
      );

      if (addMemberResponse?.response !== "true") {
        setErrorMessage(
          "Failed to add lab member: " + addMemberResponse?.message
        );
        return;
      } else {
        setPopupMessage("Participant added successfully! ");
      }

      if (isManager) {
        const managerResponse = await createNewSiteManagerFromLabWebsite(
          userId,
          email,
          domain
        );
        if (managerResponse?.response !== "true") {
          setErrorMessage("Failed to add manager: " + managerResponse?.message);
          return;
        }
      }

      if (isAlumni) {
        const alumniResponse = await addAlumniFromLabWebsite(
          userId,
          email,
          domain
        );
        if (alumniResponse?.response !== "true") {
          setErrorMessage(
            "Failed to mark as alumni: " + alumniResponse?.message
          );
          return;
        }
      }

      setNewParticipant({
        fullName: "",
        email: "",
        degree: "",
        isManager: false,
        isAlumni: false,
      });
      setShowAddForm(false);
      fetchParticipants(); // Refresh full list from backend
    } catch (error) {
      setErrorMessage("Error adding participant:" + error);
    }
  };

  if (loading) {
    return (
      <div className="members-loading">
        <div className="loading-spinner"></div>
        <p>Loading lab members...</p>
      </div>
    );
  }

  return (
    <div className="members-page">
      <div className="members-page__container">
        <div className="members-page__header">
          <h1 className="members-page__title">Lab Members</h1>

          <div className="members-page__controls">
            <div className="members-page__filter">
              <select
                id="degree-filter"
                value={selectedDegree}
                onChange={(e) => setSelectedDegree(e.target.value)}
                className="members-page__select"
              >
                <option value="All">All Members</option>
                {degreeOptions.map((degree) => (
                  <option key={degree} value={degree}>
                    {degree}
                  </option>
                ))}
              </select>
            </div>

            {editMode && (
              <button
                className="members-page__add-button"
                onClick={() => setShowAddForm(true)}
                aria-label="Add member"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="20"
                  height="20"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                <span>Add Member</span>
              </button>
            )}
          </div>
        </div>

        <div className="members-page__content">
          {Object.entries(filteredParticipants).map(([degree, members]) => (
            <div key={degree} className="degree-section">
              <h2 className="degree-section__title">{degree}</h2>

              {members.length === 0 ? (
                <div className="degree-section__empty">
                  No participants found for this category.
                </div>
              ) : (
                <div className="member-grid">
                  {members.map((member) => (
                    <div key={member.email} className="member-card">
                      <div className="member-card__photo">
                        <img
                          src={
                            member.profile_picture
                              ? member.profile_picture
                              : accountIcon
                          }
                          alt="User"
                          className="member-photo-img"
                        />
                      </div>
                      <div className="member-card__content">
                        <div className="member-card__header">
                          <h3 className="member-card__name">
                            {member.fullName}
                          </h3>
                          {websiteData.components.includes(
                            "Page for Participant"
                          ) && (
                            <FaExternalLinkAlt
                              className="profile-link-icon_2"
                              onClick={() => NavigateProfile(member.email)}
                              title="View Profile"
                            />
                          )}
                        </div>

                        <div className="member-card__bio">
                          {member.bio ||
                            "Research interests and bio information will appear here."}
                        </div>

                        <div className="member-card__contact">
                          <a
                            href={`mailto:${member.email}`}
                            className="member-card__email"
                          >
                            <FaEnvelope />
                            <span>{member.email}</span>
                          </a>

                          {member.linkedin_link && (
                            <a
                              href={member.linkedin_link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="member-card__linkedin"
                            >
                              <FaLinkedin />
                              <span>LinkedIn</span>
                            </a>
                          )}
                        </div>

                        {editModeOption(member)}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}

          {/* Show Alumni section when "All" is selected or when Alumni is specifically selected */}
          {(selectedDegree === "All" || selectedDegree === "Alumni") &&
            alumni.length > 0 && (
              <div className="degree-section">
                <h2 className="degree-section__title">Alumni</h2>
                <div className="member-grid">
                  {alumni.map((member) => (
                    <div
                      key={member.email}
                      className="member-card member-card--alumni"
                    >
                      <div className="member-card__photo">
                        <img
                          src={
                            member.profile_picture
                              ? member.profile_picture
                              : accountIcon
                          }
                          alt="User"
                          className="member-photo-img"
                        />
                      </div>
                      <div className="member-card__content">
                        <div className="member-card__header">
                          <h3 className="member-card__name">
                            {member.fullName}
                            <span className="member-card__degree">
                              [{member.degree}]
                            </span>
                          </h3>
                          {websiteData.components.includes(
                            "Page for Participant"
                          ) && (
                            <FaExternalLinkAlt
                              className="profile-link-icon"
                              onClick={() => NavigateProfile(member.email)}
                              title="View Profile"
                            />
                          )}
                        </div>

                        <div className="member-card__bio">
                          {member.bio || "Alumni information will appear here."}
                        </div>

                        <div className="member-card__contact">
                          <a
                            href={`mailto:${member.email}`}
                            className="member-card__email"
                          >
                            <FaEnvelope />
                            <span>{member.email}</span>
                          </a>

                          {member.linkedin_link && (
                            <a
                              href={member.linkedin_link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="member-card__linkedin"
                            >
                              <FaLinkedin />
                              <span>LinkedIn</span>
                            </a>
                          )}
                        </div>

                        {editModeOption(member)}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
        </div>
      </div>

      {/* Add New Member Modal */}
      {showAddForm && (
        <div className="modal" onClick={() => setShowAddForm(false)}>
          <div className="modal__content" onClick={(e) => e.stopPropagation()}>
            <button
              className="modal__close"
              onClick={() => setShowAddForm(false)}
            >
              ×
            </button>

            <h2 className="modal__title">Add New Participant</h2>

            <div className="modal__form">
              <div className="form-field">
                <label htmlFor="fullName" className="form-field__label">
                  Full Name *
                </label>
                <input
                  id="fullName"
                  name="fullName"
                  type="text"
                  value={newParticipant.fullName}
                  onChange={handleInputChangeParticipant}
                  className="form-field__input"
                  placeholder="Enter full name"
                  required
                />
              </div>

              <div className="form-field">
                <label htmlFor="email" className="form-field__label">
                  Email Address *
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={newParticipant.email}
                  onChange={handleInputChangeParticipant}
                  className="form-field__input"
                  placeholder="Enter email address"
                  required
                />
              </div>

              <div className="form-field">
                <label htmlFor="degree" className="form-field__label">
                  Academic Degree *
                </label>
                <select
                  id="degree"
                  name="degree"
                  value={newParticipant.degree}
                  onChange={handleInputChangeParticipant}
                  className="form-field__select"
                  required
                >
                  <option value="">Select a degree</option>
                  {degreeOptions
                    .filter((d) => d !== "Alumni")
                    .map((degree) => (
                      <option key={degree} value={degree}>
                        {degree}
                      </option>
                    ))}
                </select>
              </div>

              <div className="form-field form-field--checkbox">
                <label className="checkbox">
                  <input
                    type="checkbox"
                    name="isManager"
                    checked={newParticipant.isManager}
                    onChange={handleInputChangeParticipant}
                  />
                  <span>Manager</span>
                </label>
              </div>

              <div className="form-field form-field--checkbox">
                <label className="checkbox">
                  <input
                    type="checkbox"
                    name="isAlumni"
                    checked={newParticipant.isAlumni}
                    onChange={handleInputChangeParticipant}
                  />
                  <span>Alumni</span>
                </label>
              </div>
            </div>

            <div className="modal__actions">
              <button
                className="button button--secondary"
                onClick={() => setShowAddForm(false)}
              >
                Cancel
              </button>
              <button
                className="button button--primary"
                onClick={handleAddParticipant}
              >
                Add Participant
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Notification Popups */}
      {popupMessage && (
        <SuccessPopup
          message={popupMessage}
          onClose={() => setPopupMessage("")}
        />
      )}
      {errorMessage && (
        <ErrorPopup
          message={errorMessage}
          onClose={() => setErrorMessage("")}
        />
      )}
    </div>
  );
};

export default ParticipantsPage;
