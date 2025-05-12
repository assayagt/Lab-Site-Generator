import React, { useState, useEffect, useContext } from "react";
import "./AccountPage2.css";
import accountIcon from "../../images/account_avatar.svg";
import AddPublicationForm from "../../Components/AddPublicationForm/AddPubliactionForm";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";
import ErrorPopup from "../../Components/PopUp/ErrorPopup";
import { useNavigate, useLocation } from "react-router-dom";

import {
  getUserDetails,
  approveRegistration,
  rejectRegistration,
  setPublicationGitLink,
  setPublicationPttxLink,
  setPublicationVideoLink,
  setBioByMember,
  setDegreeByMember,
  setSecondEmailByMember,
  setLinkedInLinkByMember,
  getMemberPublications,
  finalApprovePublicationByManager,
  initialApprovePublicationByAuthor,
  rejectPublication,
} from "../../services/websiteService";
import { fetchUserNotifications } from "../../services/UserService";
import { NotificationContext } from "../../Context/NotificationContext";

const AccountPage = () => {
  const location = useLocation(); // Add this

  const [activeSection, setActiveSection] = useState(() => {
    const params = new URLSearchParams(location.search);
    const section = params.get("section");
    return section || "personal-info";
  });

  // ... rest of your existing state definitions

  // Optional: Update active section when URL changes
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const section = params.get("section");
    if (
      section &&
      ["personal-info", "my-publications", "notifications"].includes(section)
    ) {
      setActiveSection(section);
    }
  }, [location.search]);
  const [userDetails, setUserDetails] = useState({
    bio: "",
    email: "",
    secondaryEmail: "",
    degree: "",
    linkedIn: "",
    fullname: "",
  });
  const [showApprovalModal, setShowApprovalModal] = useState(false);
  const [popupMessage, setPopupMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [saveButtonText, setSaveButtonText] = useState("Save Changes");
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [selectedNotification, setSelectedNotification] = useState(null);
  const [approvalForm, setApprovalForm] = useState({
    fullName: "",
    degree: "",
  });

  const [publications, setPublications] = useState([]);
  const [uploadedPhoto, setUploadedPhoto] = useState(accountIcon);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 3; // Reduced items per page for cleaner display
  const [searchTerm, setSearchTerm] = useState("");
  const [isAddPublicationModalOpen, setIsAddPublicationModalOpen] =
    useState(false);
  const {
    notifications,
    markNotificationAsRead,
    updateNotifications,
    setHasNewNotifications,
  } = useContext(NotificationContext);

  // Fetch user details and publications on load
  useEffect(() => {
    const fetchData = async () => {
      try {
        const domain = sessionStorage.getItem("domain");
        const sid = sessionStorage.getItem("sid");

        // Fetch user details
        const userData = await getUserDetails(domain, sid);
        if (userData) {
          setUserDetails({
            bio: userData.user.bio || "",
            email: userData.user.email || "",
            secondaryEmail: userData.user.secondEmail || "",
            degree: userData.user.degree || "",
            linkedIn: userData.user.linkedin_link || "",
            fullname: userData.user.fullName,
          });
        }

        // Fetch publications
        const pubData = await getMemberPublications(domain);
        setPublications(pubData || []);
      } catch (error) {
        console.error("Error fetching data:", error);
        setErrorMessage(
          "Failed to load your account data. Please try again later."
        );
      }
    };

    fetchData();
  }, []);

  // Handle section changes
  const handleSectionChange = (section) => {
    setActiveSection(section);
  };

  // Fetch and update notifications when viewing notifications section
  const [isLoadingNotifications, setIsLoadingNotifications] = useState(false);

  // Replace the existing notification fetching effect with this:
  useEffect(() => {
    const fetchAndUpdateNotifications = async () => {
      if (activeSection === "notifications" && !isLoadingNotifications) {
        const email = sessionStorage.getItem("userEmail");
        if (email) {
          setIsLoadingNotifications(true);
          try {
            const updatedNotifications = await fetchUserNotifications(email);
            updateNotifications(updatedNotifications);
            setHasNewNotifications(false);
          } catch (error) {
            console.error("Error fetching notifications:", error);
          } finally {
            setIsLoadingNotifications(false);
          }
        }
      }
    };

    fetchAndUpdateNotifications();
  }, [activeSection]); // Only depend on activeSection

  // Clear popup messages after delay
  useEffect(() => {
    if (popupMessage || errorMessage) {
      const timer = setTimeout(() => {
        setPopupMessage("");
        setErrorMessage("");
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [popupMessage, errorMessage]);

  // Photo upload handling
  const handleUploadPhoto = () => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "image/*";
    fileInput.onchange = (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          setUploadedPhoto(reader.result);
        };
        reader.readAsDataURL(file);
      }
    };
    fileInput.click();
  };

  // Update form fields
  const handleChange = (field, value) => {
    setUserDetails((prev) => ({ ...prev, [field]: value }));
    setHasUnsavedChanges(true);
    setSaveButtonText("Save Changes");
  };

  // Save user information changes
  const handleSaveChanges = async () => {
    try {
      setSaveButtonText("Saving...");
      const sid = sessionStorage.getItem("sid");
      const domain = sessionStorage.getItem("domain");

      // Track if any update was successful
      let isUpdated = false;
      let res = null;

      if (userDetails.bio) {
        res = await setBioByMember(sid, userDetails.bio, domain);
        if (res?.response === "true") {
          isUpdated = true;
        }
      }

      if (userDetails.secondaryEmail) {
        res = await setSecondEmailByMember(
          sid,
          userDetails.secondaryEmail,
          domain
        );
        if (res?.response === "true") {
          isUpdated = true;
        }
      }

      if (userDetails.degree) {
        res = await setDegreeByMember(sid, userDetails.degree, domain);
        if (res?.response === "true") {
          isUpdated = true;
        }
      }

      if (userDetails.linkedIn) {
        res = await setLinkedInLinkByMember(sid, userDetails.linkedIn, domain);
        if (res?.response === "true") {
          isUpdated = true;
        }
      }

      if (isUpdated) {
        setPopupMessage("Your profile has been updated successfully!");
        setSaveButtonText("Saved");
        setHasUnsavedChanges(false);
      } else {
        setErrorMessage("Error: " + (res?.message || "Failed to save changes"));
        setSaveButtonText("Save Changes");
      }
    } catch (error) {
      console.error("Error saving changes:", error);
      setErrorMessage(`An error occurred: ${error.message}`);
      setSaveButtonText("Save Changes");
    }
  };

  // Handle notification approvals
  const handleApproveNotification = async (notif) => {
    setSelectedNotification(notif);
    const sid = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    if (notif.subject === "New Registration Request Pending Approval") {
      setShowApprovalModal(true);
    } else if (notif.subject === "New Publication Pending Final Approval") {
      const response = await finalApprovePublicationByManager(
        sid,
        domain,
        notif.id
      );
      if (response?.response === "true") {
        markNotificationAsRead(notif.id);
        setPopupMessage("Publication approved successfully.");
      } else {
        setErrorMessage("Failed to approve publication.");
      }
    } else if (notif.subject === "New Publication Pending Approval") {
      const response = await initialApprovePublicationByAuthor(
        sid,
        domain,
        notif.id
      );
      if (response?.response === "true") {
        markNotificationAsRead(notif.id);
        setPopupMessage("Publication approved successfully.");
      } else {
        setErrorMessage("Failed to approve publication.");
      }
    } else {
      setErrorMessage("Unknown notification type.");
    }
  };

  // Handle notification rejections
  const handleRejectNotification = async (notif) => {
    const sid = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    if (notif.subject === "New Registration Request Pending Approval") {
      const payload = {
        domain: domain,
        manager_userId: sid,
        notification_id: notif.id,
      };

      const response = await rejectRegistration(payload);
      if (response) {
        markNotificationAsRead(notif.id);
        setPopupMessage("Registration request rejected.");
      } else {
        setErrorMessage("Failed to reject registration request.");
      }
    } else if (
      notif.subject === "New Publication Pending Final Approval" ||
      notif.subject === "New Publication Pending Approval"
    ) {
      const response = await rejectPublication(sid, domain, notif.id);
      if (response?.response === "true") {
        markNotificationAsRead(notif.id);
        setPopupMessage("Publication rejected.");
      } else {
        setErrorMessage("Failed to reject publication.");
      }
    } else {
      setErrorMessage("Unknown notification type.");
    }
  };

  // Submit registration approval with user details
  const handleSubmitApproval = async () => {
    if (!approvalForm.fullName || !approvalForm.degree) {
      setErrorMessage("Please complete all fields.");
      return;
    }

    const payload = {
      domain: sessionStorage.getItem("domain"),
      manager_userId: sessionStorage.getItem("sid"),
      requested_full_name: approvalForm.fullName,
      requested_degree: approvalForm.degree,
      notification_id: selectedNotification.id,
    };

    try {
      const response = await approveRegistration(payload);
      if (response) {
        markNotificationAsRead(selectedNotification.id);
        setShowApprovalModal(false);
        setApprovalForm({ fullName: "", degree: "" });
        setSelectedNotification(null);
        setPopupMessage("Registration approved successfully.");
      } else {
        setErrorMessage("Failed to approve registration.");
      }
    } catch (error) {
      setErrorMessage("An error occurred while approving registration.");
    }
  };

  // Filter publications based on search term
  const filteredPublications = publications.filter((pub) =>
    pub.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Pagination calculations
  const totalPages = Math.ceil(filteredPublications.length / itemsPerPage);
  const paginatedPublications = filteredPublications.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  // Pagination navigation
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

  // Save publication links
  const handleSavePublicationLinks = async (publication) => {
    try {
      const sid = sessionStorage.getItem("sid");
      const domain = sessionStorage.getItem("domain");
      let isUpdated = false;

      if (publication.github) {
        const githubResponse = await setPublicationGitLink(
          sid,
          domain,
          publication.id,
          publication.github
        );
        if (githubResponse === "true") {
          isUpdated = true;
        }
      }

      if (publication.presentation) {
        const presentationResponse = await setPublicationPttxLink(
          sid,
          domain,
          publication.id,
          publication.presentation
        );
        if (presentationResponse === "true") {
          isUpdated = true;
        }
      }

      if (publication.video) {
        const videoResponse = await setPublicationVideoLink(
          sid,
          domain,
          publication.id,
          publication.video
        );
        if (videoResponse === "true") {
          isUpdated = true;
        }
      }

      if (isUpdated) {
        setPopupMessage("Publication links updated successfully!");
      } else {
        setErrorMessage("No changes were saved.");
      }
    } catch (error) {
      console.error("Error updating publication links:", error);
      setErrorMessage(`An error occurred: ${error.message}`);
    }
  };

  // Format notification content
  const renderNotification = (body) => {
    const lines = body
      .split("\n")
      .slice(1) // Skip the first line
      .filter((line) => line.trim() !== "");

    return (
      <div className="notification__content">
        {lines.map((line, index) => {
          if (line.startsWith("Link: ")) {
            const url = line.replace("Link: ", "").trim();
            return (
              <div className="notification__link" key={index}>
                <span>Link:</span>
                <a href={url} target="_blank" rel="noopener noreferrer">
                  {url}
                </a>
              </div>
            );
          }
          return <p key={index}>{line}</p>;
        })}
      </div>
    );
  };

  return (
    <div className="account">
      <div className="account__container">
        <div className="account__sidebar">
          <h2 className="account__sidebar-title">My Account</h2>
          <nav className="account__nav">
            <button
              className={`account__nav-link ${
                activeSection === "personal-info" ? "active" : ""
              }`}
              onClick={() => handleSectionChange("personal-info")}
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
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span>Personal Information</span>
            </button>

            <button
              className={`account__nav-link ${
                activeSection === "my-publications" ? "active" : ""
              }`}
              onClick={() => handleSectionChange("my-publications")}
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
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
              </svg>
              <span>Publications</span>
            </button>

            <button
              className={`account__nav-link ${
                activeSection === "notifications" ? "active" : ""
              }`}
              onClick={() => handleSectionChange("notifications")}
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
                <path d="M22 17H2a3 3 0 0 0 3-3V9a7 7 0 0 1 14 0v5a3 3 0 0 0 3 3zm-8.27 4a2 2 0 0 1-3.46 0"></path>
              </svg>
              <span>Notifications</span>
              {notifications && notifications.length > 0 && (
                <span className="account__notification-badge">
                  {notifications.length}
                </span>
              )}
            </button>
          </nav>
        </div>

        <div className="account__content">
          {/* Personal Information Section */}
          {activeSection === "personal-info" && (
            <div className="profile-section">
              <h1 className="profile-section__title">Personal Information</h1>

              <div className="profile-section__content">
                <div className="profile-photo">
                  <div className="profile-photo__container">
                    <img
                      src={uploadedPhoto}
                      alt="Profile"
                      className="profile-photo__image"
                    />
                    <button
                      className="profile-photo__upload"
                      onClick={handleUploadPhoto}
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
                        <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                        <circle cx="12" cy="13" r="4"></circle>
                      </svg>
                    </button>
                  </div>
                  <h3 className="profile-photo__name">
                    {userDetails.fullname}
                  </h3>
                  <span className="profile-photo__email">
                    {userDetails.email}
                  </span>
                </div>

                <div className="profile-form">
                  <div className="form-field">
                    <label htmlFor="bio" className="form-field__label">
                      Bio
                    </label>
                    <textarea
                      id="bio"
                      className="form-field__textarea"
                      value={userDetails.bio}
                      onChange={(e) => handleChange("bio", e.target.value)}
                      placeholder="Tell us about yourself and your research interests"
                      rows={4}
                    />
                  </div>

                  <div className="form-field">
                    <label
                      htmlFor="secondaryEmail"
                      className="form-field__label"
                    >
                      Secondary Email
                    </label>
                    <input
                      id="secondaryEmail"
                      type="email"
                      className="form-field__input"
                      value={userDetails.secondaryEmail}
                      onChange={(e) =>
                        handleChange("secondaryEmail", e.target.value)
                      }
                      placeholder="Alternative email address"
                    />
                  </div>

                  <div className="form-field">
                    <label htmlFor="degree" className="form-field__label">
                      Academic Degree
                    </label>
                    <input
                      id="degree"
                      type="text"
                      className="form-field__input"
                      value={userDetails.degree}
                      onChange={(e) => handleChange("degree", e.target.value)}
                      placeholder="Your highest degree (e.g., Ph.D., M.Sc.)"
                    />
                  </div>

                  <div className="form-field">
                    <label htmlFor="linkedin" className="form-field__label">
                      LinkedIn Profile
                    </label>
                    <input
                      id="linkedin"
                      type="url"
                      className="form-field__input"
                      value={userDetails.linkedIn}
                      onChange={(e) => handleChange("linkedIn", e.target.value)}
                      placeholder="https://linkedin.com/in/yourprofile"
                    />
                  </div>

                  <div className="form-actions">
                    <button
                      className={`button ${
                        hasUnsavedChanges
                          ? "button--primary"
                          : "button--disabled"
                      }`}
                      onClick={handleSaveChanges}
                      disabled={!hasUnsavedChanges}
                    >
                      {saveButtonText}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Publications Section */}
          {activeSection === "my-publications" && (
            <div className="publications-section">
              <div className="publications-section__header">
                <h1 className="publications-section__title">My Publications</h1>

                <div className="publications-section__controls">
                  <div className="search-field">
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
                      <circle cx="11" cy="11" r="8"></circle>
                      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input
                      type="text"
                      placeholder="Search publications..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="search-field__input"
                    />
                  </div>

                  <button
                    className="button button--primary"
                    onClick={() => setIsAddPublicationModalOpen(true)}
                  >
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
                      <line x1="12" y1="5" x2="12" y2="19"></line>
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                    </svg>
                    Add Publication
                  </button>
                </div>
              </div>

              {filteredPublications.length === 0 ? (
                <div className="publications-section__empty">
                  <p>
                    No publications found. Add your first publication by
                    clicking the button above.
                  </p>
                </div>
              ) : (
                <>
                  <div className="publication-cards">
                    {paginatedPublications.map((publication) => (
                      <div key={publication.id} className="publication-card">
                        <div className="publication-card__header">
                          <h3 className="publication-card__title">
                            {publication.title}
                          </h3>
                          <span className="publication-card__year">
                            {publication.publication_year}
                          </span>
                        </div>

                        <div className="publication-card__authors">
                          {publication.authors}
                        </div>

                        <div className="publication-card__journal">
                          {publication.journal_name}
                        </div>

                        <div className="publication-card__links">
                          <div className="form-field">
                            <label className="form-field__label">
                              GitHub Repository
                            </label>
                            <input
                              type="url"
                              className="form-field__input"
                              defaultValue={publication.github || ""}
                              placeholder="https://github.com/username/repo"
                              onChange={(e) =>
                                (publication.github = e.target.value)
                              }
                            />
                          </div>

                          <div className="form-field">
                            <label className="form-field__label">
                              Presentation
                            </label>
                            <input
                              type="url"
                              className="form-field__input"
                              defaultValue={publication.presentation || ""}
                              placeholder="Link to presentation slides"
                              onChange={(e) =>
                                (publication.presentation = e.target.value)
                              }
                            />
                          </div>

                          <div className="form-field">
                            <label className="form-field__label">Video</label>
                            <input
                              type="url"
                              className="form-field__input"
                              defaultValue={publication.video || ""}
                              placeholder="Link to video presentation"
                              onChange={(e) =>
                                (publication.video = e.target.value)
                              }
                            />
                          </div>
                        </div>

                        <div className="publication-card__actions">
                          <button
                            className="button button--secondary"
                            onClick={() =>
                              handleSavePublicationLinks(publication)
                            }
                          >
                            Save Changes
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>

                  {totalPages > 1 && (
                    <div className="pagination">
                      <button
                        className="pagination__button"
                        onClick={handlePrevPage}
                        disabled={currentPage === 1}
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
                          <polyline points="15 18 9 12 15 6"></polyline>
                        </svg>
                        Previous
                      </button>

                      <span className="pagination__info">
                        Page {currentPage} of {totalPages}
                      </span>

                      <button
                        className="pagination__button"
                        onClick={handleNextPage}
                        disabled={currentPage === totalPages}
                      >
                        Next
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
                          <polyline points="9 18 15 12 9 6"></polyline>
                        </svg>
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>
          )}

          {/* Notifications Section */}
          {activeSection === "notifications" && (
            <div className="notifications-section">
              <h1 className="notifications-section__title">Notifications</h1>

              {!notifications || notifications.length === 0 ? (
                <div className="notifications-section__empty">
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
                    <path d="M22 17H2a3 3 0 0 0 3-3V9a7 7 0 0 1 14 0v5a3 3 0 0 0 3 3zm-8.27 4a2 2 0 0 1-3.46 0"></path>
                  </svg>
                  <p>You have no notifications at this time.</p>
                </div>
              ) : (
                <div className="notification-list">
                  {notifications.map((notif) => (
                    <div key={notif.id} className="notification">
                      <div className="notification__header">
                        <h3 className="notification__subject">
                          {notif.subject}
                        </h3>
                      </div>

                      {renderNotification(notif.body)}

                      <div className="notification__actions">
                        <button
                          className="button button--outline-danger"
                          onClick={() => handleRejectNotification(notif)}
                        >
                          Reject
                        </button>
                        <button
                          className="button button--primary"
                          onClick={() => handleApproveNotification(notif)}
                        >
                          Approve
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
      {/* Add Publication Modal */}
      {isAddPublicationModalOpen && (
        <div
          className="modal"
          onClick={() => setIsAddPublicationModalOpen(false)}
        >
          <div className="modal__content" onClick={(e) => e.stopPropagation()}>
            <button
              className="modal__close"
              onClick={() => setIsAddPublicationModalOpen(false)}
            >
              ×
            </button>
            <h2 className="modal__title">Add New Publication</h2>
            <AddPublicationForm
              onSuccess={() => {
                setIsAddPublicationModalOpen(false);
                setPopupMessage("Publication added successfully!");
                // Refresh publications
                getMemberPublications(sessionStorage.getItem("domain")).then(
                  (data) => setPublications(data || [])
                );
              }}
            />
          </div>
        </div>
      )}
      {/* Approval Modal */}
      {showApprovalModal && (
        <div className="modal" onClick={() => setShowApprovalModal(false)}>
          <div className="modal__content" onClick={(e) => e.stopPropagation()}>
            <button
              className="modal__close"
              onClick={() => setShowApprovalModal(false)}
            >
              ×
            </button>
            <h2 className="modal__title">Approve Registration</h2>

            <div className="form-field">
              <label className="form-field__label">Full Name</label>
              <input
                type="text"
                className="form-field__input"
                value={approvalForm.fullName}
                onChange={(e) =>
                  setApprovalForm({ ...approvalForm, fullName: e.target.value })
                }
                placeholder="Enter full name"
              />
            </div>

            <div className="form-field">
              <label className="form-field__label">Academic Degree</label>
              <select
                className="form-field__select"
                value={approvalForm.degree}
                onChange={(e) =>
                  setApprovalForm({ ...approvalForm, degree: e.target.value })
                }
              >
                <option value="">Select Degree</option>
                <option value="B.Sc.">B.Sc.</option>
                <option value="M.Sc.">M.Sc.</option>
                <option value="Ph.D.">Ph.D.</option>
                <option value="Faculty Member">Faculty Member</option>
                <option value="Research Assistant">Research Assistant</option>
              </select>
            </div>

            <div className="modal__actions">
              <button
                className="button button--outline"
                onClick={() => setShowApprovalModal(false)}
              >
                Cancel
              </button>
              <button
                className="button button--primary"
                onClick={handleSubmitApproval}
              >
                Approve
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Success and Error Popups */}
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

export default AccountPage;
