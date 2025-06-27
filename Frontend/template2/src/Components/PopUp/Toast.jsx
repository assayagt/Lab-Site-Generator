import React from 'react';
import { Toast } from 'react-bootstrap';
import './Toast.css';

const CustomToast = ({ show, onClose, message, type = 'success' }) => {
  const variant = type === 'success' ? 'success' : 'danger';
  const title = type === 'success' ? 'Success' : 'Error';

  return (
    <Toast 
      show={show} 
      onClose={onClose}
      className={`custom-toast ${type}`}
      delay={3000}
      autohide
    >
      <Toast.Header closeButton>
        <strong className="me-auto">{title}</strong>
      </Toast.Header>
      <Toast.Body>{message}</Toast.Body>
    </Toast>
  );
};

export default CustomToast; 