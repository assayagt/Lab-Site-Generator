import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card, Button, Form, Pagination, Modal } from 'react-bootstrap';
import { getApprovedPublications, setPublicationGitLink, setPublicationPttxLink, setPublicationVideoLink } from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import AddPublicationForm from "../../Components/AddPublicationForm/AddPublicationForm";
import CustomToast from "../../Components/PopUp/Toast";
import "./PublicationsPage.css";

const PublicationsPage = () => {
  const [publications, setPublications] = useState([]);
  const [yearFilter, setYearFilter] = useState("");
  const [authorFilter, setAuthorFilter] = useState("");
  const [availableYears, setAvailableYears] = useState([]);
  const [availableAuthors, setAvailableAuthors] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editedLinks, setEditedLinks] = useState({});
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const [saveStatus, setSaveStatus] = useState({});
  const { editMode } = useEditMode();
  const itemsPerPage = 5;

  useEffect(() => {
    fetchPublications();
  }, []);

  const fetchPublications = async () => {
    try {
      const domain = sessionStorage.getItem("domain");
      const fetchedPublications = await getApprovedPublications(domain);
      setPublications(fetchedPublications || []);
    } catch (error) {
      console.error("Error fetching publications:", error);
    }
  };

  useEffect(() => {
    const years = Array.from(
      new Set(
        publications.map((pub) => {
          const date = new Date(pub.publication_year);
          return isNaN(date.getFullYear()) ? pub.publication_year : date.getFullYear();
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
      const publicationYear = isNaN(new Date(pub.publication_year).getFullYear())
        ? pub.publication_year
        : new Date(pub.publication_year).getFullYear();
      const matchesYear = yearFilter ? publicationYear === parseInt(yearFilter, 10) : true;

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
        setShowSuccess(true);
        setSaveStatus((prev) => ({ ...prev, [paperId]: "Saved" }));
      } else {
        setShowError(true);
      }
    } catch (error) {
      console.error("Error updating publication links:", error);
      setShowError(true);
    }
  };

  return (
    <Container fluid className="publications-page py-5">
      <Container>
        {/* Header Section */}
        <Row className="mb-4 align-items-center">
          <Col>
            <h1 className="page-title">
              Publications
              {editMode && (
                <Button
                  variant="primary"
                  size="sm"
                  className="ms-3"
                  onClick={() => setShowAddForm(true)}
                >
                  Add Publication
                </Button>
              )}
            </h1>
          </Col>
        </Row>

        {/* Filters Section */}
        <Row className="mb-4">
          <Col md={6} lg={3} className="mb-3">
            <Form.Group>
              <Form.Label>Filter by Year</Form.Label>
              <Form.Select
                value={yearFilter}
                onChange={handleYearChange}
              >
                <option value="">All Years</option>
                {availableYears.map((year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>
          <Col md={6} lg={3} className="mb-3">
            <Form.Group>
              <Form.Label>Filter by Author</Form.Label>
              <Form.Select
                value={authorFilter}
                onChange={handleAuthorChange}
              >
                <option value="">All Authors</option>
                {availableAuthors.map((author) => (
                  <option key={author} value={author}>
                    {author}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>
        </Row>

        {/* Publications List */}
        <Row className="g-4">
          {paginatedPublications.map((pub) => (
            <Col key={pub.id} xs={12}>
              <Card className="publication-card h-100">
                <Card.Body>
                  <Card.Title>{pub.title}</Card.Title>
                  <Card.Subtitle className="mb-2 text-muted">
                    {pub.authors?.join(", ")}
                  </Card.Subtitle>
                  <Card.Text>
                    <strong>Year:</strong> {new Date(pub.publication_year).getFullYear()}
                  </Card.Text>
                  
                  {editMode && (
                    <div className="mt-3">
                      <Form.Group className="mb-2">
                        <Form.Label>GitHub Link</Form.Label>
                        <Form.Control
                          type="text"
                          value={editedLinks[pub.id]?.git_link || pub.git_link || ""}
                          onChange={(e) => handleInputChange(pub.id, "git_link", e.target.value)}
                        />
                      </Form.Group>
                      <Form.Group className="mb-2">
                        <Form.Label>Presentation Link</Form.Label>
                        <Form.Control
                          type="text"
                          value={editedLinks[pub.id]?.presentation_link || pub.presentation_link || ""}
                          onChange={(e) => handleInputChange(pub.id, "presentation_link", e.target.value)}
                        />
                      </Form.Group>
                      <Form.Group className="mb-3">
                        <Form.Label>Video Link</Form.Label>
                        <Form.Control
                          type="text"
                          value={editedLinks[pub.id]?.video || pub.video || ""}
                          onChange={(e) => handleInputChange(pub.id, "video", e.target.value)}
                        />
                      </Form.Group>
                      <Button
                        variant="outline-primary"
                        onClick={() => handleSavePublicationLinks(pub.id)}
                        disabled={saveStatus[pub.id] === "Saved"}
                      >
                        {saveStatus[pub.id] || "Save"}
                      </Button>
                    </div>
                  )}
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>

        {/* Pagination */}
        {totalPages > 1 && (
          <Row className="mt-4">
            <Col className="d-flex justify-content-center">
              <Pagination>
                <Pagination.Prev
                  onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                />
                {[...Array(totalPages)].map((_, index) => (
                  <Pagination.Item
                    key={index + 1}
                    active={currentPage === index + 1}
                    onClick={() => setCurrentPage(index + 1)}
                  >
                    {index + 1}
                  </Pagination.Item>
                ))}
                <Pagination.Next
                  onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                />
              </Pagination>
            </Col>
          </Row>
        )}
      </Container>

      {/* Add Publication Modal */}
      <Modal show={showAddForm} onHide={() => setShowAddForm(false)} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Add New Publication</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <AddPublicationForm onSuccess={() => {
            setShowAddForm(false);
            fetchPublications();
          }} />
        </Modal.Body>
      </Modal>

      {/* Toast Notifications */}
      <CustomToast
        show={showSuccess}
        onClose={() => setShowSuccess(false)}
        message="Changes saved successfully!"
        type="success"
      />
      <CustomToast
        show={showError}
        onClose={() => setShowError(false)}
        message="An error occurred while saving."
        type="error"
      />
    </Container>
  );
};

export default PublicationsPage;
