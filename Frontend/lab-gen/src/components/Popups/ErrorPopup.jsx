import React from "react";
import "./ErrorPopup.css";

const ErrorPopup = ({ message, onClose }) => {
  if (!message) return null; // Don't show if no error

  return (
    <div className="error-popup-overlay">
      <div className="error-popup">
        <h3>Error</h3>
        <p>{message}</p>
        <button onClick={onClose} className="close-error-button">
          Close
        </button>
      </div>
    </div>
  );
};

export default ErrorPopup;
