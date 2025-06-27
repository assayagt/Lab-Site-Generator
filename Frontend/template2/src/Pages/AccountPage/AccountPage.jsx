import React, { useState, useEffect, useContext } from "react";
import { Container, Row, Col, Card, Form, Button, Nav, Tab, Spinner, Modal, Badge } from 'react-bootstrap';
import { FaUser, FaCamera, FaSearch, FaEnvelope, FaLinkedin, FaGraduationCap, FaFileAlt } from 'react-icons/fa';
import "./AccountPage.css";
import accountIcon from "../../images/account_avatar.svg";
import cameraIcon from "../../images/camera_icon.svg";
import searchIcon from "../../images/search_icon.svg";
import AddPublicationForm from "../../Components/AddPublicationForm/AddPubliactionForm";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";

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
import ErrorPopup from "../../Components/PopUp/ErrorPopup";
import CustomToast from "../../Components/PopUp/Toast";

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
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [saveButtonText, setSaveButtonText] = useState("Save Changes");
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [selectedNotification, setSelectedNotification] = useState(null);
  const [approvalForm, setApprovalForm] = useState({
    fullName: "",
    degree: "",
  });

  const [publications, setPublications] = useState([]);
  const [uploadedPhoto, setUploadedPhoto] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;
  const [searchTerm, setSearchTerm] = useState("");
  const [isAddPublicationModalOpen, setIsAddPublicationModalOpen] = useState(false);
  const {
    notifications,
    markNotificationAsRead,
    updateNotifications,
    setHasNewNotifications,
  } = useContext(NotificationContext);

  useEffect(() => {
    const fetchUserDetails = async () => {
      try {
        const data = await getUserDetails(
          sessionStorage.getItem("domain"),
          sessionStorage.getItem("sid")
        );
        if (data) {
          setUserDetails({
            bio: data.user.bio || "",
            email: data.user.email || "",
            secondaryEmail: data.user.secondEmail || "",
            degree: data.user.degree || "",
            linkedIn: data.user.linkedin_link || "",
            fullname: data.user.fullName,
          });
        }
      } catch (error) {
        setErrorMessage("Failed to fetch user details");
        setShowError(true);
      }
    };

    const fetchPublications = async () => {
      try {
        const domain = sessionStorage.getItem("domain");
        const data = await getMemberPublications(domain);
        setPublications(data || []);
      } catch (error) {
        setErrorMessage("Failed to fetch publications");
        setShowError(true);
      }
    };

    fetchUserDetails();
    fetchPublications();
  }, []);

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

  const handleApproveNotification = async (notif) => {
    setSelectedNotification(notif);
    const sid = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    try {
      if (notif.subject === "New Registration Request Pending Approval") {
        setShowApprovalModal(true);
      } else if (notif.subject === "New Publication Pending Final Approval") {
        const response = await finalApprovePublicationByManager(sid, domain, notif.id);
        if (response?.response === "true") {
          markNotificationAsRead(notif.id);
          setShowSuccess(true);
        } else {
          setErrorMessage("Failed to approve publication");
          setShowError(true);
        }
      } else if (notif.subject === "New Publication Pending Approval") {
        const response = await initialApprovePublicationByAuthor(sid, domain, notif.id);
        if (response?.response === "true") {
          markNotificationAsRead(notif.id);
          setShowSuccess(true);
        } else {
          setErrorMessage("Failed to approve publication");
          setShowError(true);
        }
      }
    } catch (error) {
      setErrorMessage("An error occurred while processing the notification");
      setShowError(true);
    }
  };

  const handleSubmitApproval = async () => {
    try {
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
        setShowSuccess(true);
      }
    } catch (error) {
      setErrorMessage("Failed to approve registration");
      setShowError(true);
    }
  };

  const handleRejectNotification = async (notif) => {
    const sid = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    try {
      if (notif.subject === "New Registration Request Pending Approval") {
        const payload = {
          domain: domain,
          manager_userId: sid,
          notification_id: notif.id,
        };

        const response = await rejectRegistration(payload);
        if (response) {
          markNotificationAsRead(notif.id);
          setShowSuccess(true);
        }
      } else if (
        notif.subject === "New Publication Pending Final Approval" ||
        notif.subject === "New Publication Pending Approval"
      ) {
        const response = await rejectPublication(sid, domain, notif.id);
        if (response?.response === "true") {
          markNotificationAsRead(notif.id);
          setShowSuccess(true);
        }
      }
    } catch (error) {
      setErrorMessage("Failed to reject request");
      setShowError(true);
    }
  };

  const handleChange = (field, value) => {
    setUserDetails(prev => ({ ...prev, [field]: value }));
    setHasUnsavedChanges(true);
    setSaveButtonText("Save Changes");
  };

  const handleSaveChanges = async () => {
    const userId = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    try {
      await Promise.all([
        setBioByMember(userId, domain, userDetails.bio),
        setDegreeByMember(userId, domain, userDetails.degree),
        setSecondEmailByMember(userId, domain, userDetails.secondaryEmail),
        setLinkedInLinkByMember(userId, domain, userDetails.linkedIn),
      ]);

      setHasUnsavedChanges(false);
      setSaveButtonText("Saved");
      setShowSuccess(true);
    } catch (error) {
      setErrorMessage("Failed to save changes");
      setShowError(true);
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

  return (
    <Container fluid className="account-page py-5">
      <Container>
        <Row>
          <Col lg={3}>
            <Card className="sidebar-card mb-4">
              <Card.Body>
                <Nav variant="pills" className="flex-column">
                  <Nav.Item>
                    <Nav.Link
                      active={activeSection === "personal-info"}
                      onClick={() => setActiveSection("personal-info")}
                    >
                      <FaUser className="me-2" />
                      Personal Info
                    </Nav.Link>
                  </Nav.Item>
                  <Nav.Item>
                    <Nav.Link
                      active={activeSection === "publications"}
                      onClick={() => setActiveSection("publications")}
                    >
                      <FaFileAlt className="me-2" />
                      Publications
                    </Nav.Link>
                  </Nav.Item>
                  <Nav.Item>
                    <Nav.Link
                      active={activeSection === "notifications"}
                      onClick={() => setActiveSection("notifications")}
                    >
                      <FaEnvelope className="me-2" />
                      Notifications
                      {notifications?.length > 0 && (
                        <Badge bg="danger" className="ms-2">
                          {notifications.length}
                        </Badge>
                      )}
                    </Nav.Link>
                  </Nav.Item>
                </Nav>
              </Card.Body>
            </Card>
          </Col>

          <Col lg={9}>
            {activeSection === "personal-info" && (
              <Card className="content-card">
                <Card.Body>
                  <div className="text-center mb-4">
                    <div className="profile-photo-container">
                      <img
                        src={uploadedPhoto || "/default-avatar.png"}
                        alt="Profile"
                        className="profile-photo"
                      />
                      <Button
                        variant="light"
                        className="photo-upload-btn"
                        onClick={handleUploadPhoto}
                      >
                        <FaCamera />
                      </Button>
                    </div>
                  </div>

                  <Form>
                    <Form.Group className="mb-3">
                      <Form.Label>Bio</Form.Label>
                      <Form.Control
                        as="textarea"
                        rows={3}
                        value={userDetails.bio}
                        onChange={(e) => handleChange("bio", e.target.value)}
                        placeholder="Tell us about yourself"
                      />
                    </Form.Group>

                    <Form.Group className="mb-3">
                      <Form.Label>
                        <FaEnvelope className="me-2" />
                        Primary Email
                      </Form.Label>
                      <Form.Control
                        type="email"
                        value={userDetails.email}
                        disabled
                      />
                    </Form.Group>

                    <Form.Group className="mb-3">
                      <Form.Label>
                        <FaEnvelope className="me-2" />
                        Secondary Email
                      </Form.Label>
                      <Form.Control
                        type="email"
                        value={userDetails.secondaryEmail}
                        onChange={(e) => handleChange("secondaryEmail", e.target.value)}
                        placeholder="Enter secondary email"
                      />
                    </Form.Group>

                    <Form.Group className="mb-3">
                      <Form.Label>
                        <FaGraduationCap className="me-2" />
                        Degree
                      </Form.Label>
                      <Form.Control
                        type="text"
                        value={userDetails.degree}
                        onChange={(e) => handleChange("degree", e.target.value)}
                        placeholder="Enter your degree"
                      />
                    </Form.Group>

                    <Form.Group className="mb-3">
                      <Form.Label>
                        <FaLinkedin className="me-2" />
                        LinkedIn Profile
                      </Form.Label>
                      <Form.Control
                        type="url"
                        value={userDetails.linkedIn}
                        onChange={(e) => handleChange("linkedIn", e.target.value)}
                        placeholder="Enter LinkedIn profile URL"
                      />
                    </Form.Group>

                    <Button
                      variant="primary"
                      onClick={handleSaveChanges}
                      disabled={!hasUnsavedChanges}
                    >
                      {saveButtonText}
                    </Button>
                  </Form>
                </Card.Body>
              </Card>
            )}

            {activeSection === "publications" && (
              <Card className="content-card">
                <Card.Body>
                  <div className="d-flex justify-content-between align-items-center mb-4">
                    <h5 className="mb-0">My Publications</h5>
                    <Button
                      variant="primary"
                      onClick={() => setIsAddPublicationModalOpen(true)}
                    >
                      Add Publication
                    </Button>
                  </div>

                  <Form.Group className="mb-4">
                    <div className="position-relative">
                      <Form.Control
                        type="text"
                        placeholder="Search publications..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                      />
                      <FaSearch className="search-icon" />
                    </div>
                  </Form.Group>

                  {paginatedPublications.map((publication) => (
                    <Card key={publication.id} className="mb-3 publication-card">
                      <Card.Body>
                        <Card.Title>{publication.title}</Card.Title>
                        <Card.Text>{publication.description}</Card.Text>
                        <div className="d-flex gap-2">
                          <Button
                            variant="outline-primary"
                            size="sm"
                            href={publication.github_link}
                            target="_blank"
                          >
                            GitHub
                          </Button>
                          <Button
                            variant="outline-primary"
                            size="sm"
                            href={publication.presentation_link}
                            target="_blank"
                          >
                            Presentation
                          </Button>
                          <Button
                            variant="outline-primary"
                            size="sm"
                            href={publication.video_link}
                            target="_blank"
                          >
                            Video
                          </Button>
                        </div>
                      </Card.Body>
                    </Card>
                  ))}

                  {totalPages > 1 && (
                    <div className="d-flex justify-content-center mt-4">
                      <Button
                        variant="outline-primary"
                        onClick={() => setCurrentPage(currentPage - 1)}
                        disabled={currentPage === 1}
                        className="me-2"
                      >
                        Previous
                      </Button>
                      <Button
                        variant="outline-primary"
                        onClick={() => setCurrentPage(currentPage + 1)}
                        disabled={currentPage === totalPages}
                      >
                        Next
                      </Button>
                    </div>
                  )}
                </Card.Body>
              </Card>
            )}

            {activeSection === "notifications" && (
              <Card className="content-card">
                <Card.Body>
                  <h5 className="mb-4">Notifications</h5>
                  {notifications?.length > 0 ? (
                    notifications.map((notification) => (
                      <Card key={notification.id} className="mb-3 notification-card">
                        <Card.Body>
                          <div className="d-flex justify-content-between align-items-start">
                            <div>
                              <Card.Title>{notification.subject}</Card.Title>
                              <Card.Text>{notification.body}</Card.Text>
                            </div>
                            <div className="d-flex gap-2">
                              <Button
                                variant="success"
                                size="sm"
                                onClick={() => handleApproveNotification(notification)}
                              >
                                Approve
                              </Button>
                              <Button
                                variant="danger"
                                size="sm"
                                onClick={() => handleRejectNotification(notification)}
                              >
                                Reject
                              </Button>
                            </div>
                          </div>
                        </Card.Body>
                      </Card>
                    ))
                  ) : (
                    <p className="text-center text-muted">No notifications</p>
                  )}
                </Card.Body>
              </Card>
            )}
          </Col>
        </Row>
      </Container>

      {/* Approval Modal */}
      <Modal show={showApprovalModal} onHide={() => setShowApprovalModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Approve Registration</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Full Name</Form.Label>
              <Form.Control
                type="text"
                value={approvalForm.fullName}
                onChange={(e) =>
                  setApprovalForm({ ...approvalForm, fullName: e.target.value })
                }
                placeholder="Enter full name"
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Degree</Form.Label>
              <Form.Control
                type="text"
                value={approvalForm.degree}
                onChange={(e) =>
                  setApprovalForm({ ...approvalForm, degree: e.target.value })
                }
                placeholder="Enter degree"
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowApprovalModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleSubmitApproval}>
            Approve
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Toast Notifications */}
      <CustomToast
        show={showSuccess}
        onClose={() => setShowSuccess(false)}
        message="Operation completed successfully!"
        type="success"
      />
      <CustomToast
        show={showError}
        onClose={() => setShowError(false)}
        message={errorMessage}
        type="error"
      />
    </Container>
  );
};

export default AccountPage;
