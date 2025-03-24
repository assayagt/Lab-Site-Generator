import React, { useState, useEffect, useContext } from "react";
import "./AccountPage.css";
import accountIcon from "../../images/account_avatar.svg";
import cameraIcon from "../../images/camera_icon.svg";
import searchIcon from "../../images/search_icon.svg";
import AddPublicationForm from "../../Components/AddPublicationForm/AddPubliactionForm";
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
} from "../../services/websiteService";
import { fetchUserNotifications } from "../../services/UserService";
import { NotificationContext } from "../../Context/NotificationContext";

const AccountPage = () => {
  const [activeSection, setActiveSection] = useState("personal-info");
  const [userDetails, setUserDetails] = useState({
    bio: "",
    email: "",
    secondaryEmail: "",
    degree: "",
    linkedIn: "",
    fullname: "",
  });
  const [showApprovalModal, setShowApprovalModal] = useState(false);

  const [selectedNotification, setSelectedNotification] = useState(null);
  const [approvalForm, setApprovalForm] = useState({
    fullName: "",
    degree: "",
  });

  const [publications, setPublications] = useState([]);
  const [uploadedPhoto, setUploadedPhoto] = useState(accountIcon);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;
  const [searchTerm, setSearchTerm] = useState("");
  const [isAddPublicationModalOpen, setIsAddPublicationModalOpen] =
    useState(false);
  const {
    notifications,
    hasNewNotifications,
    markNotificationAsRead,
    updateNotifications,
  } = useContext(NotificationContext); // Get notifications

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
          linkedIn: data.user.linkedIn || "",
          fullname: data.user.fullName,
        });
      }
    };

    const fetchPublications = async () => {
      const domain = sessionStorage.getItem("domain");
      const data = await getMemberPublications(domain);
      console.log("Fetched Publications:", data); // Debugging log
      setPublications(data || []);
    };
    fetchUserDetails();
    fetchPublications();
  }, []);

  const handleSectionChange = (section) => {
    setActiveSection(section);
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

  const handleSavePhoto = () => {
    alert("Photo saved successfully!");
  };

  const handleApproveNotification = async (notif) => {
    setSelectedNotification(notif);
    setShowApprovalModal(true);
  };

  const handleSubmitApproval = async () => {
    const payload = {
      domain: sessionStorage.getItem("domain"),
      manager_userId: sessionStorage.getItem("sid"),
      requested_email: selectedNotification.id,
      requested_full_name: approvalForm.fullName,
      requested_degree: approvalForm.degree,
    };

    const response = await approveRegistration(payload);
    if (response) {
      markNotificationAsRead(selectedNotification.id);
      setShowApprovalModal(false);
      setApprovalForm({ fullName: "", degree: "" });
      setSelectedNotification(null);
    } else {
      alert("Approval failed.");
    }
  };

  const handleRejectNotification = async (notifId) => {
    const payload = {
      domain: sessionStorage.getItem("domain"),
      manager_userId: sessionStorage.getItem("sid"),
      requested_email: notifId,
    };

    const response = await rejectRegistration(payload);
    if (response) {
      markNotificationAsRead(notifId);
    } else {
      alert("Rejection failed.");
    }
  };

  const filteredPublications = publications.filter((pub) =>
    pub.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const totalPages = Math.ceil(filteredPublications.length / itemsPerPage);
  const paginatedPublications = filteredPublications.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

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

  const handleSavePublicationLinks = async (publication) => {
    try {
      let isUpdated = false; // Track if any field was successfully updated
      const sid = sessionStorage.getItem("sid");
      const domain = sessionStorage.getItem("domain");
      if (publication.github) {
        const githubResponse = await setPublicationGitLink(
          sid,
          domain,
          publication.id,
          publication.github
        );
        if (githubResponse === "true") {
          isUpdated = true;
        } else {
          throw new Error(
            `Failed to update GitHub link: ${githubResponse.statusText}`
          );
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
        } else {
          throw new Error(
            `Failed to update Presentation link: ${presentationResponse.statusText}`
          );
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
        } else {
          throw new Error(
            `Failed to update Video link: ${videoResponse.statusText}`
          );
        }
      }

      if (isUpdated) {
        alert("Links updated successfully!");
      } else {
        alert("No changes were made.");
      }
    } catch (error) {
      console.error("Error updating publication links:", error);
      alert(`An error occurred: ${error.message}`);
    }
  };

  const handleSaveChanges = async () => {
    try {
      const sid = sessionStorage.getItem("sid");
      const domain = sessionStorage.getItem("domain");
      // Track if any update was successful
      let isUpdated = false;

      if (userDetails.bio) {
        await setBioByMember(sid, userDetails.bio, domain);
        isUpdated = true;
      }

      if (userDetails.secondaryEmail) {
        await setSecondEmailByMember(sid, userDetails.secondaryEmail, domain);
        isUpdated = true;
      }

      if (userDetails.degree) {
        await setDegreeByMember(sid, userDetails.degree, domain);
        isUpdated = true;
      }

      if (userDetails.linkedIn) {
        await setLinkedInLinkByMember(sid, userDetails.linkedIn, domain);
        isUpdated = true;
      }

      if (isUpdated) {
        alert("Changes saved successfully!");
      } else {
        alert("No changes were made.");
      }
    } catch (error) {
      console.error("Error saving changes:", error);
      alert(`An error occurred: ${error.message}`);
    }
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
                <button className="save-photo" onClick={handleSavePhoto}>
                  Save Photo
                </button>
              </div>
              <div className="details">
                <label className="detail-bio">
                  <div className="text-detail">{userDetails.email}</div>
                </label>
                <div className="coolinput">
                  <label htmlFor="input" className="text">
                    Bio:
                  </label>
                  <input
                    type="text"
                    placeholder="Bio"
                    name="input"
                    className="input"
                    value={userDetails.bio}
                    onChange={(e) =>
                      setUserDetails({ ...userDetails, bio: e.target.value })
                    }
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
                      setUserDetails({
                        ...userDetails,
                        secondaryEmail: e.target.value,
                      })
                    }
                  />
                </div>
                <div className="coolinput">
                  <label htmlFor="input" className="text">
                    Degree:
                  </label>
                  <input
                    type="text"
                    placeholder="Degree"
                    name="input"
                    className="input"
                    value={userDetails.degree}
                    onChange={(e) =>
                      setUserDetails({ ...userDetails, degree: e.target.value })
                    }
                  />
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
                    onChange={(e) =>
                      setUserDetails({
                        ...userDetails,
                        linkedIn: e.target.value,
                      })
                    }
                  />
                </div>
              </div>
            </div>
            <div className="button-wrapper">
              <button
                className="save-changes"
                type="button"
                onClick={handleSaveChanges}
              >
                Save Changes
              </button>
            </div>
          </form>
        )}

        {activeSection === "my-publications" && (
          <div id="my-publications" className="my-publications">
            <h2>My Publications</h2>

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
              <button
                className="add-publication-button"
                onClick={() => setIsAddPublicationModalOpen(true)}
              >
                + Add Publication
              </button>
            </div>
            {paginatedPublications.map((publication) => (
              <div key={publication.id} className="publication-item">
                <form className="publication-form">
                  <strong>{publication.title}</strong>
                  <div>{publication.publication_year}</div>
                  <label className="detail-bio">
                    <strong>GitHub:</strong>
                    <input
                      className="text-detail"
                      type="url"
                      defaultValue={publication.github || ""}
                    />
                  </label>
                  <label className="detail-bio">
                    <strong>Presentation:</strong>
                    <input
                      className="text-detail"
                      type="url"
                      defaultValue={publication.presentation || ""}
                    />
                  </label>
                  <label className="detail-bio">
                    <strong>Video:</strong>
                    <input
                      className="text-detail"
                      type="url"
                      defaultValue={publication.video || ""}
                    />
                  </label>
                  <button
                    className="save-publications"
                    type="button"
                    onClick={() => handleSavePublicationLinks(publication)}
                  >
                    Save Changes
                  </button>
                </form>
              </div>
            ))}
            <div className="pagination">
              <button
                onClick={handlePrevPage}
                className="pagination-buttons"
                disabled={currentPage === 1}
              >
                Previous
              </button>
              <span>
                Page {currentPage} of {totalPages}
              </span>
              <button
                onClick={handleNextPage}
                disabled={currentPage === totalPages}
                className="pagination-buttons"
              >
                Next
              </button>
            </div>

            {isAddPublicationModalOpen && (
              <div className="custom-modal-overlay">
                <div className="custom-modal">
                  <button
                    className="close-button"
                    onClick={() => setIsAddPublicationModalOpen(false)}
                  >
                    X
                  </button>
                  <AddPublicationForm
                    onSuccess={() => setIsAddPublicationModalOpen(false)}
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
                    <div>{notif.body}</div>
                    <div className="notification_buttons">
                      <button
                        className="notification_button"
                        onClick={() => handleRejectNotification(notif.id)}
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
