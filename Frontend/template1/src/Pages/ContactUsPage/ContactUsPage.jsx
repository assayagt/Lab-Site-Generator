import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./ContactUsPage.css";
import {
  getContactUs,
  setSiteContactInfoByManager,
} from "../../services/websiteService";
import { useEditMode } from "../../Context/EditModeContext";
import SuccessPopup from "../../Components/PopUp/SuccessPopup";
import ErrorPopup from "../../Components/PopUp/ErrorPopup";
import { useWebsite } from "../../Context/WebsiteContext";

// Fix default marker icon for Leaflet
L.Marker.prototype.options.icon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

function ContactUsPage() {
  const { websiteData, setWebsite } = useWebsite();
  const { editMode } = useEditMode();

  const [address, setAddress] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNum, setPhoneNum] = useState("");
  const [coordinates, setCoordinates] = useState(null);

  const [loading, setLoading] = useState(true);
  const [popupMessage, setPopupMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [saveButtonText, setSaveButtonText] = useState("Save");

  const domain = sessionStorage.getItem("domain");

  // Remove postcode from address (optional)
  const removePostcode = (addr) => addr.replace(/,?\s*\b\d{5,7}\b/, "");

  useEffect(() => {
    const fetchContactDetails = async () => {
      try {
        const data = await getContactUs(domain);
        if (data.response === "true") {
          const addr = data.data.address || "";
          setAddress(addr);
          setEmail(data.data.email || "");
          setPhoneNum(data.data.phone_num || "");

          setWebsite({
            contact_us: {
              email: data.data.email,
              phone: data.data.phone_num,
              address: addr,
            },
          });

          // Fetch coordinates based on fetched address
          if (addr) {
            const res = await fetch(
              `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
                addr
              )}&format=json`
            );
            const geo = await res.json();
            if (geo.length > 0) {
              setCoordinates({
                lat: parseFloat(geo[0].lat),
                lng: parseFloat(geo[0].lon),
              });
            }
          }
        }
      } catch (err) {
        setErrorMessage("Failed to load contact details.");
      } finally {
        setLoading(false);
      }
    };

    fetchContactDetails();
  }, [domain]);

  const handleChange = (setter) => (e) => {
    setter(e.target.value);
    setHasUnsavedChanges(true);
    setSaveButtonText("Save");
  };

  const handleSave = async () => {
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
        setWebsite({
          contact_us: { email, phone: phoneNum, address },
        });
      } else {
        setErrorMessage(response.message);
      }
    } catch (error) {
      setErrorMessage("An error occurred while saving.");
    }
  };

  const LocationSelector = () => {
    useMapEvents({
      click: async ({ latlng }) => {
        const { lat, lng } = latlng;
        setCoordinates({ lat, lng });
        try {
          const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json&accept-language=en`
          );
          const data = await res.json();
          if (data?.display_name) {
            setAddress(data.display_name);
            setHasUnsavedChanges(true);
            setSaveButtonText("Save");
          }
        } catch (err) {
          console.error("Reverse geocoding error:", err);
        }
      },
    });
    return null;
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

  const mapCenter = coordinates
    ? [coordinates.lat, coordinates.lng]
    : [31.2615, 34.7978]; // Default fallback (BGU)

  return (
    <div className="contact_page">
      <div className="page_title">Contact Us</div>
      <div className="contact_info">
        <div>
          <strong>Address:</strong>{" "}
          {editMode ? (
            <input
              type="text"
              value={removePostcode(address)}
              onChange={handleChange(setAddress)}
              className="contact_input"
            />
          ) : (
            removePostcode(address)
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
            <a href={`mailto:${email}`} className="email-link">
              {email}
            </a>
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

        <div className="map_container">
          <MapContainer
            center={mapCenter}
            zoom={15}
            style={{ height: "300px", width: "100%" }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap contributors"
            />
            {coordinates && <Marker position={mapCenter} />}
            {editMode && <LocationSelector />}
          </MapContainer>
        </div>

        {editMode && (
          <div className="button_container">
            <button
              type="button"
              className="saveButton_contact"
              onClick={handleSave}
              disabled={!hasUnsavedChanges}
            >
              {saveButtonText}
            </button>
          </div>
        )}
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
