import React, { useState, useEffect } from "react";
import "./PublicationsPage2.css";
import { getApprovedPublications } from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import AddPublicationForm from "../../Components/AddPublicationForm/AddPubliactionForm";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";
import ErrorPopup from "../../Components/PopUp/ErrorPopup";
import { FaInfoCircle } from "react-icons/fa";
import BibTexPopup from "../../Components/PopUp/BibTexPopup";

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
  const [expandedDescriptions, setExpandedDescriptions] = useState({});
  const [showBibTexPopup, setShowBibTexPopup] = useState(false);
  const [currentBibTex, setCurrentBibTex] = useState("");

  // Replace the handleBibTexView function with this:
  const handleBibTexView = (bibtex) => {
    if (bibtex) {
      setCurrentBibTex(bibtex);
      setShowBibTexPopup(true);
    }
  };

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

  const toggleDescription = (publicationId) => {
    setExpandedDescriptions((prev) => ({
      ...prev,
      [publicationId]: !prev[publicationId],
    }));
  };

  const truncateText = (text, maxLength = 300) => {
    if (!text) return "";
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + "...";
  };

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
            setErrorMessage("Can not save empty field for GitHub link");
          }
          if (updatedLinks?.presentation_link === "") {
            setErrorMessage("Can not save empty field for Presentation");
          }
          if (updatedLinks?.video === "") {
            setErrorMessage("Can not save empty field for Video");
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

  const handleViewPublication = (pub) => {
    if (pub) {
      window.open(pub, "_blank");
    }
  };

  return (
    <div className="publications-page_2">
      <div className="publications-page__container_2">
        <div className="publications-page__header_2">
          <h1 className="publications-page__title_2">Publications</h1>

          <div className="publications-page__controls_2">
            <div className="publications-page__filters_2">
              <div className="filter-group_2">
                <label htmlFor="year-filter_2">Filter by Year:</label>
                <select
                  id="year-filter_2"
                  className="publications-page__select_2"
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
              </div>

              <div className="filter-group_2">
                <label htmlFor="author-filter_2">Filter by Author:</label>
                <select
                  id="author-filter_2"
                  className="publications-page__select_2"
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
              </div>
            </div>

            {editMode && (
              <button
                className="publications-page__add-button_2"
                onClick={() => setShowAddForm(true)}
                aria-label="Add publication"
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
                <span>Add Publication</span>
              </button>
            )}
          </div>
        </div>

        <div className="publications-page__content_2">
          {paginatedPublications.length === 0 ? (
            <div className="publications-page__empty">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
              <h3>No Publications Found</h3>
              <p>No publications match your current filters.</p>
            </div>
          ) : (
            <div className="publications-list_2">
              {paginatedPublications.map((pub) => (
                <div key={pub.paper_id} className="publication-card_2">
                  <div className="publication-header_2">
                    <h2 className="publication-title_2">{pub.title}</h2>
                    <span className="publication-year_2">
                      {typeof pub.publication_year === "number"
                        ? pub.publication_year
                        : isNaN(new Date(pub.publication_year))
                        ? pub.publication_year
                        : new Date(pub.publication_year).getFullYear()}
                    </span>
                  </div>

                  <div className="publication-authors_2">
                    <strong>Authors:</strong>{" "}
                    {pub.authors?.join(", ") || "Unknown Authors"}
                  </div>

                  <div className="publication-content_2">
                    {pub.video_link && (
                      <div className="publication-video_2">
                        <iframe
                          src={pub.video_link}
                          title={pub.title}
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                          allowFullScreen
                        ></iframe>
                      </div>
                    )}

                    {pub.description && (
                      <div className="publication-description_2">
                        <p>
                          {expandedDescriptions[pub.paper_id]
                            ? pub.description
                            : truncateText(pub.description, 700)}
                          {pub.description.length > 700 && (
                            <button
                              className="read-more-btn"
                              onClick={() => toggleDescription(pub.paper_id)}
                            >
                              {expandedDescriptions[pub.paper_id]
                                ? " Read less"
                                : " Read more"}
                            </button>
                          )}
                        </p>
                      </div>
                    )}
                  </div>

                  <div className="publication-actions_2">
                    {pub.publication_link && (
                      <button
                        onClick={() =>
                          handleViewPublication(pub.publication_link)
                        }
                        className="publication-button_2 publication-button--primary_2"
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
                        className="publication-button_2"
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
                          handleViewPublication(pub.presentation_link)
                        }
                        className="publication-button_2"
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

                  {editMode && (
                    <div className="publication-edit-form_2">
                      <h4 className="edit-form-title_2">Edit Links</h4>

                      <div className="edit-form-row_2">
                        <div className="input-group_2">
                          <input
                            type="url"
                            className="edit-input_2"
                            placeholder="GitHub link_2"
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
                            className={`info-icon_2 ${
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
                            <FaInfoCircle />
                            <div className="info-tooltip_2">
                              Format: https://github.com/username/repository
                            </div>
                          </div>
                        </div>

                        <div className="input-group_2">
                          <input
                            type="url"
                            className="edit-input_2"
                            placeholder="Presentation link"
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
                            className={`info-icon_2 ${
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
                            <FaInfoCircle />
                            <div className="info-tooltip_2">
                              Format: https://docs.google.com/presentation/d/...
                            </div>
                          </div>
                        </div>

                        <div className="input-group_2">
                          <input
                            type="url"
                            className="edit-input"
                            placeholder="Video link_2"
                            defaultValue={pub.video_link || ""}
                            onChange={(e) =>
                              handleInputChange(
                                pub.paper_id,
                                "video",
                                e.target.value
                              )
                            }
                          />
                          <div
                            className={`info-icon_2 ${
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
                            <FaInfoCircle />
                            <div className="info-tooltip_2">
                              Format: https://youtube.com/watch?v=... or embed
                              link
                            </div>
                          </div>
                        </div>

                        <button
                          type="button"
                          className="save-button_2"
                          onClick={() =>
                            handleSavePublicationLinks(pub.paper_id)
                          }
                        >
                          {saveStatus[pub.paper_id] || "Save"}
                        </button>
                      </div>
                    </div>
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
          )}

          {totalPages > 1 && (
            <div className="publications-pagination_2">
              <button
                className="pagination-button_2"
                onClick={handlePrevPage}
                disabled={currentPage === 1}
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
                  <path d="M15 18l-6-6 6-6"></path>
                </svg>
                Previous
              </button>

              <span className="pagination-info_2">
                Page {currentPage} of {totalPages}
              </span>

              <button
                className="pagination-button_2"
                onClick={handleNextPage}
                disabled={currentPage === totalPages}
              >
                Next
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
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Add Publication Modal */}
      {showAddForm && (
        <div className="modal-overlay_2">
          <div className="modal-content_2">
            <button
              className="modal-close_2"
              onClick={() => setShowAddForm(false)}
            >
              ×
            </button>
            <h2 className="modal-title_2">Add New Publication</h2>
            <AddPublicationForm
              onSuccess={() => {
                setShowAddForm(false);
                window.location.reload();
              }}
            />
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

export default PublicationPage;
