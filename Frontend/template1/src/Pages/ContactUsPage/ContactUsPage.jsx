import React, { useState, useEffect } from "react";
import "./ContactUsPage.css";
import { getContactUs } from "../../services/websiteService"; // Adjust the path based on your project structure

function ContactUsPage() {
  const [coordinates, setCoordinates] = useState(null);
  const [address, setAddress] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNum, setPhoneNum] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const domain = sessionStorage.getItem("domain")

  useEffect(() => {
    const fetchContactDetails = async () => {
      try {
        const data = await getContactUs(domain);
        if (data.response ==="true") {
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
        } else {
          console.error("Address not found");
        }
      } catch (error) {
        console.error("Error fetching coordinates:", error);
      }
    };

    fetchCoordinates();
  }, [address]);

  const mapLink = coordinates
    ? `https://www.openstreetmap.org/?mlat=${coordinates.lat}&mlon=${coordinates.lon}&zoom=15`
    : "#";

  if (loading) {
    return <div className="loading">Loading contact details...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="contact_page">
      <div className="page_title">Contact Us</div>
      <div className="contact_info">
        <div>
          <strong>Address:</strong> {address}
        </div>
        <div>
          <strong>Email:</strong>{" "}
          {email && <a href={`mailto:${email}`} className="email-link">{email}</a>}
        </div>
        <div>
          <strong>Phone:</strong> {phoneNum}
        </div>
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
      
    </div>
  );
}

export default ContactUsPage;
