import React, { useState } from "react";
import { useAuth } from "../../Context/AuthContext";
import "./LoginPopup.css";
import { useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";

const LoginPopup = ({ onClose }) => {
  const [error, setError] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const token = credentialResponse.credential;
      const result = await login(token); // your backend should validate this token

      if (result.response === "true") {
        setError(false);
        onClose(); // close the popup
        navigate("/choose-components"); // redirect after login
      } else {
        setError(true);
        setErrorMsg(result.message || "Login failed.");
      }
    } catch (err) {
      console.error("Google login error:", err);
      setError(true);
      setErrorMsg("Login failed. Please try again.");
    }
  };

  return (
    <div
      className="login-popup-overlay"
      onClick={(e) => {
        if (e.target.className === "login-popup-overlay") {
          onClose();
        }
      }}
    >
      <div className="login-popup">
        <button className="close-popup" onClick={onClose}>
          ×
        </button>
        <h2 className="login-title">Welcome Back</h2>
        <p className="login-subtitle">
          Login with your University Google account
        </p>

        {error && (
          <div className="login-error">
            {errorMsg || "Invalid email. Please try again."}
          </div>
        )}

        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={() => {
            setError(true);
            setErrorMsg("Login failed. Please try again.");
          }}
          ux_mode="popup"
        />
      </div>
    </div>
  );
};

export default LoginPopup;
