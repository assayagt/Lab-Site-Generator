import React, { useState, useEffect } from "react";
import "./ParticipantsPage.css";
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
        <div className="edit-options">
          <label>
            <input
              type="checkbox"
              checked={member.isManager}
              onChange={() => handleToggleManager(member)}
            />
            Manager
          </label>
          <label>
            <input
              type="checkbox"
              checked={member.isAlumni}
              onChange={() => handleToggleAlumni(member)}
            />
            Alumni
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
    return <div>Loading participants...</div>;
  }

  return (
    <div className="participants-page">
      <div className="participant_title">
        Lab Members
        {editMode && (
          <div className="tooltip-container">
            <button
              className="add-participant-btn"
              onClick={() => setShowAddForm(true)}
            >
              +
            </button>
            <span className="tooltip-text">Add Member</span>
          </div>
        )}
      </div>

      <div className="filter-container">
        <label htmlFor="degree-filter">Filter by Degree:</label>
        <select
          id="degree-filter"
          value={selectedDegree}
          onChange={(e) => setSelectedDegree(e.target.value)}
        >
          <option value="All">All Degrees</option>
          {degreeOptions.map((degree) => (
            <option key={degree} value={degree}>
              {degree}
            </option>
          ))}
        </select>
      </div>

      {Object.entries(filteredParticipants).map(([degree, members]) => (
        <div key={degree} className="degree-section">
          <div className="degree">{degree}</div>
          {members.length === 0 ? (
            <div className="no-participants-msg">
              No participants found for this category.
            </div>
          ) : (
            <div className="degree-section-items">
              {members.map((member) => (
                <div key={member.email} className="participant">
                  <img
                    src={
                      member.profile_picture
                        ? member.profile_picture
                        : accountIcon
                    }
                    alt="User"
                    className="personal_photo"
                  />
                  <div className="personal_info_member">
                    <div className="name-with-icon">
                      <span className="fullname">{member.fullName}</span>
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
                    <div className="personal_bio">{member.bio}</div>
                    <div className="contact-links">
                      <a
                        href={`mailto:${member.email}`}
                        className="email-link"
                        title="Email"
                      >
                        <FaEnvelope /> {member.email}
                      </a>

                      {member.linkedin_link && (
                        <a
                          href={member.linkedin_link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="linkedin-link"
                          title="LinkedIn"
                        >
                          <FaLinkedin /> LinkedIn
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

      {alumni.length > 0 && (
        <div className="degree-section">
          <div className="degree">Alumni</div>
          <div className="degree-section-items">
            {alumni.map((member) => (
              <div key={member.email} className="participant">
                <img
                  src={member.profile_picture}
                  alt="User"
                  className="personal_photo"
                />
                <div className="personal_info_member">
                  <div className="name-with-icon">
                    <span className="fullname">{member.fullName}</span>
                    <span className="alumni-degree"> [{member.degree}]</span>
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
                  <p>{member.bio}</p>
                  <a href={`mailto:${member.email}`} className="email-link">
                    {member.email}
                  </a>
                  {editModeOption(member)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {showAddForm && (
        <div className="modal-overlay" onClick={() => setShowAddForm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3 className="title_add_user">Add New Participant</h3>

            <div className="form-group">
              <label htmlFor="fullName">Full Name:</label>
              <input
                id="fullName"
                name="fullName"
                value={newParticipant.fullName}
                onChange={handleInputChangeParticipant}
                className="modal-content-item"
                placeholder="Full Name"
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                id="email"
                name="email"
                value={newParticipant.email}
                onChange={handleInputChangeParticipant}
                className="modal-content-item"
                placeholder="Email"
              />
            </div>

            <div className="form-group">
              <label htmlFor="degree">Degree:</label>
              <select
                id="degree"
                name="degree"
                value={newParticipant.degree}
                onChange={handleInputChangeParticipant}
                className="modal-content-item"
              >
                <option value="">Select Degree</option>
                {degreeOptions.map((degree) => (
                  <option key={degree} value={degree}>
                    {degree}
                  </option>
                ))}
              </select>
            </div>

            <div className="modal-buttons">
              <button
                className="modal-button cancel-button"
                onClick={() => setShowAddForm(false)}
              >
                Cancel
              </button>
              <button
                className="modal-button add_button"
                onClick={handleAddParticipant}
              >
                Add
              </button>
            </div>
          </div>
        </div>
      )}
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
