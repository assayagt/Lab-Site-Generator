import React from "react";
import "./LoadingPopup.css";

const LoadingPopup = ({ message }) => {
  if (!message) return null; // Don't show if not loading

  return (
    <div className="popup-overlay">
      <div className="loading-popup-content">
        <div className="spinner"></div>
        <p>{message}</p>
      </div>
    </div>
  );
};

export default LoadingPopup;
