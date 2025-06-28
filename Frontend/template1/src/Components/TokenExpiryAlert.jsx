import React from 'react';
import { useAuth } from '../Context/AuthContext';
import './TokenExpiryAlert.css';

const TokenExpiryAlert = () => {
  const { error, clearError } = useAuth();

  if (!error) return null;

  const isTokenExpired = error.includes('expired') || error.includes('session');

  return (
    <div className={`token-expiry-alert ${isTokenExpired ? 'expired' : 'error'}`}>
      <div className="alert-content">
        <span className="alert-icon">
          {isTokenExpired ? '⏰' : '⚠️'}
        </span>
        <span className="alert-message">{error}</span>
        <button className="alert-close" onClick={clearError}>
          ×
        </button>
      </div>
    </div>
  );
};

export default TokenExpiryAlert; 