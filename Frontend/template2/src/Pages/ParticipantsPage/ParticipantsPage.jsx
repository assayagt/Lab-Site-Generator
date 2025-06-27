import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card, Button, Form, Modal, Spinner, Badge } from 'react-bootstrap';
import { FaLinkedin, FaEnvelope } from "react-icons/fa";
import {
  getAllAlumni,
  getAllLabManagers,
  getAllLabMembers,
  addLabMemberFromWebsite,
  createNewSiteManagerFromLabWebsite,
  addAlumniFromLabWebsite,
  removeManagerPermission,
} from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import CustomToast from "../../Components/PopUp/Toast";
import "./ParticipantsPage.css";

const ParticipantsPage = () => {
  const [selectedDegree, setSelectedDegree] = useState("All");
  const [participants, setParticipants] = useState([]);
  const [alumni, setAlumni] = useState([]);
  const [loading, setLoading] = useState(true);
  const { editMode } = useEditMode();
  const [showAddForm, setShowAddForm] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [newParticipant, setNewParticipant] = useState({
    fullName: "",
    email: "",
    degree: "",
    isManager: false,
    isAlumni: false,
  });

  const degreeOrder = {
    "Ph.D.": 1,
    "M.Sc.": 2,
    "D.Sc.": 3,
    "B.Sc.": 4,
    "Faculty Member": 5,
  };

  const degreeOptions = [
    "Ph.D.",
    "M.Sc.",
    "B.Sc.",
    "D.Sc.",
    "Faculty Member",
    "Alumni",
  ];

  const fetchParticipants = async () => {
    setLoading(true);
    try {
      const domain = sessionStorage.getItem("domain");

      const [managers, members, alumniData] = await Promise.all([
        getAllLabManagers(domain),
        getAllLabMembers(domain),
        getAllAlumni(domain),
      ]);

      const taggedManagers = managers.map((m) => ({
        ...m,
        isManager: true,
        isAlumni: false,
      }));
      const taggedMembers = members.map((m) => ({
        ...m,
        isManager: false,
        isAlumni: false,
      }));

      setParticipants([...taggedManagers, ...taggedMembers]);

      const taggedAlumni = (alumniData || []).map((a) => ({
        ...a,
        isAlumni: true,
        isManager: false,
      }));
      setAlumni(taggedAlumni);
    } catch (err) {
      console.error("Error fetching participants:", err);
      setErrorMessage("Error fetching participants");
      setShowError(true);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchParticipants();
  }, []);

  const handleToggleManager = async (member) => {
    const userId = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    try {
      if (!member.isManager) {
        const response = await createNewSiteManagerFromLabWebsite(
          userId,
          member.email,
          domain
        );
        if (response?.response === "true") {
          setParticipants((prev) =>
            prev.map((p) =>
              p.email === member.email ? { ...p, isManager: !p.isManager } : p
            )
          );
          setShowSuccess(true);
        } else {
          setErrorMessage("Failed to promote to manager: " + response?.message);
          setShowError(true);
        }
      } else {
        const response = await removeManagerPermission(
          userId,
          member.email,
          domain
        );
        if (response?.manager_email) {
          setParticipants((prev) =>
            prev.map((p) =>
              p.email === member.email ? { ...p, isManager: !p.isManager } : p
            )
          );
          setShowSuccess(true);
        } else {
          setErrorMessage("Failed to remove manager permission: " + response?.message);
          setShowError(true);
        }
      }
    } catch (err) {
      setErrorMessage("Error toggling manager: " + err);
      setShowError(true);
    }
  };

  const handleToggleAlumni = async (member) => {
    const userId = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    try {
      if (!member.isAlumni) {
        const response = await addAlumniFromLabWebsite(
          userId,
          member.email,
          domain
        );
        if (response?.response === "true") {
          setParticipants((prev) => prev.filter((p) => p.email !== member.email));
          setAlumni((prev) => [
            ...prev,
            { ...member, isAlumni: true, isManager: false },
          ]);
          setShowSuccess(true);
        } else {
          setErrorMessage("Failed to promote to alumni: " + response?.message);
          setShowError(true);
        }
      }
    } catch (err) {
      setErrorMessage("Error toggling alumni: " + err);
      setShowError(true);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewParticipant((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleAddParticipant = async () => {
    const userId = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");

    try {
      const response = await addLabMemberFromWebsite(
        userId,
        newParticipant.email,
        newParticipant.fullName,
        newParticipant.degree,
        domain
      );

      if (response?.response === "true") {
        setShowAddForm(false);
        setNewParticipant({
          fullName: "",
          email: "",
          degree: "",
          isManager: false,
          isAlumni: false,
        });
        fetchParticipants();
        setShowSuccess(true);
      } else {
        setErrorMessage("Failed to add participant: " + response?.message);
        setShowError(true);
      }
    } catch (err) {
      setErrorMessage("Error adding participant: " + err);
      setShowError(true);
    }
  };

  const filteredParticipants = selectedDegree === "All"
    ? participants
    : participants.filter((p) => p.degree === selectedDegree);

  const sortedParticipants = [...filteredParticipants].sort((a, b) => {
    const degreeA = degreeOrder[a.degree] || 999;
    const degreeB = degreeOrder[b.degree] || 999;
    return degreeA - degreeB;
  });

  return (
    <Container fluid className="participants-page py-5">
      <Container>
        {/* Header Section */}
        <Row className="mb-4 align-items-center">
          <Col>
            <h1 className="page-title">
              Lab Members
              {editMode && (
                <Button
                  variant="primary"
                  size="sm"
                  className="ms-3"
                  onClick={() => setShowAddForm(true)}
                >
                  Add Member
                </Button>
              )}
            </h1>
          </Col>
        </Row>

        {/* Filter Section */}
        <Row className="mb-4">
          <Col md={6} lg={3}>
            <Form.Group>
              <Form.Label>Filter by Degree</Form.Label>
              <Form.Select
                value={selectedDegree}
                onChange={(e) => setSelectedDegree(e.target.value)}
              >
                <option value="All">All Degrees</option>
                {degreeOptions.map((degree) => (
                  <option key={degree} value={degree}>
                    {degree}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>
        </Row>

        {/* Participants List */}
        {loading ? (
          <div className="text-center py-5">
            <Spinner animation="border" variant="primary" />
          </div>
        ) : (
          <Row className="g-4">
            {sortedParticipants.map((participant) => (
              <Col key={participant.email} xs={12} md={6} lg={4}>
                <Card className="participant-card h-100">
                  <Card.Body>
                    <Card.Title className="d-flex justify-content-between align-items-start">
                      <span>{participant.fullName}</span>
                      {participant.isManager && (
                        <Badge bg="primary">Manager</Badge>
                      )}
                    </Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">
                      {participant.degree}
                    </Card.Subtitle>
                    <div className="d-flex gap-2 mb-3">
                      <Button
                        variant="outline-primary"
                        size="sm"
                        href={`mailto:${participant.email}`}
                      >
                        <FaEnvelope className="me-1" />
                        Email
                      </Button>
                      {participant.linkedin && (
                        <Button
                          variant="outline-primary"
                          size="sm"
                          href={participant.linkedin}
                          target="_blank"
                          rel="noopener noreferrer"
                        >
                          <FaLinkedin className="me-1" />
                          LinkedIn
                        </Button>
                      )}
                    </div>
                    {editMode && (
                      <div className="mt-3">
                        <Form.Check
                          type="checkbox"
                          id={`manager-${participant.email}`}
                          label="Manager"
                          checked={participant.isManager}
                          onChange={() => handleToggleManager(participant)}
                          className="mb-2"
                        />
                        <Form.Check
                          type="checkbox"
                          id={`alumni-${participant.email}`}
                          label="Alumni"
                          checked={participant.isAlumni}
                          onChange={() => handleToggleAlumni(participant)}
                        />
                      </div>
                    )}
                  </Card.Body>
                </Card>
              </Col>
            ))}
          </Row>
        )}

        {/* Add Participant Modal */}
        <Modal show={showAddForm} onHide={() => setShowAddForm(false)}>
          <Modal.Header closeButton>
            <Modal.Title>Add New Member</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Form.Group className="mb-3">
                <Form.Label>Full Name</Form.Label>
                <Form.Control
                  type="text"
                  name="fullName"
                  value={newParticipant.fullName}
                  onChange={handleInputChange}
                  placeholder="Enter full name"
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control
                  type="email"
                  name="email"
                  value={newParticipant.email}
                  onChange={handleInputChange}
                  placeholder="Enter email"
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Degree</Form.Label>
                <Form.Select
                  name="degree"
                  value={newParticipant.degree}
                  onChange={handleInputChange}
                >
                  <option value="">Select degree</option>
                  {degreeOptions.map((degree) => (
                    <option key={degree} value={degree}>
                      {degree}
                    </option>
                  ))}
                </Form.Select>
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowAddForm(false)}>
              Cancel
            </Button>
            <Button variant="primary" onClick={handleAddParticipant}>
              Add Member
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
    </Container>
  );
};

export default ParticipantsPage;
