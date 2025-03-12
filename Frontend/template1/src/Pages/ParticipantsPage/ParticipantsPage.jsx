import React, { useState, useEffect } from "react";
import "./ParticipantsPage.css";
import {
  getAllAlumni,
  getAllLabManagers,
  getAllLabMembers,
} from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";

const ParticipantsPage = () => {
  const [selectedDegree, setSelectedDegree] = useState("All");
  const [participants, setParticipants] = useState([]); // State for participants (excluding alumni)
  const [alumni, setAlumni] = useState([]); // Separate state for alumni
  const [loading, setLoading] = useState(true);
  const { editMode } = useEditMode(); // Get edit mode state
  const [showAddForm, setShowAddForm] = useState(false);
  const [newParticipant, setNewParticipant] = useState({
    fullName: "",
    email: "",
    degree: "",
  });
  const degreeOrder = {
    PhD: 1,
    MSc: 2,
    "Research Assistant": 3,
    BSc: 4,
  };

  const degreeOptions = ["Ph.D.", "M.Sc.", "B.Sc.", "Postdoc"];

  useEffect(() => {
    const fetchParticipants = async () => {
      setLoading(true);
      try {
        let domain = window.location.hostname
          .replace(/^https?:\/\//, "")
          .replace(":3001", "");

        // Add "www." if missing
        if (!domain.startsWith("www.")) domain = `www.${domain}`;
        // Add ".com" if missing
        if (!domain.endsWith(".com")) domain = `${domain}.com`;

        const [managers, members, alumniData] = await Promise.all([
          getAllLabManagers(domain),
          getAllLabMembers(domain),
          getAllAlumni(domain),
        ]);

        setParticipants([...managers, ...members]); // Store only non-alumni
        setAlumni(alumniData || []); // Store alumni separately
      } catch (err) {
        console.error("Error fetching participants:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchParticipants();
  }, []);

  // Grouping participants by degree
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
            <input type="checkbox" defaultChecked={member.isManager} />
            Manager
          </label>
          <label>
            <input type="checkbox" defaultChecked={member.isAlumni} />
            Alumni
          </label>
        </div>
      )
    );
  };

  // Sort degrees by defined hierarchy
  const sortedDegrees = Object.keys(groupedParticipants).sort(
    (a, b) => (degreeOrder[a] || 999) - (degreeOrder[b] || 999)
  );

  // Filtering participants
  const filteredParticipants =
    selectedDegree === "All"
      ? groupedParticipants
      : { [selectedDegree]: groupedParticipants[selectedDegree] };

  if (loading) {
    return <div>Loading...</div>;
  }

  // Handle input changes for the form
  const handleInputChangeParticipant = (e) => {
    const { name, value } = e.target;
    setNewParticipant((prev) => ({ ...prev, [name]: value }));
  };

  // Function to handle adding a new participant (Temporary, replace with API call)
  const handleAddParticipant = () => {
    // if (newParticipant.fullName && newParticipant.email && newParticipant.degree) {
    //   setParticipants([...participants, newParticipant]); // Add to the participants list
    //   setNewParticipant({ fullName: "", email: "", degree: "" }); // Reset form
    //   setShowAddForm(false); // Close modal
    // } else {
    //   alert("Please fill in all fields!");
    // }if (newParticipant.fullName && newParticipant.email && newParticipant.degree) {
    //   setParticipants([...participants, newParticipant]); // Add to the participants list
    //   setNewParticipant({ fullName: "", email: "", degree: "" }); // Reset form
    //   setShowAddForm(false); // Close modal
    // } else {
    //   alert("Please fill in all fields!");
    // }
  };

  return (
    <div className="participants-page">
      <div className="participant_title">
        Lab Members
        {editMode && (
          <div className="tooltip-container">
            <button
              className="add-participant-btn"
              onClick={() => setShowAddForm(true)}
              s
            >
              +
            </button>
            <span className="tooltip-text">Add Member</span>
          </div>
        )}
      </div>

      {/* Degree Filter Dropdown */}
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
          "<option value="Alumni">Alumni</option>
        </select>
      </div>

      {/* Display Participants by Degree */}
      {sortedDegrees.map((degree) =>
        filteredParticipants[degree] ? (
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
        ) : null
      )}

      {/* Alumni Section (Separate) */}
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
                type="text"
                placeholder="Full Name"
                name="fullName"
                value={newParticipant.fullName}
                onChange={handleInputChangeParticipant}
                className="modal-content-item"
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email:</label>
              <input
                id="email"
                type="text"
                placeholder="Email"
                name="email"
                value={newParticipant.email}
                onChange={handleInputChangeParticipant}
                className="modal-content-item"
              />
            </div>

            <div className="form-group">
              <label htmlFor="degree">Degree:</label>
              <select
                id="degree"
                className="modal-content-item"
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
