import React, { useState } from 'react';
import participants from '../../participants.json'; // Replace with your correct JSON file path
import "./ParticipantsPage.css";

const ParticipantsPage = () => {
  const [selectedDegree, setSelectedDegree] = useState('All'); // Track selected degree filter

  // Define the degree hierarchy
  const degreeOrder = {
    "PhD": 1,
    "MSc": 2,
    "Research Assistant": 3,
    "BSc": 4,
    "Alumni": 5,
  };

  const groupedParticipants = participants.reduce((acc, participant) => {
    const { degree } = participant;
    if (!acc[degree]) acc[degree] = [];
    acc[degree].push(participant);
    return acc;
  }, {});

  // Sort degrees by the defined hierarchy
  const sortedDegrees = Object.keys(groupedParticipants).sort(
    (a, b) => (degreeOrder[a] || 999) - (degreeOrder[b] || 999) // Fallback to 999 for undefined degrees
  );

  const filteredParticipants = selectedDegree === 'All'
    ? groupedParticipants
    : { [selectedDegree]: groupedParticipants[selectedDegree] };

  return (
    <div className="participants-page">
      <h1>Participants</h1>

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
        </select>
      </div>

      {/* Display Participants */}
      {sortedDegrees.map((degree) =>
        filteredParticipants[degree] ? (
          <div key={degree} className="degree-section">
            <h2>{degree}</h2>
            <div className="degree-section-items">
              {filteredParticipants[degree].map((member) => (
                <div key={member.email} className="participant">
                  <div className="personal_photo"></div>
                  <div>
                    <strong>{member.full_name}</strong>
                    <p>{member.bio}</p>
                    <a href={`mailto:${member.email}`} className="email-link">
                      {member.email}
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : null
      )}
    </div>
  );
};

export default ParticipantsPage;
