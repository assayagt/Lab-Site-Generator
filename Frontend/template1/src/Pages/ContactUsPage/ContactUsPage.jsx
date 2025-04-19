import React, { useState, useEffect } from "react";
import "./ContactUsPage.css";
import {
  getContactUs,
  setSiteContactInfoByManager,
} from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";
import ErrorPopup from "../../Components/PopUp/ErrorPopup";

function ContactUsPage() {
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
  const [popupMessage, setPopupMessage] = useState("");
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

  useEffect(() => {
    if (popupMessage || errorMessage) {
      const timer = setTimeout(() => {
        setPopupMessage("");
        setErrorMessage("");
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [popupMessage, errorMessage]);

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
        setPopupMessage("Changes saved successfully!");
        setSaveButtonText("Saved");
        setHasUnsavedChanges(false);
      } else {
        setErrorMessage("An error occurred while saving.");
      }
    } catch (error) {
      setErrorMessage("An error occurred while saving.");
    } finally {
      setIsSaving(false);
    }
  };

  const handleChange = (setter) => (e) => {
    setter(e.target.value);
    setHasUnsavedChanges(true);
    setSaveButtonText("Save");
  };

  const mapLink = coordinates
    ? `https://www.openstreetmap.org/?mlat=${coordinates.lat}&mlon=${coordinates.lon}&zoom=15`
    : "#";

  if (loading) return <div className="loading">Loading contact details...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="contact_page">
      <div className="page_title">Contact Us</div>
      <div className="contact_info">
        <div>
          <strong>Address:</strong>{" "}
          {editMode ? (
            <input
              type="text"
              value={address}
              onChange={handleChange(setAddress)}
              className="contact_input"
            />
          ) : (
            address
          )}
        </div>
        <div>
          <strong>Email:</strong>{" "}
          {editMode ? (
            <input
              type="email"
              value={email}
              onChange={handleChange(setEmail)}
              className="contact_input"
            />
          ) : (
            email && (
              <a href={`mailto:${email}`} className="email-link">
                {email}
              </a>
            )
          )}
        </div>
        <div>
          <strong>Phone:</strong>{" "}
          {editMode ? (
            <input
              type="text"
              value={phoneNum}
              onChange={handleChange(setPhoneNum)}
              className="contact_input"
            />
          ) : (
            phoneNum
          )}
        </div>
        {editMode && (
          <div className="button_container">
            <button
              type="button"
              className="saveButton_contact"
              onClick={handleSave}
              disabled={isSaving || !hasUnsavedChanges}
            >
              {saveButtonText}
            </button>
          </div>
        )}
        <div className="map_container">
          {coordinates ? (
            <iframe
              title="OpenStreetMap"
              src={`https://www.openstreetmap.org/export/embed.html?bbox=${coordinates.lon},${coordinates.lat},${coordinates.lon},${coordinates.lat}&marker=${coordinates.lat},${coordinates.lon}&layers=mapnik`}
              style={{
                width: "400px",
                height: "250px",
                border: "0",
                borderRadius: "8px",
              }}
              allowFullScreen
            ></iframe>
          ) : (
            <p>Loading map...</p>
          )}
        </div>
      </div>
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
}

export default ContactUsPage;
