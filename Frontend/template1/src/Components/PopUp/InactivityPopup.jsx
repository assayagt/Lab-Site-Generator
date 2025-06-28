import React from "react";
import "./InactivityPopup.css"; // You can keep using this CSS

const InactivityPopup = ({ onClose }) => {
  return (
    <div className="login-popup-overlay">
      <div className="login-popup">
        <button className="close-popup" onClick={onClose}>
          ×
        </button>
        <h2 className="login-title">Session Expired</h2>
        <p className="login-subtitle">
          You have been logged out due to inactivity.
        </p>
      </div>
    </div>
  );
};

export default InactivityPopup;
