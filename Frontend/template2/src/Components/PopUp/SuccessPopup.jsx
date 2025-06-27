import React from "react";
import "./SuccessPopup.css";

const SuccessPopup = ({ message, onClose }) => {
  return (
    <div className="success-popup">
      <div className="popup-content">{message}</div>
    </div>
  );
};

export default SuccessPopup;
