import React, { useState,useEffect } from 'react';
import participants from '../../participants.json'; // Replace with your correct JSON file path
import "./ParticipantsPage.css";
import {getAllAlumni,getAllLabManagers,getAllLabMembers} from "../../services/websiteService";

const ParticipantsPage = () => {
  const [selectedDegree, setSelectedDegree] = useState('All');
  const [participants, setParticipants] = useState([]); // State for combined participants
  const [loading, setLoading] = useState(true); // Loading state


  const degreeOrder = {
    "PhD": 1,
    "MSc": 2,
    "Research Assistant": 3,
    "BSc": 4,
    "Alumni": 5,
  };


    // Fetch participants data
    useEffect(() => {
      const fetchParticipants = async () => {
        setLoading(true);
  
        try {
          let domain = window.location.hostname; // Extract domain dynamically
          domain = domain.replace(/^https?:\/\//, '');
          domain= domain.replace(":3001",'')
          console.log(domain);
      // Add "www." if missing
          if (!domain.startsWith('www.')) {
            domain = `www.${domain}`;
          }

          // Add ".com" if missing
          if (!domain.endsWith('.com')) {
            domain = `${domain}.com`;
          }
          const [managers, members, alumni] = await Promise.all([
            getAllLabManagers(domain),
            getAllLabMembers(domain),
            getAllAlumni(domain),
          ]);
  
          const safeManagers = Array.isArray(managers) ? managers : [];
          const safeMembers = Array.isArray(members) ? members : [];
          const safeAlumni = Array.isArray(alumni) ? alumni : [];

          // Combine all participants without modifying their structure
          const combinedParticipants = [
            ...safeManagers,
            ...safeMembers,
            ...safeAlumni,
          ];
  
          setParticipants(combinedParticipants);
        } catch (err) {
          console.error('Error fetching participants:', err);
        } finally {
          setLoading(false);
        }
      };
  
      fetchParticipants();
    }, []);

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
    </div>
  );
};

export default ParticipantsPage;
