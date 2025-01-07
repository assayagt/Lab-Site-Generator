import React, { useState, useEffect } from "react";
import "./ContactUsPage.css";

function ContactUsPage(props) {
  const [coordinates, setCoordinates] = useState(null);

  useEffect(() => {
    const fetchCoordinates = async () => {
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
            props.address
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
  }, [props.address]);

  const mapLink = coordinates
    ? `https://www.openstreetmap.org/?mlat=${coordinates.lat}&mlon=${coordinates.lon}&zoom=15`
    : "#";

  return (
    <div className="contact_page">
      <div className="page_title">Contact Us</div>
      <div className="contact_info">
        <div>
          <strong>Address:</strong> {props.address}
        </div>
        <div>
          <strong>Email:</strong> {                
            <a href={`mailto:${props.email}`} className="email-link">{props.email}</a>}
        </div>
        <div>
          <strong>Phone:</strong> {props.phone}
        </div>
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
  );
}

export default ContactUsPage;
