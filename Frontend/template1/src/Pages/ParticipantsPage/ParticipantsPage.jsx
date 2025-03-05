import React, { useState, useEffect } from 'react';
import "./ParticipantsPage.css";
import { getAllAlumni, getAllLabManagers, getAllLabMembers } from "../../services/websiteService";

const ParticipantsPage = () => {
  const [selectedDegree, setSelectedDegree] = useState('All');
  const [participants, setParticipants] = useState([]); // State for participants (excluding alumni)
  const [alumni, setAlumni] = useState([]); // Separate state for alumni
  const [loading, setLoading] = useState(true);

  const degreeOrder = {
    "PhD": 1,
    "MSc": 2,
    "Research Assistant": 3,
    "BSc": 4
    
  };

  useEffect(() => {
    const fetchParticipants = async () => {
      setLoading(true);
      try {
        let domain = window.location.hostname.replace(/^https?:\/\//, '').replace(":3001", '');

        // Add "www." if missing
        if (!domain.startsWith('www.')) domain = `www.${domain}`;
        // Add ".com" if missing
        if (!domain.endsWith('.com')) domain = `${domain}.com`;

        const [managers, members, alumniData] = await Promise.all([
          getAllLabManagers(domain),
          getAllLabMembers(domain),
          getAllAlumni(domain),
        ]);

        setParticipants([...managers, ...members]); // Store only non-alumni
        setAlumni(alumniData || []); // Store alumni separately
      } catch (err) {
        console.error('Error fetching participants:', err);
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

  // Sort degrees by defined hierarchy
  const sortedDegrees = Object.keys(groupedParticipants).sort(
    (a, b) => (degreeOrder[a] || 999) - (degreeOrder[b] || 999)
  );

  // Filtering participants
  const filteredParticipants = selectedDegree === 'All'
    ? groupedParticipants
    : { [selectedDegree]: groupedParticipants[selectedDegree] };

  if (loading) {
    return <div>Loading...</div>;
  }

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
          ))}"
          <option  value="Alumni">
              Alumni
            </option>
        </select>
      </div>

      {/* Display Participants by Degree */}
      {sortedDegrees.map((degree) =>
        filteredParticipants[degree] ? (
          <div key={degree} className="degree-section">
            <h2>{degree}</h2>
            <div className="degree-section-items">
              {filteredParticipants[degree].map((member) => (
                <div key={member.email} className="participant">
                  <div className="personal_photo"></div>
                  <div>
                    <strong>{member.fullName}</strong>
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

      {/* Alumni Section (Separate) */}
      {alumni.length > 0 && (
        <div className="degree-section">
          <h2>Alumni</h2>
          <div className="degree-section-items">
            {alumni.map((member) => (
              <div key={member.email} className="participant">
                <div className="personal_photo"></div>
                <div>
                  <strong>{member.fullName}</strong>
                  <span className="alumni-degree">  [{member.degree}]</span>
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
    </div>
  );
};

export default ParticipantsPage;
