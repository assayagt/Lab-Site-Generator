import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card, Form, Button, Spinner } from 'react-bootstrap';
import { FaMapMarkerAlt, FaEnvelope, FaPhone } from 'react-icons/fa';
import {
  getContactUs,
  setSiteContactInfoByManager,
} from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import CustomToast from "../../Components/PopUp/Toast";
import "./ContactUsPage.css";

const ContactUsPage = () => {
  const [coordinates, setCoordinates] = useState(null);
  const [address, setAddress] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNum, setPhoneNum] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { editMode } = useEditMode();
  const [isSaving, setIsSaving] = useState(false);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [saveButtonText, setSaveButtonText] = useState("Save");
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const domain = sessionStorage.getItem("domain");

  useEffect(() => {
    const fetchContactDetails = async () => {
      try {
        const data = await getContactUs(domain);
        if (data.response === "true") {
          setAddress(data.data.address || "");
          setEmail(data.data.email || "");
          setPhoneNum(data.data.phone_num || "");
          setError(null);
        }
      } catch (err) {
        console.error("Error fetching contact details:", err);
        setError("Failed to load contact details.");
        setShowError(true);
      } finally {
        setLoading(false);
      }
    };
    fetchContactDetails();
  }, [domain]);

  useEffect(() => {
    const fetchCoordinates = async () => {
      if (!address) return;
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
            address
          )}&format=json`
        );
        const data = await response.json();
        if (data.length > 0) {
          setCoordinates({ lat: data[0].lat, lon: data[0].lon });
        }
      } catch (error) {
        console.error("Error fetching coordinates:", error);
      }
    };
    fetchCoordinates();
  }, [address]);

  const handleSave = async () => {
    setIsSaving(true);
    const userId = sessionStorage.getItem("sid");
    try {
      const response = await setSiteContactInfoByManager(
        userId,
        domain,
        address,
        email,
        phoneNum
      );
      if (response?.response === "true") {
        setShowSuccess(true);
        setSaveButtonText("Saved");
        setHasUnsavedChanges(false);
      } else {
        setErrorMessage("An error occurred while saving.");
        setShowError(true);
      }
    } catch (error) {
      setErrorMessage("An error occurred while saving.");
      setShowError(true);
    } finally {
      setIsSaving(false);
    }
  };

  const handleChange = (setter) => (e) => {
    setter(e.target.value);
    setHasUnsavedChanges(true);
    setSaveButtonText("Save");
  };

  if (loading) {
    return (
      <div className="text-center py-5">
        <Spinner animation="border" variant="primary" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-5 text-danger">
        {error}
      </div>
    );
  }

  return (
    <Container fluid className="contact-page py-5">
      <Container>
        <Row className="mb-4">
          <Col>
            <h1 className="page-title">Contact Us</h1>
          </Col>
        </Row>

        <Row className="g-4">
          {/* Contact Information */}
          <Col lg={6}>
            <Card className="contact-card h-100">
              <Card.Body>
                <div className="contact-info">
                  <div className="mb-4">
                    <h5 className="d-flex align-items-center mb-3">
                      <FaMapMarkerAlt className="me-2" />
                      Address
                    </h5>
                    {editMode ? (
                      <Form.Control
                        type="text"
                        value={address}
                        onChange={handleChange(setAddress)}
                        placeholder="Enter address"
                      />
                    ) : (
                      <p className="mb-0">{address}</p>
                    )}
                  </div>

                  <div className="mb-4">
                    <h5 className="d-flex align-items-center mb-3">
                      <FaEnvelope className="me-2" />
                      Email
                    </h5>
                    {editMode ? (
                      <Form.Control
                        type="email"
                        value={email}
                        onChange={handleChange(setEmail)}
                        placeholder="Enter email"
                      />
                    ) : (
                      email && (
                        <a href={`mailto:${email}`} className="text-decoration-none">
                          {email}
                        </a>
                      )
                    )}
                  </div>

                  <div className="mb-4">
                    <h5 className="d-flex align-items-center mb-3">
                      <FaPhone className="me-2" />
                      Phone
                    </h5>
                    {editMode ? (
                      <Form.Control
                        type="text"
                        value={phoneNum}
                        onChange={handleChange(setPhoneNum)}
                        placeholder="Enter phone number"
                      />
                    ) : (
                      <p className="mb-0">{phoneNum}</p>
                    )}
                  </div>

                  {editMode && (
                    <div className="mt-4">
                      <Button
                        variant="primary"
                        onClick={handleSave}
                        disabled={isSaving || !hasUnsavedChanges}
                      >
                        {isSaving ? (
                          <>
                            <Spinner
                              as="span"
                              animation="border"
                              size="sm"
                              role="status"
                              aria-hidden="true"
                              className="me-2"
                            />
                            Saving...
                          </>
                        ) : (
                          saveButtonText
                        )}
                      </Button>
                    </div>
                  )}
                </div>
              </Card.Body>
            </Card>
          </Col>

          {/* Map */}
          <Col lg={6}>
            <Card className="map-card h-100">
              <Card.Body>
                <h5 className="mb-3">Location</h5>
                {coordinates ? (
                  <iframe
                    title="OpenStreetMap"
                    src={`https://www.openstreetmap.org/export/embed.html?bbox=${coordinates.lon},${coordinates.lat},${coordinates.lon},${coordinates.lat}&marker=${coordinates.lat},${coordinates.lon}&layers=mapnik`}
                    className="map-iframe"
                    allowFullScreen
                  />
                ) : (
                  <div className="text-center py-5">
                    <Spinner animation="border" variant="primary" />
                    <p className="mt-2 mb-0">Loading map...</p>
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>

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
        message={errorMessage}
        type="error"
      />
    </Container>
  );
};

export default ContactUsPage;
