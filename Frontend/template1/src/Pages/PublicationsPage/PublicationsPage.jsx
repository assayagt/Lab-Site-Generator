import React, { useState, useEffect } from "react";
import "./PublicationsPage.css";
import { getApprovedPublications } from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import AddPublicationForm from "../../Components/AddPublicationForm/AddPubliactionForm";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";
import BibTexPopup from "../../Components/PopUp/BibTexPopup";
import ErrorPopup from "../../Components/PopUp/ErrorPopup";
import { FaInfoCircle } from "react-icons/fa";

import {
  setPublicationGitLink,
  setPublicationPttxLink,
  setPublicationVideoLink,
} from "../../services/websiteService";

const PublicationPage = () => {
  const [publications, setPublications] = useState([]);
  const [yearFilter, setYearFilter] = useState("");
  const [authorFilter, setAuthorFilter] = useState("");
  const [availableYears, setAvailableYears] = useState([]);
  const [availableAuthors, setAvailableAuthors] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;
  const { editMode } = useEditMode();
  const [showAddForm, setShowAddForm] = useState(false);
  const [editedLinks, setEditedLinks] = useState({});
  const [popupMessage, setPopupMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [saveStatus, setSaveStatus] = useState({});
  const [activeTooltip, setActiveTooltip] = useState(null);
  const [showBibTexPopup, setShowBibTexPopup] = useState(false);
  const [currentBibTex, setCurrentBibTex] = useState("");

  // Replace the handleBibTexView function with this:
  const handleBibTexView = (bibtex) => {
    if (bibtex) {
      setCurrentBibTex(bibtex);
      setShowBibTexPopup(true);
    }
  };

  // Add this function to close the popup:
  const handleCloseBibTexPopup = () => {
    setShowBibTexPopup(false);
    setCurrentBibTex("");
  };

  useEffect(() => {
    const fetchPublications = async () => {
      try {
        const domain = sessionStorage.getItem("domain");
        const fetchedPublications = await getApprovedPublications(domain);
        setPublications(fetchedPublications || []);
      } catch (error) {
        console.error("Error fetching publications:", error);
      }
    };

    fetchPublications();
  }, []);

  useEffect(() => {
    const years = Array.from(
      new Set(
        publications.map((pub) => {
          let date = null;
          if (typeof pub.publication_year == "number") {
            date = new Date(pub.publication_year, 0);
          } else {
            date = new Date(pub.publication_year);
          }
          return isNaN(date.getFullYear())
            ? pub.publication_year
            : date.getFullYear();
        })
      )
    ).sort((a, b) => b - a);
    setAvailableYears(years);

    const authors = Array.from(
      new Set(publications.flatMap((pub) => pub.authors || []))
    ).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: "base" }));
    setAvailableAuthors(authors);
  }, [publications]);

  const handleYearChange = (event) => {
    setYearFilter(event.target.value);
    setCurrentPage(1);
  };

  const handleAuthorChange = (event) => {
    setAuthorFilter(event.target.value);
    setCurrentPage(1);
  };

  const filteredPublications = publications
    .filter((pub) => {
      let publicationYear;

      if (typeof pub.publication_year === "number") {
        publicationYear = pub.publication_year;
      } else {
        const date = new Date(pub.publication_year);
        publicationYear = isNaN(date.getTime())
          ? pub.publication_year
          : date.getFullYear();
      }

      const matchesYear = yearFilter
        ? publicationYear === parseInt(yearFilter, 10)
        : true;

      const matchesAuthor = authorFilter
        ? Array.isArray(pub.authors)
          ? pub.authors.some((author) =>
              author.toLowerCase().includes(authorFilter.toLowerCase())
            )
          : pub.authors.toLowerCase().includes(authorFilter.toLowerCase())
        : true;

      return matchesYear && matchesAuthor;
    })
    .sort((a, b) => {
      const getYear = (val) => {
        if (typeof val === "number") return val;
        const date = new Date(val);
        return isNaN(date.getTime()) ? 0 : date.getFullYear();
      };

      const yearA = getYear(a.publication_year);
      const yearB = getYear(b.publication_year);

      return yearB - yearA;
    });

  const paginatedPublications = filteredPublications.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const totalPages = Math.ceil(filteredPublications.length / itemsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleInputChange = (paperId, field, value) => {
    setEditedLinks((prev) => ({
      ...prev,
      [paperId]: {
        ...prev[paperId],
        [field]: value,
      },
    }));
    setSaveStatus((prev) => ({ ...prev, [paperId]: "Save" }));
  };

  const handleSavePublicationLinks = async (paperId) => {
    try {
      const sid = sessionStorage.getItem("sid");
      const domain = sessionStorage.getItem("domain");
      const updatedLinks = editedLinks[paperId];

      if (!updatedLinks) return;

      const gitLink = updatedLinks.git_link ?? "";
      const presentationLink = updatedLinks.presentation_link ?? "";
      const videoLink = updatedLinks.video ?? "";
      let res = null;
      let success = false;
      if (gitLink !== "") {
        res = await setPublicationGitLink(sid, domain, paperId, gitLink);
        success = true;
      }
      if (presentationLink !== "") {
        res = await setPublicationPttxLink(
          sid,
          domain,
          paperId,
          presentationLink
        );
        success = true;
      }
      if (videoLink !== "") {
        res = await setPublicationVideoLink(sid, domain, paperId, videoLink);
        success = true;
      }

      if (res?.response === "true") {
        setPopupMessage("Changes saved successfully!");
        setSaveStatus((prev) => ({ ...prev, [paperId]: "Saved" }));
        setPublications((prev) =>
          prev.map((pub) =>
            pub.paper_id === paperId
              ? {
                  ...pub,
                  git_link: updatedLinks.git_link ?? pub.git_link,
                  presentation_link:
                    updatedLinks.presentation_link ?? pub.presentation_link,
                  video_link: updatedLinks.video ?? pub.video_link,
                }
              : pub
          )
        );
      } else {
        if (!success) {
          if (updatedLinks?.git_link === "") {
            setErrorMessage("Can not save empty filed for GitHub link");
          }
          if (updatedLinks?.presentation_link === "") {
            setErrorMessage("Can not save empty filed for Presentation");
          }
          if (updatedLinks?.video === "") {
            setErrorMessage("Can not save empty filed for Video");
          }
        } else {
          setErrorMessage(res.message);
        }
      }
    } catch (error) {
      console.error("Error updating publication links:", error);
      setErrorMessage("An error occurred while saving.");
    }
  };

  useEffect(() => {
    if (popupMessage || errorMessage) {
      const timer = setTimeout(() => {
        setPopupMessage("");
        setErrorMessage("");
      }, 300000000);
      return () => clearTimeout(timer);
    }
  }, [popupMessage, errorMessage]);

  const handleViewPublication = (pub) => {
    if (pub) {
      window.open(pub, "_blank");
    }
  };
  return (
    <div className="publication-page">
      <div className="publication-header">
        <div className="publication_title">
          Publications
          {editMode && (
            <div className="tooltip-container">
              <button
                className="add-participant-btn"
                onClick={() => setShowAddForm(true)}
              >
                +
              </button>
              <span className="tooltip-text">Add Publication</span>
            </div>
          )}
        </div>
        <div className="filters">
          <label className="specific-filter">
            Filter by Year:
            <select
              className="allOptions"
              value={yearFilter}
              onChange={handleYearChange}
            >
              <option value="">All Years</option>
              {availableYears.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </label>
          <label className="specific-filter">
            Filter by Author:
            <select
              className="allOptions"
              value={authorFilter}
              onChange={handleAuthorChange}
            >
              <option value="">All Authors</option>
              {availableAuthors.map((author) => (
                <option key={author} value={author}>
                  {author}
                </option>
              ))}
            </select>
          </label>
        </div>
      </div>
      <div className="publication-list">
        {paginatedPublications.map((pub) => (
          <div key={pub.paper_id} className="publication-item">
            <div className="pub_item_title">{pub.title}</div>
            <div className="publication-item-info">
              {pub.video_link && (
                <iframe
                  className="video"
                  src={pub.video_link}
                  title={pub.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                ></iframe>
              )}
              <div className="publication_inner_container">
                <p>
                  <strong>Authors:</strong>{" "}
                  {pub.authors.join(", ") || "Unknown Authors"}
                </p>
                <p>
                  <strong>Year:</strong>{" "}
                  {typeof pub.publication_year === "number"
                    ? pub.publication_year
                    : isNaN(new Date(pub.publication_year))
                    ? pub.publication_year
                    : new Date(pub.publication_year).getFullYear()}
                </p>
                <p className="description">{pub.description}</p>
                <div className="links">
                  {pub.publication_link && (
                    <button
                      onClick={() =>
                        handleViewPublication(pub.publication_link)
                      }
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
                    <button
                      onClick={() => handleViewPublication(pub.git_link)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="publication-link-button "
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
                    </button>
                  )}
                  {pub.presentation_link && (
                    <button
                      onClick={() =>
                        handleViewPublication(pub.publication_link)
                      }
                      className="publication-link-button "
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
                    </button>
                  )}
                  {pub.bibtex && (
                    <button
                      onClick={() => handleBibTexView(pub.bibtex)}
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
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                        <polyline points="14 2 14 8 20 8"></polyline>
                        <line x1="16" y1="13" x2="8" y2="13"></line>
                        <line x1="16" y1="17" x2="8" y2="17"></line>
                        <polyline points="10 9 9 9 8 9"></polyline>
                      </svg>
                      BibTeX
                    </button>
                  )}
                  {pub.pub_url && (
                    <button
                      onClick={() => handleViewPublication(pub.pub_url)}
                      className="publication-link-button"
                      title="Visit Publisher Site"
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
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                        <polyline points="15 3 21 3 21 9" />
                        <line x1="10" y1="14" x2="21" y2="3" />
                      </svg>
                      Publisher Site
                    </button>
                  )}
                </div>
              </div>
            </div>
            {/* </a> */}
            {editMode && (
              <form className="publication-form">
                <div className="input-container">
                  <div className="input-with-info">
                    <input
                      type="url"
                      className="submit-pub_pg"
                      placeholder="Enter GitHub link"
                      defaultValue={pub.git_link || ""}
                      onChange={(e) =>
                        handleInputChange(
                          pub.paper_id,
                          "git_link",
                          e.target.value
                        )
                      }
                    />
                    <div
                      className={`info-icon-container ${
                        activeTooltip === `${pub.paper_id}-github`
                          ? "active"
                          : ""
                      }`}
                      onClick={() =>
                        setActiveTooltip(
                          activeTooltip === `${pub.paper_id}-github`
                            ? null
                            : `${pub.paper_id}-github`
                        )
                      }
                    >
                      <FaInfoCircle className="input-info-icon" />
                      <div className="info-tooltip">
                        Format: https://github.com/username/repository
                      </div>
                    </div>
                  </div>
                  <label className="hidden-label_pg">GitHub</label>
                </div>

                <div className="input-container">
                  <div className="input-with-info">
                    <input
                      type="url"
                      className="submit-pub_pg"
                      placeholder="Enter Presentation link"
                      defaultValue={pub.presentation_link || ""}
                      onChange={(e) =>
                        handleInputChange(
                          pub.paper_id,
                          "presentation_link",
                          e.target.value
                        )
                      }
                    />
                    <div
                      className={`info-icon-container ${
                        activeTooltip === `${pub.paper_id}-presentation`
                          ? "active"
                          : ""
                      }`}
                      onClick={() =>
                        setActiveTooltip(
                          activeTooltip === `${pub.paper_id}-presentation`
                            ? null
                            : `${pub.paper_id}-presentation`
                        )
                      }
                    >
                      <FaInfoCircle className="input-info-icon" />
                      <div className="info-tooltip">
                        Format: https://docs.google.com/presentation/d/...
                      </div>
                    </div>
                  </div>
                  <label className="hidden-label_pg">Presentation</label>
                </div>

                <div className="input-container">
                  <div className="input-with-info">
                    <input
                      type="url"
                      className="submit-pub_pg"
                      placeholder="Enter Video link"
                      defaultValue={pub.video_link || ""}
                      onChange={(e) =>
                        handleInputChange(pub.paper_id, "video", e.target.value)
                      }
                    />
                    <div
                      className={`info-icon-container ${
                        activeTooltip === `${pub.paper_id}-video`
                          ? "active"
                          : ""
                      }`}
                      onClick={() =>
                        setActiveTooltip(
                          activeTooltip === `${pub.paper_id}-video`
                            ? null
                            : `${pub.paper_id}-video`
                        )
                      }
                    >
                      <FaInfoCircle className="input-info-icon" />
                      <div className="info-tooltip">
                        Format: https://youtube.com/watch?v=... or embed link
                      </div>
                    </div>
                  </div>
                  <label className="hidden-label_pg">Video</label>
                </div>

                <button
                  type="button"
                  className="save-btn"
                  onClick={() => handleSavePublicationLinks(pub.paper_id)}
                >
                  {saveStatus[pub.paper_id] || "Save"}
                </button>
              </form>
            )}
          </div>
        ))}
        {showBibTexPopup && (
          <BibTexPopup
            bibtex={currentBibTex}
            onClose={handleCloseBibTexPopup}
          />
        )}
      </div>
      <div className="pagination_t1">
        <button
          className="pagination-buttons"
          onClick={handlePrevPage}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          className="pagination-buttons"
          onClick={handleNextPage}
          disabled={currentPage === totalPages}
        >
          Next
        </button>
      </div>

      {showAddForm && (
        <div className="custom-modal-overlay">
          <div className="modal__content">
            <button
              className="close-button"
              onClick={() => setShowAddForm(false)}
            >
              X
            </button>
            <h2 className="modal__title">Add New Publication</h2>
            <AddPublicationForm
              onSuccess={() => {
                setShowAddForm(false);
                window.location.reload();
              }}
            />
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

export default PublicationPage;
