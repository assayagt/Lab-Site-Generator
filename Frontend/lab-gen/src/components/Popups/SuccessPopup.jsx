// SuccessPopup.jsx
import React from "react";
import "./SuccessPopup.css";

const SuccessPopup = ({ message, onClose }) => {
  if (!message) return null; // Don't show if no success message

  return (
    <div className="success-popup-overlay">
      <div className="success-popup">
        <h3>Success</h3>
        <p>{message}</p>
        <button onClick={onClose} className="close-success-button">
          Close
        </button>
      </div>
    </div>
  );
};

export default SuccessPopup;
