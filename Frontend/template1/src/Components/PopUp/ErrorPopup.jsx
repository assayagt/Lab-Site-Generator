import React from "react";
import "./ErrorPopup.css"; // Use same CSS file or separate if preferred

const ErrorPopup = ({ message, onClose }) => {
  return (
    <div className="popup-overlay">
      <div className="popup error">
        <button className="close-popup" onClick={onClose}>
          ✕
        </button>
        <h3 className="popup-title">Error</h3>
        <p>{message}</p>
      </div>
    </div>
  );
};

export default ErrorPopup;
