import React, { useState, useContext, useEffect } from "react";
import { Card, Form, Button, Alert } from 'react-bootstrap';
import "./AboutUs.css";
import { useEditMode } from "../../Context/EditModeContext";
import { setSiteAboutUsByManager } from "../../services/websiteService";

function AboutUs(props) {
  const { editMode } = useEditMode();
  const [aboutUsText, setAboutUsText] = useState(props.info || "");
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [saveButtonText, setSaveButtonText] = useState("Save");
  const [showSuccess, setShowSuccess] = useState(false);
  const [showError, setShowError] = useState(false);

  useEffect(() => {
    if (showSuccess || showError) {
      const timer = setTimeout(() => {
        setShowSuccess(false);
        setShowError(false);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [showSuccess, showError]);

  const handleSave = async () => {
    const userId = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");
    const response = await setSiteAboutUsByManager(userId, domain, aboutUsText);
    if (response?.response === "true") {
      setShowSuccess(true);
      setSaveButtonText("Saved");
      setHasUnsavedChanges(false);
    } else {
      setShowError(true);
    }
  };

  const handleChange = (e) => {
    setAboutUsText(e.target.value);
    setHasUnsavedChanges(true);
    setSaveButtonText("Save");
  };

  return (
    <Card className="about-us-card">
      <Card.Body>
        <Card.Title className="mb-4">About Us</Card.Title>
        
        {editMode ? (
          <div className="edit-mode-container">
            <Form.Control
              as="textarea"
              value={aboutUsText}
              onChange={handleChange}
              className="mb-3"
              rows={8}
            />
            <Button
              variant="outline-primary"
              onClick={handleSave}
              disabled={!hasUnsavedChanges}
              className="save-button"
            >
              {saveButtonText}
            </Button>
          </div>
        ) : (
          <div className="about-us-content">
            {aboutUsText}
          </div>
        )}

        <Alert 
          show={showSuccess} 
          variant="success" 
          className="position-fixed top-0 end-0 m-3"
          onClose={() => setShowSuccess(false)}
          dismissible
        >
          Changes saved successfully!
        </Alert>

        <Alert 
          show={showError} 
          variant="danger" 
          className="position-fixed top-0 end-0 m-3"
          onClose={() => setShowError(false)}
          dismissible
        >
          An error occurred while saving.
        </Alert>
      </Card.Body>
    </Card>
  );
}

export default AboutUs;
