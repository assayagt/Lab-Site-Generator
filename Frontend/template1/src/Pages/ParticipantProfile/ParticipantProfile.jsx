import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./ParticipantProfile.css";
import defaultProfileIcon from "../../images/account_avatar.svg";
import {
  getAllLabMembers,
  getAllLabManagers,
  getAllAlumni,
  getApprovedPublications,
} from "../../services/websiteService";
const ParticipantProfile = () => {
  const { email } = useParams(); // Get participant email from URL
  const navigate = useNavigate();
  const [participant, setParticipant] = useState(null);
  const [publications, setPublications] = useState([]);
  const [filteredPublications, setFilteredPublications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [publicationsLoading, setPublicationsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedYear, setSelectedYear] = useState("all");
  const [availableYears, setAvailableYears] = useState([]);
  const [participantType, setParticipantType] = useState(""); // "member", "manager", "alumni"

  useEffect(() => {
    fetchParticipantData();
  }, [email]);

  useEffect(() => {
    filterPublicationsByYear();
    extractAvailableYears();
  }, [publications, selectedYear]);

  const fetchParticipantData = async () => {
    try {
      setLoading(true);
      const domain = sessionStorage.getItem("domain");
      const decodedEmail = decodeURIComponent(email);

      // Try to find the participant in different lists
      let participantData = null;
      let type = "";

      // Check lab members
      const members = await getAllLabMembers(domain);
      if (members && members.length > 0) {
        participantData = members.find(
          (member) => member.email === decodedEmail
        );
        if (participantData) type = "member";
      }

      // If not found in members, check managers
      if (!participantData) {
        const managers = await getAllLabManagers(domain);
        if (managers && managers.length > 0) {
          participantData = managers.find(
            (manager) => manager.email === decodedEmail
          );
          if (participantData) type = "manager";
        }
      }

      // If not found in managers, check alumni
      if (!participantData) {
        const alumni = await getAllAlumni(domain);
        if (alumni && alumni.length > 0) {
          participantData = alumni.find((alum) => alum.email === decodedEmail);
          if (participantData) type = "alumni";
        }
      }

      setParticipant(participantData);
      setParticipantType(type);
      setLoading(false);

      // Fetch publications separately
      if (participantData) {
        setPublicationsLoading(true);
        try {
          // Fetch all approved publications
          const allPublications = await getApprovedPublications(domain);

          if (allPublications && allPublications.length > 0) {
            // Filter publications where participant is an author
            const participantPublications = allPublications.filter((pub) => {
              // Multiple ways to match the participant in authors
              if (participantData && pub.authors) {
                const authorsLower = pub.authors;
                const fullNameLower = participantData.fullName;
                const emailLower = participantData.email;

                // Check if full name appears in authors
                if (fullNameLower && authorsLower.includes(fullNameLower)) {
                  return true;
                }

                // Check if email appears in authors (some publications might list emails)
                if (emailLower && authorsLower.includes(emailLower)) {
                  return true;
                }

                // Check if last name appears (for cases where first names might vary)
                const lastName = participantData.fullName
                  ?.split(" ")
                  .pop()
                  ?.toLowerCase();
                if (lastName && authorsLower.includes(lastName)) {
                  // Additional check to avoid false positives with common last names
                  const nameParts = participantData.fullName?.split(" ");
                  if (nameParts?.length > 1) {
                    const firstName = nameParts[0].toLowerCase();
                    // Check if at least first initial or first name is present
                    if (
                      authorsLower.includes(firstName) ||
                      authorsLower.includes(firstName[0])
                    ) {
                      return true;
                    }
                  }
                }
              }
              return false;
            });

            // Sort publications by year (newest first)
            participantPublications.sort(
              (a, b) => b.publication_year - a.publication_year
            );
            setPublications(participantPublications);
          }
        } catch (pubError) {
          console.error("Error fetching publications:", pubError);
        } finally {
          setPublicationsLoading(false);
        }
      }
    } catch (error) {
      console.error("Error fetching participant data:", error);
      setError("Failed to load participant data");
    } finally {
      if (!participant) {
        setLoading(false);
      }
    }
  };

  const extractAvailableYears = () => {
    const yearsSet = new Set();

    publications.forEach((pub) => {
      if (typeof pub.publication_year === "number") {
        yearsSet.add(pub.publication_year);
      } else {
        const date = new Date(pub.publication_year);
        if (!isNaN(date.getTime())) {
          yearsSet.add(date.getFullYear());
        }
      }
    });

    const years = Array.from(yearsSet);
    years.sort((a, b) => b - a); // Sort years in descending order
    setAvailableYears(years);
  };
  const filterPublicationsByYear = () => {
    if (selectedYear === "all") {
      setFilteredPublications(publications);
    } else {
      const selectedYearInt = parseInt(selectedYear, 10);

      const filtered = publications.filter((pub) => {
        let year;

        if (typeof pub.publication_year === "number") {
          year = pub.publication_year;
        } else {
          const date = new Date(pub.publication_year);
          year = isNaN(date.getTime()) ? null : date.getFullYear();
        }

        return year === selectedYearInt;
      });

      setFilteredPublications(filtered);
    }
  };

  const handleViewPublication = (pub) => {
    if (pub.publication_link) {
      window.open(pub.publication_link, "_blank");
    }
  };

  const getParticipantBadge = () => {
    switch (participantType) {
      case "manager":
        return <span className="participant-badge manager">Lab Manager</span>;
      case "alumni":
        return <span className="participant-badge alumni">Alumni</span>;
      case "member":
      default:
        return <span className="participant-badge member">Lab Member</span>;
    }
  };

  if (loading) {
    return (
      <div className="participant-profile">
        <div className="loading">Loading participant information...</div>
      </div>
    );
  }

  if (error || !participant) {
    return (
      <div className="participant-profile">
        <div className="error">
          {error || "Participant not found"}
          <button onClick={() => navigate(-1)} className="back-button">
            Go Back
          </button>
        </div>
      </div>
    );
  }

  const formatAuthors = (authors) => {
    if (!authors) return "";

    // If authors is already an array, join with commas
    if (Array.isArray(authors)) {
      return authors.filter((author) => author).join(", ");
    }

    // Convert to string if it's not already
    const authorsString = String(authors);

    // Split authors by common delimiters (semicolon, "and", newline, etc.)
    const authorList = authorsString
      .split(/;|\sand\s|\n/)
      .map((author) => author.trim())
      .filter((author) => author.length > 0);

    // Join with commas and proper spacing
    return authorList.join(", ");
  };

  return (
    <div className="participant-profile">
      <div className="profile-content">
        <div className="profile-info-section">
          <div className="profile-photo-container">
            <img
              src={participant.photo || defaultProfileIcon}
              alt={participant.fullName}
              className="profile-photo"
            />
          </div>

          <div className="profile-details">
            <div className="profile-header-info">
              <h1 className="profile-name">{participant.fullName}</h1>
              {getParticipantBadge()}
            </div>
            <p className="profile-degree">{participant.degree}</p>
            <p className="profile-email">{participant.email}</p>

            {participant.bio && (
              <div className="profile-bio">
                <h3>Bio</h3>
                <p className="profile_bio_content">{participant.bio}</p>
              </div>
            )}

            <div className="profile-links">
              {participant.linkedin_link && (
                <a
                  href={participant.linkedin_link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="profile-link linkedin"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" />
                  </svg>
                  LinkedIn Profile
                </a>
              )}

              {participant.secondEmail && (
                <div className="secondary-email">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                    <path d="m22 7-10 5L2 7"></path>
                  </svg>
                  {participant.secondEmail}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="publications-section2">
          <div className="publications-header">
            <h2>Publications ({filteredPublications.length})</h2>
            <div className="filter-controls">
              <label htmlFor="year-filter">Filter by Year:</label>
              <select
                id="year-filter"
                value={selectedYear}
                onChange={(e) => setSelectedYear(e.target.value)}
                className="year-filter"
              >
                <option value="all">All Years</option>
                {availableYears.map((year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {publicationsLoading ? (
            <div className="loading-publications">
              <div className="spinner"></div>
              <p>Loading publications...</p>
            </div>
          ) : filteredPublications.length === 0 ? (
            <div className="no-publications">
              {publications.length === 0
                ? "No publications found for this participant"
                : `No publications found for ${selectedYear}`}
            </div>
          ) : (
            <div className="publications-list">
              {filteredPublications.map((pub, index) => (
                <div key={pub.id || index} className="publication-card_user">
                  <div className="publication-header">
                    <h3 className="publication-title">{pub.title}</h3>
                    <span className="publication-year">
                      {typeof pub.publication_year === "number"
                        ? pub.publication_year
                        : (() => {
                            const date = new Date(pub.publication_year);
                            return isNaN(date.getTime())
                              ? pub.publication_year
                              : date.getFullYear();
                          })()}
                    </span>
                  </div>

                  <p className="publication-authors">
                    {formatAuthors(pub.authors)}
                  </p>

                  {pub.journal_name && (
                    <p className="publication-journal">{pub.journal_name}</p>
                  )}
                  {pub.description && (
                    <p className="publication-journal">{pub.description}</p>
                  )}

                  <div className="publication-links">
                    {pub.publication_link && (
                      <button
                        onClick={() => handleViewPublication(pub)}
                        className="publication-link-button primary"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                          <polyline points="15 3 21 3 21 9"></polyline>
                          <line x1="10" y1="14" x2="21" y2="3"></line>
                        </svg>
                        View Publication
                      </button>
                    )}

                    {pub.git_link && (
                      <a
                        href={pub.git_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="publication-link-button"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          viewBox="0 0 24 24"
                          fill="currentColor"
                        >
                          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
                        </svg>
                        GitHub
                      </a>
                    )}

                    {pub.presentation_link && (
                      <a
                        href={pub.presentation_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="publication-link-button"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <rect
                            x="2"
                            y="3"
                            width="20"
                            height="14"
                            rx="2"
                            ry="2"
                          ></rect>
                          <line x1="8" y1="21" x2="16" y2="21"></line>
                          <line x1="12" y1="17" x2="12" y2="21"></line>
                        </svg>
                        Presentation
                      </a>
                    )}

                    {pub.video && (
                      <a
                        href={pub.video}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="publication-link-button"
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="16"
                          height="16"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        >
                          <polygon points="23 7 16 12 23 17 23 7"></polygon>
                          <rect
                            x="1"
                            y="5"
                            width="15"
                            height="14"
                            rx="2"
                            ry="2"
                          ></rect>
                        </svg>
                        Video
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ParticipantProfile;
