import React, { useState, useEffect, useContext, useRef } from "react";
import "./AccountPage.css";
import { useNavigate, useLocation } from "react-router-dom";

import accountIcon from "../../images/account_avatar.svg";
import cameraIcon from "../../images/camera_icon.svg";
import searchIcon from "../../images/search_icon.svg";
import AddPublicationForm from "../../Components/AddPublicationForm/AddPubliactionForm";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";
import LoadingPopup from "../../Components/PopUp/LoadingPopup";
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
  getNotApprovedMemberPublications,
  setScholarLinkByMember,
  initialApproveMultiplePublicationsByAuthor,
  rejectMultiplePublications,
} from "../../services/websiteService";
import {
  fetchUserNotifications,
  uploadProfilePicture,
} from "../../services/UserService";
import { NotificationContext } from "../../Context/NotificationContext";
import ErrorPopup from "../../Components/PopUp/ErrorPopup";

const AccountPage = () => {
  const location = useLocation();
  // Add file input ref and selected file state
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);

  const [activeSection, setActiveSection] = useState(() => {
    const params = new URLSearchParams(location.search);
    const section = params.get("section");
    return section || "personal-info";
  });
  const [userDetails, setUserDetails] = useState({
    bio: "",
    email: "",
    secondaryEmail: "",
    degree: "",
    linkedIn: "",
    fullname: "",
    google_scholar: "",
    emailNotifications: true, // New field for email notifications
    profile_picture: "",
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
  const [crawledPublications, setCrawledPublications] = useState([]);
  const [selectedPublications, setSelectedPublications] = useState([]);
  const [currentPublicationType, setCurrentPublicationType] =
    useState("manual");
  const [statusFilter, setStatusFilter] = useState("all");
  const [uploadedPhoto, setUploadedPhoto] = useState(
    userDetails.profile_picture || accountIcon
  );
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;
  const [searchTerm, setSearchTerm] = useState("");
  const [isAddPublicationModalOpen, setIsAddPublicationModalOpen] =
    useState(false);
  const {
    notifications,
    markNotificationAsRead,
    updateNotifications,
    setHasNewNotifications,
  } = useContext(NotificationContext); // Get notifications
  const [isLoading, setIsLoading] = useState(false);

  // Add this useEffect to your AccountPage component, right after your existing useEffects
  // This listens for the custom event from the Header component

  useEffect(() => {
    // Function to handle section change events
    const handleSectionEvent = (event) => {
      if (event.detail && event.detail.section) {
        setActiveSection(event.detail.section);

        // Update the URL to match the new section (optional but helps with consistency)
        const url = new URL(window.location);
        url.searchParams.set("section", event.detail.section);
        window.history.replaceState({}, "", url);
      }
    };

    // Add event listener for the custom event
    document.addEventListener("NAVIGATE_TO_SECTION", handleSectionEvent);

    // Cleanup function to remove event listener
    return () => {
      document.removeEventListener("NAVIGATE_TO_SECTION", handleSectionEvent);
    };
  }, []);

  // Also update your existing URL parameter useEffect to handle both initial load
  // and subsequent navigation within the same page:

  useEffect(() => {
    if (userDetails.profile_picture) {
      setUploadedPhoto(userDetails.profile_picture);
    }
  }, [userDetails.profile_picture]);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const section = params.get("section");
    if (section) {
      setActiveSection(section);
    }
  }, [location.search]); // This will run when the URL parameters change

  useEffect(() => {
    // Fetch user details
    const fetchUserDetails = async () => {
      const data = await getUserDetails(
        sessionStorage.getItem("domain"),
        sessionStorage.getItem("sid")
      );
      if (data) {
        console.log(data);
        setUserDetails({
          bio: data.user.bio || "",
          email: data.user.email || "",
          secondaryEmail: data.user.secondEmail || "",
          degree: data.user.degree || "",
          linkedIn: data.user.linkedin_link || "",
          fullname: data.user.fullName,
          emailNotifications: data.user.emailNotifications !== false, // Default to true if not set
          google_scholar: data.user.scholar_link || "",
          profile_picture: data.user.profile_picture || "",
        });
      }
    };

    const fetchPublications = async () => {
      const domain = sessionStorage.getItem("domain");
      const data = await getMemberPublications(domain);
      console.log("Fetched Publications:", data); // Debugging log
      setPublications(data || []);
    };

    const fetchCrawledPublications = async () => {
      const domain = sessionStorage.getItem("domain");
      // You'll need to implement this API method
      const data = await getNotApprovedMemberPublications(
        domain,
        sessionStorage.getItem("sid")
      );

      console.log("Fetched Crawled Publications:", data);
      setCrawledPublications(data);
    };

    fetchUserDetails();
    fetchPublications();
    fetchCrawledPublications();
  }, []);

  const handleSectionChange = (section) => {
    setActiveSection(section);
    if (section != "my-publications") {
      setCurrentPublicationType("manual");
      setStatusFilter("all");
    }
  };

  useEffect(() => {
    const fetchAndUpdateNotifications = async () => {
      if (activeSection === "notifications") {
        const email = sessionStorage.getItem("userEmail");
        if (email) {
          const updatedNotifications = await fetchUserNotifications(email);
          updateNotifications(updatedNotifications);
        }
      }
    };

    fetchAndUpdateNotifications();
  }, [activeSection]);

  const handleUploadPhoto = () => {
    // Trigger the hidden file input
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };
  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Validate file type
      const allowedTypes = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/gif",
      ];
      if (!allowedTypes.includes(file.type)) {
        setErrorMessage(
          "Please select a valid image file (JPEG, PNG, or GIF)."
        );
        return;
      }

      // Validate file size (e.g., max 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB in bytes
      if (file.size > maxSize) {
        setErrorMessage("File size must be less than 5MB.");
        return;
      }

      setSelectedFile(file);

      // Create a preview URL and update the displayed photo
      const previewUrl = URL.createObjectURL(file);
      setUploadedPhoto(previewUrl);

      // Clear any previous error messages
      setErrorMessage("");
    }
  };
  const handleSavePhoto = async () => {
    if (!selectedFile) {
      setErrorMessage("Please select a photo first.");
      return;
    }

    try {
      const response = await uploadProfilePicture(
        selectedFile,
        sessionStorage.getItem("domain")
      );
      console.log(response);
    } catch (error) {
      setErrorMessage("Error uploading photo.");
    }
  };

  const handleApproveNotification = async (notif) => {
    setSelectedNotification(notif);

    const sid = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    if (notif.subject === "New Registration Request Pending Approval") {
      setShowApprovalModal(true); // Open modal to get name + degree
    } else if (notif.subject === "New Publication Pending Final Approval") {
      const response = await finalApprovePublicationByManager(
        sid,
        domain,
        notif.id
      );
      if (response?.response === "true") {
        markNotificationAsRead(notif.id);
        setPopupMessage("Publication approved by manager.");
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
        setPopupMessage("Publication approved by author.");
      } else {
        setErrorMessage("Failed to approve publication.");
      }
    } else {
      setErrorMessage("Unknown notification type.");
    }
  };

  const handleSubmitApproval = async () => {
    const payload = {
      domain: sessionStorage.getItem("domain"),
      manager_userId: sessionStorage.getItem("sid"),
      requested_full_name: approvalForm.fullName,
      requested_degree: approvalForm.degree,
      notification_id: selectedNotification.id,
    };

    const response = await approveRegistration(payload);
    if (response) {
      markNotificationAsRead(selectedNotification.id);
      setShowApprovalModal(false);
      setApprovalForm({ fullName: "", degree: "" });
      setSelectedNotification(null);
    } else {
      setErrorMessage("An error occurred while saving changes.");
    }
  };

  useEffect(() => {
    if (activeSection === "notifications") {
      setHasNewNotifications(false); // ✅ Now inside an effect, safe to call
    }
  }, [activeSection, setHasNewNotifications]);
  useEffect(() => {
    if (popupMessage) {
      const timer = setTimeout(() => setPopupMessage(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [popupMessage]);

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
        setPopupMessage("Registration rejected.");
      } else {
        setErrorMessage("Failed to reject registration.");
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
  const filteredPublications = publications.filter((pub) =>
    pub.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const cloned = [...crawledPublications]; // avoids referencing original state
  const filteredCrawledPublications = cloned
    .filter((pub) => pub.title.toLowerCase().includes(searchTerm.toLowerCase()))
    .filter((pub) => {
      const status = pub.status;
      // Exclude approved publications from showing up
      if (status === "Approved") return false;
      return statusFilter === "all" || status === statusFilter;
    });

  const totalPages = Math.ceil(filteredPublications.length / itemsPerPage);
  const totalCrawledPages = Math.ceil(
    filteredCrawledPublications.length / itemsPerPage
  );
  const paginatedPublications = filteredPublications.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const paginatedCrawledPublications = filteredCrawledPublications.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handleSelectPublication = (publicationId) => {
    setSelectedPublications((prev) => {
      if (prev.includes(publicationId)) {
        return prev.filter((id) => id !== publicationId);
      } else {
        return [...prev, publicationId];
      }
    });
  };

  const handlePublicationLinkChange = (paperId, field, value) => {
    setPublications((prev) =>
      prev.map((pub) =>
        pub.paper_id === paperId ? { ...pub, [field]: value } : pub
      )
    );
  };

  const handleBulkApprove = async () => {
    try {
      // TODO: Call API to bulk approve
      // const response = await bulkApproveCrawledPublications(selectedPublications);

      // Update local state
      setIsLoading(true); // ✅ Show loading popup

      const response = await initialApproveMultiplePublicationsByAuthor(
        sessionStorage.getItem("sid"),
        sessionStorage.getItem("domain"),
        selectedPublications.join(", ")
      );
      if (response.response === "true") {
        setSelectedPublications([]);
        setPopupMessage(
          `${selectedPublications.length} publications approved, you will see them in a few minutes on website`
        );
        setCrawledPublications((prev) =>
          prev.map((pub) =>
            selectedPublications.includes(pub.paper_id)
              ? { ...pub, status: "Approved" } // or "rejected"
              : pub
          )
        );
      } else {
        setErrorMessage("Failed to approve publications: " + response.message);
      }
    } catch (error) {
      setErrorMessage("Failed to approve publications");
    } finally {
      setIsLoading(false); // ✅ Hide loading popup
    }
  };

  const handleBulkReject = async () => {
    try {
      const response = await rejectMultiplePublications(
        sessionStorage.getItem("sid"),
        sessionStorage.getItem("domain"),
        selectedPublications
      );
      if (response.response === "true") {
        setSelectedPublications([]);
        setPopupMessage(`${selectedPublications.length} publications rejected`);
        setCrawledPublications((prev) =>
          prev.map((pub) =>
            selectedPublications.includes(pub.paper_id)
              ? { ...pub, status: "Rejected" } // or "rejected"
              : pub
          )
        );
      } else {
        setErrorMessage("Failed to reject publications: " + response.message);
      }
    } catch (error) {
      setErrorMessage("Failed to reject publications");
    }
  };

  const handleNextPage = () => {
    const maxPages =
      currentPublicationType === "manual" ? totalPages : totalCrawledPages;
    if (currentPage < maxPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleSavePublicationLinks = async (publication) => {
    try {
      let isUpdated = false; // Track if any field was successfully updated
      const sid = sessionStorage.getItem("sid");
      const domain = sessionStorage.getItem("domain");
      if (publication.git_link) {
        const githubResponse = await setPublicationGitLink(
          sid,
          domain,
          publication.paper_id,
          publication.git_link
        );
        if (githubResponse.response === "true") {
          console.log(githubResponse);
          isUpdated = true;
        } else {
          console.log(githubResponse);
          isUpdated = false;
        }
      }

      if (publication.presentation_link) {
        const presentationResponse = await setPublicationPttxLink(
          sid,
          domain,
          publication.paper_id,
          publication.presentation_link
        );
        if (presentationResponse.response === "true") {
          isUpdated = true;
        } else {
          isUpdated = false;
        }
      }

      if (publication.video_link) {
        const videoResponse = await setPublicationVideoLink(
          sid,
          domain,
          publication.paper_id,
          publication.video_link
        );
        if (videoResponse.response === "true") {
          isUpdated = true;
        } else {
          isUpdated = false;
        }
      }

      if (isUpdated) {
        setPopupMessage("Links updated successfully!");
      } else {
        setErrorMessage("An error occurred while saving changes.");
      }
    } catch (error) {
      console.error("Error updating publication links:", error);
      setErrorMessage(`An error occurred: ${error.message}`);
    }
  };
  const handleChange = (field, value) => {
    setUserDetails((prev) => ({ ...prev, [field]: value }));
    setHasUnsavedChanges(true);
    setSaveButtonText("Save Changes");
  };

  const handleSaveChanges = async () => {
    try {
      const sid = sessionStorage.getItem("sid");
      const domain = sessionStorage.getItem("domain");
      // Track if any update was successful
      let isUpdated = false;
      let res = null;
      if (userDetails.bio) {
        res = await setBioByMember(sid, userDetails.bio, domain);
        if (res?.response === "true") {
          isUpdated = true;
        } else {
          isUpdated = false;
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
        } else {
          isUpdated = false;
        }
      }

      if (userDetails.degree) {
        res = await setDegreeByMember(sid, userDetails.degree, domain);
        if (res?.response === "true") {
          isUpdated = true;
        } else {
          isUpdated = false;
        }
      }

      if (userDetails.linkedIn) {
        res = await setLinkedInLinkByMember(sid, userDetails.linkedIn, domain);
        if (res?.response === "true") {
          isUpdated = true;
        } else {
          isUpdated = false;
        }
      }
      if (userDetails.google_scholar) {
        res = await setScholarLinkByMember(
          sid,
          userDetails.google_scholar,
          domain
        );
        if (res?.response === "true") {
          isUpdated = true;
        } else {
          isUpdated = false;
        }
      }

      // Handle email notification preference
      // You'll need to add a new API method for this
      // For now, we'll just simulate the update
      console.log(
        "Email notifications preference:",
        userDetails.emailNotifications
      );
      // TODO: Call API to update email notification preference
      // res = await setEmailNotificationPreference(sid, userDetails.emailNotifications, domain);

      if (isUpdated) {
        setPopupMessage("Changes saved successfully!");
        setSaveButtonText("Saved");
        setHasUnsavedChanges(false);
      } else {
        console.log(res);
        setErrorMessage("Error: " + res?.message);
      }
    } catch (error) {
      console.error("Error saving changes:", error);
      setErrorMessage(`An error occurred: ${error.message}`);
    }
  };

  const renderNotification = (body) => {
    const lines = body
      .split("\n")
      .slice(1) // Skip the first line
      .filter((line) => line.trim() !== "");

    return (
      <div className="notification-body">
        {lines.map((line, index) => {
          if (line.startsWith("Link: ")) {
            const url = line.replace("Link: ", "").trim();
            return (
              <div className="link_notification" key={index}>
                <div>Link:</div>{" "}
                <a href={url} target="_blank" rel="noopener noreferrer">
                  {url}
                </a>
              </div>
            );
          }
          return <div key={index}>{line}</div>;
        })}
      </div>
    );
  };

  return (
    <div className="account-page">
      <Sidebar
        activeSection={activeSection}
        onSectionChange={handleSectionChange}
      />
      <div className="main-content">
        {activeSection === "personal-info" && (
          <form
            id="personal-info"
            className="personal-info"
            onSubmit={(e) => e.preventDefault()}
          >
            <h2 className="title_account">Personal Information</h2>
            <div className="info">
              <div className="user-photo-div">
                <img src={uploadedPhoto} alt="User" className="user-photo" />
                <div className="camera-icon" onClick={handleUploadPhoto}>
                  <img src={cameraIcon} alt="Upload" />
                </div>
                {/* Hidden file input */}
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  style={{ display: "none" }}
                />
                <button
                  className="save-photo"
                  onClick={handleSavePhoto}
                  disabled={!selectedFile}
                  style={{
                    opacity: selectedFile ? 1 : 0.6,
                    cursor: selectedFile ? "pointer" : "not-allowed",
                  }}
                >
                  {selectedFile ? "Save Photo" : "Select Photo"}
                </button>
                {selectedFile && (
                  <div className="file-info">
                    <small>Selected: {selectedFile.name}</small>
                  </div>
                )}
              </div>
              <div className="details">
                <label className="detail-bio">
                  <div className="text-detail">{userDetails.email}</div>
                </label>
                <div className="coolinput">
                  <label htmlFor="input" className="text">
                    Bio:
                  </label>
                  <textarea
                    type="text"
                    placeholder="Bio"
                    name="input"
                    className="input input_bio"
                    value={userDetails.bio}
                    onChange={(e) => handleChange("bio", e.target.value)}
                  />
                </div>
                <div className="coolinput">
                  <label htmlFor="input" className="text">
                    Secondary Email:
                  </label>
                  <input
                    type="text"
                    placeholder="Secondary Email"
                    name="input"
                    className="input"
                    value={userDetails.secondaryEmail}
                    onChange={(e) =>
                      handleChange("secondaryEmail", e.target.value)
                    }
                  />
                </div>
                <div className="coolinput">
                  <label htmlFor="degreeSelect" className="text">
                    Degree:
                  </label>
                  <select
                    id="degreeSelect"
                    className="input"
                    value={userDetails.degree}
                    onChange={(e) => handleChange("degree", e.target.value)}
                  >
                    <option value="">Select Degree</option>
                    <option value="B.Sc.">B.Sc.</option>
                    <option value="M.Sc.">M.Sc.</option>
                    <option value="Ph.D.">Ph.D.</option>
                    <option value="Postdoc">Postdoc</option>
                    <option value="Faculty Member">Faculty Member</option>
                    <option value="Research Assistant">
                      Research Assistant
                    </option>
                  </select>
                </div>
                <div className="coolinput">
                  <label htmlFor="input" className="text">
                    LinkedIn:
                  </label>
                  <input
                    type="text"
                    placeholder="LinkedIn"
                    name="input"
                    className="input"
                    value={userDetails.linkedIn}
                    onChange={(e) => handleChange("linkedIn", e.target.value)}
                  />
                </div>
                <div className="coolinput">
                  <label htmlFor="input" className="text">
                    Google Scholar Profile Link:
                  </label>
                  <input
                    type="text"
                    placeholder="Google Scholar Profile Link"
                    name="input"
                    className="input"
                    value={userDetails.google_scholar}
                    onChange={(e) =>
                      handleChange("google_scholar", e.target.value)
                    }
                  />
                </div>
                <div className="notification-preference">
                  <label className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={userDetails.emailNotifications}
                      onChange={(e) =>
                        handleChange("emailNotifications", e.target.checked)
                      }
                    />
                    <span>Receive email notifications</span>
                  </label>
                  <small className="notification-hint">
                    Uncheck to unsubscribe from all email notifications
                  </small>
                </div>
              </div>
            </div>
            <div className="button-wrapper">
              <button
                className="save-changes"
                type="button"
                onClick={handleSaveChanges}
              >
                {saveButtonText}
              </button>
            </div>
          </form>
        )}

        {activeSection === "my-publications" && (
          <div id="my-publications" className="my-publications">
            <div className="publications-header">
              <h2>Publications</h2>
              <div className="toggle-container">
                <button
                  className={`toggle-btn ${
                    currentPublicationType === "manual" ? "active" : ""
                  }`}
                  onClick={() => setCurrentPublicationType("manual")}
                >
                  My Publications
                </button>
                <button
                  className={`toggle-btn ${
                    currentPublicationType === "crawled" ? "active" : ""
                  }`}
                  onClick={() => setCurrentPublicationType("crawled")}
                >
                  Crawled Publications
                </button>
              </div>
            </div>

            <div className="search-add">
              <div className="search-bar">
                <img src={searchIcon} alt="Search" className="search-icon" />
                <input
                  type="text"
                  placeholder="Search by title"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="search-input"
                />
              </div>
              {/* {currentPublicationType === "crawled" && (
                <button
                  className="force-crawl-btn"
                  onClick={console.log("hello")}
                >
                  Force Crawl Publications
                </button>
              )} */}

              {currentPublicationType === "manual" ? (
                <button
                  className="add-publication-button"
                  onClick={() => setIsAddPublicationModalOpen(true)}
                >
                  + Add Publication
                </button>
              ) : (
                selectedPublications.length > 0 && (
                  <div className="bulk-actions">
                    <button
                      className="approve-bulk-btn"
                      onClick={handleBulkApprove}
                    >
                      Approve Selected ({selectedPublications.length})
                    </button>
                    <button
                      className="reject-bulk-btn"
                      onClick={handleBulkReject}
                    >
                      Reject Selected ({selectedPublications.length})
                    </button>
                  </div>
                )
              )}
            </div>

            {currentPublicationType === "crawled" && (
              <div className="filter-status">
                <label>Filter by status:</label>
                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                >
                  <option value="all">All</option>
                  <option value="Initial pending approval">New</option>
                  <option value="pending">Pending</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
            )}

            {currentPublicationType === "manual"
              ? paginatedPublications.map((publication) => (
                  <div key={publication.paper_id} className="publication-item">
                    <form className="publication-form">
                      <strong>{publication.title}</strong>
                      <div className="pub-year">
                        {publication.publication_year}
                      </div>

                      <div className="field-group">
                        <label>GitHub:</label>
                        <input
                          type="url"
                          defaultValue={publication.git_link || ""}
                          onChange={(e) =>
                            handlePublicationLinkChange(
                              publication.paper_id,
                              "git_link",
                              e.target.value
                            )
                          }
                        />
                      </div>

                      <div className="field-group">
                        <label>Presentation:</label>
                        <input
                          type="url"
                          defaultValue={publication.presentation_link || ""}
                          onChange={(e) =>
                            handlePublicationLinkChange(
                              publication.paper_id,
                              "presentation_link",
                              e.target.value
                            )
                          }
                        />
                      </div>

                      <div className="field-group">
                        <label>Video:</label>
                        <input
                          type="url"
                          defaultValue={publication.video_link || ""}
                          onChange={(e) =>
                            handlePublicationLinkChange(
                              publication.paper_id,
                              "video_link",
                              e.target.value
                            )
                          }
                        />
                      </div>

                      <button
                        className="save-publications"
                        type="button"
                        onClick={() => handleSavePublicationLinks(publication)}
                      >
                        Save Changes
                      </button>
                    </form>
                  </div>
                ))
              : paginatedCrawledPublications.map((publication) => (
                  <div
                    key={publication.paper_id}
                    className={`publication-item crawled ${publication.status}`}
                  >
                    <div className="publication-header-account">
                      {publication.status !== "pending" &&
                        publication.status !== "Approved" && (
                          <input
                            type="checkbox"
                            checked={selectedPublications.includes(
                              publication.paper_id
                            )}
                            onChange={() =>
                              handleSelectPublication(publication.paper_id)
                            }
                            className="publication-checkbox"
                          />
                        )}

                      <div className="publication-info">
                        <strong>{publication.title}</strong>
                        <div className="pub-details">
                          <span className="pub-year">
                            {publication.publication_year}
                          </span>
                          <span
                            className={`status-badge ${publication.status
                              .toLowerCase()
                              .replace(/\s+/g, "")}`}
                          >
                            {publication.status || "pending"}
                          </span>
                        </div>
                        {/* Add link display */}
                        {publication.publication_link && (
                          <div className="publication-link">
                            <a
                              href={publication.publication_link}
                              target="_blank"
                              rel="noopener noreferrer"
                            >
                              View Publication
                            </a>
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="publication-actions">
                      {publication.status === "rejected" && (
                        <button
                          className="restore-btn"
                          // onClick={() =>
                          // }
                        >
                          Restore
                        </button>
                      )}
                    </div>
                  </div>
                ))}

            <div className="pagination_t1">
              <div className="pagination-container">
                <button
                  onClick={handlePrevPage}
                  className="pagination-buttons"
                  disabled={currentPage === 1}
                >
                  Previous
                </button>
                <span>
                  Page {currentPage} of{" "}
                  {currentPublicationType === "manual"
                    ? totalPages
                    : totalCrawledPages}
                </span>
                <button
                  onClick={handleNextPage}
                  disabled={currentPage === totalCrawledPages}
                  className="pagination-buttons"
                >
                  Next
                </button>
              </div>
            </div>

            {isAddPublicationModalOpen && (
              <div className="custom-modal-overlay">
                <div className="custom-modal">
                  <h2>Add New Publication</h2>
                  <button
                    className="close-button"
                    onClick={() => setIsAddPublicationModalOpen(false)}
                  >
                    X
                  </button>
                  <AddPublicationForm
                    onSuccess={() => {
                      setIsAddPublicationModalOpen(false);
                      // Refresh the page and navigate to my-publications
                      window.location.href =
                        window.location.pathname + "?section=my-publications";
                    }}
                  />{" "}
                </div>
              </div>
            )}
          </div>
        )}

        {activeSection === "notifications" && (
          <div id="notifications" className="notifications_section">
            <h2>Notifications</h2>
            {!notifications || notifications.length === 0 ? (
              <p>No notifications available.</p>
            ) : (
              notifications?.map((notif) => (
                <div key={notif.id} className="notifications">
                  <div className="notification_info">
                    <div className="notification_subject">{notif.subject}</div>
                    {/* <div className="notification-body">{notif.body}</div> */}
                    {renderNotification(notif.body)}
                    <div className="notification_buttons">
                      <button
                        className="notification_button"
                        onClick={() => handleRejectNotification(notif)}
                      >
                        Reject
                      </button>
                      <button
                        className="notification_button"
                        onClick={() => handleApproveNotification(notif)}
                      >
                        Approve
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
            {showApprovalModal && (
              <div className="custom-modal-overlay">
                <div className="approval-modal">
                  <button
                    className="close-button"
                    onClick={() => setShowApprovalModal(false)}
                  >
                    X
                  </button>
                  <h3>Approve Registration</h3>
                  <input
                    type="text"
                    placeholder="Full Name"
                    value={approvalForm.fullName}
                    onChange={(e) =>
                      setApprovalForm({
                        ...approvalForm,
                        fullName: e.target.value,
                      })
                    }
                  />
                  <select
                    value={approvalForm.degree}
                    onChange={(e) =>
                      setApprovalForm({
                        ...approvalForm,
                        degree: e.target.value,
                      })
                    }
                  >
                    <option value="">Select Degree</option>
                    <option value="B.Sc.">B.Sc.</option>
                    <option value="M.Sc.">M.Sc.</option>
                    <option value="Ph.D.">Ph.D.</option>
                    <option value="Postdoc">Postdoc</option>
                  </select>
                  <button
                    className="approve-button"
                    onClick={handleSubmitApproval}
                  >
                    Submit
                  </button>
                </div>
              </div>
            )}
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
        {isLoading && (
          <LoadingPopup message="Approving selected publications..." />
        )}
      </div>
    </div>
  );
};

const Sidebar = ({ activeSection, onSectionChange }) => (
  <div className="sidebar">
    <h3 className="account_sidebar">Account</h3>
    <ul>
      <li>
        <button
          className={activeSection === "personal-info" ? "active" : ""}
          onClick={() => onSectionChange("personal-info")}
        >
          Personal Info
        </button>
      </li>
      <li>
        <button
          className={activeSection === "my-publications" ? "active" : ""}
          onClick={() => onSectionChange("my-publications")}
        >
          My Publications
        </button>
      </li>
      <li>
        <button
          className={activeSection === "notifications" ? "active" : ""}
          onClick={() => onSectionChange("notifications")}
        >
          Notifications
        </button>
      </li>
    </ul>
  </div>
);

export default AccountPage;
