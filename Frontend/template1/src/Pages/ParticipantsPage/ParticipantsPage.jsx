import React, { useState, useEffect } from "react";
import "./ParticipantsPage.css";
import {
  getAllAlumni,
  getAllLabManagers,
  getAllLabMembers,
  addLabMemberFromWebsite,
  createNewSiteManagerFromLabWebsite,
  addAlumniFromLabWebsite,
} from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";

const ParticipantsPage = () => {
  const [selectedDegree, setSelectedDegree] = useState("All");
  const [participants, setParticipants] = useState([]);
  const [alumni, setAlumni] = useState([]);
  const [loading, setLoading] = useState(true);
  const { editMode } = useEditMode();
  const [showAddForm, setShowAddForm] = useState(false);
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
    Postdoc: 3,
    "B.Sc.": 4,
  };

  const degreeOptions = ["Ph.D.", "M.Sc.", "B.Sc.", "Postdoc"];

  const formatDomain = () => {
    let domain = window.location.hostname
      .replace(/^https?:\/\//, "")
      .replace(":3001", "");
    if (!domain.startsWith("www.")) domain = `www.${domain}`;
    if (!domain.endsWith(".com")) domain = `${domain}.com`;
    return domain;
  };

  const fetchParticipants = async () => {
    setLoading(true);
    try {
      const domain = formatDomain();

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
      editMode && (
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
    const domain = formatDomain();

    try {
      if (!member.isManager) {
        // Promote to manager
        const response = await createNewSiteManagerFromLabWebsite(
          userId,
          member.email,
          domain
        );
        if (response?.response === "true") {
          fetchParticipants();
        } else {
          console.error("Failed to promote to manager:", response?.message);
        }
      } else {
        // Demote from manager
      }
    } catch (err) {
      console.error("Error toggling manager:", err);
    }
  };

  const handleToggleAlumni = async (member) => {
    const userId = sessionStorage.getItem("sid");
    const domain = formatDomain();

    try {
      if (!member.isAlumni) {
        // Promote to alumni
        const response = await addAlumniFromLabWebsite(
          userId,
          member.email,
          domain
        );
        if (response?.response === "true") {
          fetchParticipants();
        } else {
          console.error("Failed to promote to alumni:", response?.message);
        }
      } else {
      }
    } catch (err) {
      console.error("Error toggling alumni:", err);
    }
  };
  const sortedDegrees = Object.keys(groupedParticipants).sort(
    (a, b) => (degreeOrder[a] || 999) - (degreeOrder[b] || 999)
  );

  const filteredParticipants =
    selectedDegree === "All"
      ? groupedParticipants
      : { [selectedDegree]: groupedParticipants[selectedDegree] };

  const handleInputChangeParticipant = (e) => {
    const { name, value, type, checked } = e.target;
    setNewParticipant((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleAddParticipant = async () => {
    const { fullName, email, degree, isManager, isAlumni } = newParticipant;
    const userId = sessionStorage.getItem("sid");
    const domain = formatDomain();

    if (!fullName || !email || !degree) {
      console.error("Please fill in all fields.");
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
        console.error("Failed to add lab member:", addMemberResponse?.message);
        return;
      }

      if (isManager) {
        const managerResponse = await createNewSiteManagerFromLabWebsite(
          userId,
          email,
          domain
        );
        if (managerResponse?.response !== "true") {
          console.error("Failed to add manager:", managerResponse?.message);
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
          console.error("Failed to mark as alumni:", alumniResponse?.message);
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
      console.error("Error adding participant:", error);
    }
  };

  if (loading) return <div>Loading...</div>;

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
          {sortedDegrees.map((degree) => (
            <option key={degree} value={degree}>
              {degree}
            </option>
          ))}
          <option value="Alumni">Alumni</option>
        </select>
      </div>

      {sortedDegrees.map(
        (degree) =>
          filteredParticipants[degree] && (
            <div key={degree} className="degree-section">
              <div className="degree">{degree}</div>
              <div className="degree-section-items">
                {filteredParticipants[degree].map((member) => (
                  <div key={member.email} className="participant">
                    <div className="personal_photo"></div>
                    <div className="personal_info_member">
                      <div className="fullname">{member.fullName}</div>
                      <div>{member.bio}</div>
                      <a href={`mailto:${member.email}`} className="email-link">
                        {member.email}
                      </a>
                      {editModeOption(member)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )
      )}

      {alumni.length > 0 && (
        <div className="degree-section">
          <div className="degree">Alumni</div>
          <div className="degree-section-items">
            {alumni.map((member) => (
              <div key={member.email} className="participant">
                <div className="personal_photo"></div>
                <div>
                  <strong>{member.fullName}</strong>
                  <span className="alumni-degree"> [{member.degree}]</span>
                  <p>{member.bio}</p>
                  <a href={`mailto:${member.email}`} className="email-link">
                    {member.email}
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {showAddForm && (
        <div className="modal-overlay" onClick={() => setShowAddForm(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h3>Add New Participant</h3>

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
                className="modal-button add_button"
                onClick={handleAddParticipant}
              >
                Add
              </button>
              <button
                className="modal-button cancel-button"
                onClick={() => setShowAddForm(false)}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ParticipantsPage;
