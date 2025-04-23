// components/Popups/LoadingPopup.jsx
import React from "react";
import "./LoginPopup.css"; // Style this as needed

const LoadingPopup = ({ message }) => {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>{message}</h3>
      </div>
    </div>
  );
};

export default LoadingPopup;
