import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./ContactUsPage2.css";
import {
  getContactUs,
  setSiteContactInfoByManager,
} from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";
import ErrorPopup from "../../Components/PopUp/ErrorPopup";
import { useWebsite } from "../../Context/WebsiteContext";

// Fix marker icon issue
L.Marker.prototype.options.icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function ContactUsPage() {
  const { websiteData, setWebsite } = useWebsite();
  const [address, setAddress] = useState(websiteData.contact_us?.address || "");
  const [email, setEmail] = useState(websiteData.contact_us?.email || "");
  const [phoneNum, setPhoneNum] = useState(websiteData.contact_us?.phone || "");
  const [coordinates, setCoordinates] = useState(null);
  const [loading, setLoading] = useState(true);
  const [popupMessage, setPopupMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { editMode } = useEditMode();
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [saveButtonText, setSaveButtonText] = useState("Save Changes");
  const [shouldFetchCoordinates, setShouldFetchCoordinates] = useState(false);

  const domain = sessionStorage.getItem("domain");

  // Initial data fetch - only run once
  useEffect(() => {
    const fetchContactDetails = async () => {
      try {
        const data = await getContactUs(domain);
        if (data.response === "true") {
          const fetchedAddress = data.data.address || "";
          const fetchedEmail = data.data.email || "";
          const fetchedPhone = data.data.phone_num || "";

          // Update state with fetched data
          setAddress(fetchedAddress);
          setEmail(fetchedEmail);
          setPhoneNum(fetchedPhone);

          // Update website context
          setWebsite((prev) => ({
            ...prev,
            contact_us: {
              email: fetchedEmail,
              phone: fetchedPhone,
              address: fetchedAddress,
            },
          }));

          // Signal to fetch coordinates after we have address
          if (fetchedAddress) {
            setShouldFetchCoordinates(true);
          }
        }
      } catch (err) {
        setErrorMessage("Failed to load contact details.");
      } finally {
        setLoading(false);
      }
    };

    fetchContactDetails();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Empty dependency array - run only once

  function removePostcode(address) {
    return address.replace(/,?\s*\b\d{5,7}\b/, "");
  }

  // Separate effect for fetching coordinates - only run when needed
  useEffect(() => {
    // Skip if we don't need to fetch coordinates or if address is empty
    if (!shouldFetchCoordinates || !address) return;

    const fetchCoordinates = async () => {
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
            address
          )}&format=json`
        );
        const data = await response.json();
        if (data.length > 0) {
          setCoordinates({
            lat: parseFloat(data[0].lat),
            lng: parseFloat(data[0].lon),
          });
        }
      } catch (err) {
        console.error("Geocoding error:", err);
      } finally {
        // Reset the flag to prevent unnecessary fetches
        setShouldFetchCoordinates(false);
      }
    };

    fetchCoordinates();
  }, [shouldFetchCoordinates, address]);

  function LocationSelector() {
    useMapEvents({
      click: async (e) => {
        const { lat, lng } = e.latlng;
        setCoordinates({ lat, lng });
        try {
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json&accept-language=en`
          );
          const data = await response.json();
          if (data && data.display_name) {
            setAddress(data.display_name);
            setHasUnsavedChanges(true);
            setSaveButtonText("Save Changes");
          }
        } catch (err) {
          console.error("Reverse geocoding error:", err);
        }
      },
    });
    return null;
  }

  const handleSave = async () => {
    setSaveButtonText("Saving...");
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
        setPopupMessage("Contact information updated successfully!");
        setSaveButtonText("Saved");
        setHasUnsavedChanges(false);

        // Update website context
        setWebsite((prev) => ({
          ...prev,
          contact_us: {
            email: email,
            phone: phoneNum,
            address: address,
          },
        }));
      } else {
        setErrorMessage("An error occurred while saving changes.");
        setSaveButtonText("Save Changes");
      }
    } catch (error) {
      setErrorMessage("An error occurred while saving changes.");
      setSaveButtonText("Save Changes");
    }
  };

  const handleChange = (setter) => (e) => {
    setter(e.target.value);
    setHasUnsavedChanges(true);
    setSaveButtonText("Save Changes");
  };

  // When address changes in edit mode, set flag to fetch new coordinates
  const handleAddressChange = (e) => {
    setAddress(e.target.value);
    setHasUnsavedChanges(true);
    setSaveButtonText("Save Changes");
    // Don't trigger coordinates fetch immediately, wait for save
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

  if (loading) {
    return (
      <div className="contact-page__loading">
        <div className="loading-spinner"></div>
        <p>Loading contact information...</p>
      </div>
    );
  }

  return (
    <div className="contact-page">
      <div className="contact-page__container">
        <div className="contact-page__header">
          <h1 className="contact-page__title">Contact Us</h1>
          {editMode && (
            <div className="contact-page__edit-badge">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
              <span>Edit Mode</span>
            </div>
          )}
        </div>

        <div className="contact-page__content">
          <div className="contact-page__info">
            <div className="contact-card">
              <div className="contact-card__section">
                <div className="contact-card__icon">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                  </svg>
                </div>
                <div className="contact-card__content">
                  <h3 className="contact-card__label">Address</h3>
                  {editMode ? (
                    <input
                      type="text"
                      value={removePostcode(address)}
                      onChange={handleAddressChange}
                      className="contact-card__input"
                      placeholder="Enter location address"
                    />
                  ) : (
                    <p className="contact-card__text">
                      {removePostcode(address)}
                    </p>
                  )}
                  {editMode && (
                    <div className="contact-card__hint">
                      Click on the map to set a new location
                    </div>
                  )}
                </div>
              </div>

              <div className="contact-card__section">
                <div className="contact-card__icon">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                    <polyline points="22,6 12,13 2,6"></polyline>
                  </svg>
                </div>
                <div className="contact-card__content">
                  <h3 className="contact-card__label">Email</h3>
                  {editMode ? (
                    <input
                      type="email"
                      value={email}
                      onChange={handleChange(setEmail)}
                      className="contact-card__input"
                      placeholder="Enter email address"
                    />
                  ) : (
                    <a href={`mailto:${email}`} className="contact-card__link">
                      {email}
                    </a>
                  )}
                </div>
              </div>

              <div className="contact-card__section">
                <div className="contact-card__icon">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                  </svg>
                </div>
                <div className="contact-card__content">
                  <h3 className="contact-card__label">Phone</h3>
                  {editMode ? (
                    <input
                      type="text"
                      value={phoneNum}
                      onChange={handleChange(setPhoneNum)}
                      className="contact-card__input"
                      placeholder="Enter phone number"
                    />
                  ) : (
                    <p className="contact-card__text">{phoneNum}</p>
                  )}
                </div>
              </div>

              {editMode && (
                <div className="contact-card__actions">
                  <button
                    className={`button ${
                      hasUnsavedChanges ? "button--primary" : "button--disabled"
                    }`}
                    onClick={handleSave}
                    disabled={!hasUnsavedChanges}
                  >
                    {saveButtonText}
                  </button>
                </div>
              )}
            </div>
          </div>

          <div className="contact-page__map">
            {coordinates ? (
              <div className="map-container">
                <MapContainer
                  center={[coordinates.lat, coordinates.lng]}
                  zoom={15}
                  style={{
                    height: "100%",
                    width: "100%",
                    borderRadius: "12px",
                  }}
                  scrollWheelZoom={false}
                >
                  <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; OpenStreetMap contributors"
                  />
                  <Marker position={[coordinates.lat, coordinates.lng]} />
                  {editMode && <LocationSelector />}
                </MapContainer>
              </div>
            ) : (
              <div className="map-placeholder">
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
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                  <circle cx="12" cy="10" r="3"></circle>
                </svg>
                <p>Map loading...</p>
              </div>
            )}
          </div>
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
