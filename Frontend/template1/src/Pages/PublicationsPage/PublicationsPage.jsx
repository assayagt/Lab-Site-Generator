import React, { useState, useEffect } from "react";
import "./PublicationsPage.css";
import { getApprovedPublications } from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import AddPublicationForm from "../../Components/AddPublicationForm/AddPubliactionForm";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";
import ErrorPopup from "../../Components/PopUp/ErrorPopup";

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
          const date = new Date(pub.publication_year);
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
      const publicationYear = isNaN(
        new Date(pub.publication_year).getFullYear()
      )
        ? pub.publication_year
        : new Date(pub.publication_year).getFullYear();
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
      const yearA = new Date(a.publication_year).getFullYear();
      const yearB = new Date(b.publication_year).getFullYear();
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

      let success = false;
      if (gitLink !== "") {
        await setPublicationGitLink(sid, domain, paperId, gitLink);
        success = true;
      }
      if (presentationLink !== "") {
        await setPublicationPttxLink(sid, domain, paperId, presentationLink);
        success = true;
      }
      if (videoLink !== "") {
        await setPublicationVideoLink(sid, domain, paperId, videoLink);
        success = true;
      }

      if (success) {
        setPopupMessage("Changes saved successfully!");
        setSaveStatus((prev) => ({ ...prev, [paperId]: "Saved" }));
      } else {
        setErrorMessage("No changes were made.");
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
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [popupMessage, errorMessage]);

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
            <a
              href={pub.publication_link}
              target="_blank"
              rel="noopener noreferrer"
              className="pub_item_link"
            >
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
                <div>
                  <p>
                    <strong>Authors:</strong>{" "}
                    {pub.authors.join(", ") || "Unknown Authors"}
                  </p>
                  <p>
                    <strong>Year:</strong>{" "}
                    {isNaN(new Date(pub.publication_year).getFullYear())
                      ? pub.publication_year
                      : new Date(pub.publication_year).getFullYear()}
                  </p>
                  <p className="description">{pub.description}</p>
                  <div className="links">
                    {pub.git_link && (
                      <a
                        href={pub.git_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="git"
                      >
                        Git
                      </a>
                    )}
                    {pub.presentation_link && (
                      <a
                        href={pub.presentation_link}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="git"
                      >
                        Presentation
                      </a>
                    )}
                  </div>
                </div>
              </div>
            </a>
            {editMode && (
              <form className="publication-form">
                <div className="input-container">
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
                  <label className="hidden-label_pg">GitHub</label>
                </div>

                <div className="input-container">
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
                  <label className="hidden-label_pg">Presentation</label>
                </div>

                <div className="input-container">
                  <input
                    type="url"
                    className="submit-pub_pg"
                    placeholder="Enter Video link"
                    defaultValue={pub.video_link || ""}
                    onChange={(e) =>
                      handleInputChange(pub.paper_id, "video", e.target.value)
                    }
                  />
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
            <AddPublicationForm onSuccess={() => setShowAddForm(false)} />
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
