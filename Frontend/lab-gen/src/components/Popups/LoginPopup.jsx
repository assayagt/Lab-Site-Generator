import React, { useState } from "react";
import { useAuth } from "../../Context/AuthContext"; // Assuming you have this context
import "./LoginPopup.css"; // Add necessary styles
import { useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";

const LoginPopup = ({ onClose }) => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState(false);
  const { login } = useAuth(); // Access the login function from context
  const navigate = useNavigate();
  const handleLogin = async () => {
    if (email) {
      try {
        let data = await login(email); // Await the login function to get the result
        if (data === false) {
          setError(true);
        } else {
          setError(false);
          onClose();
          navigate("/choose-components");
        }
      } catch (err) {
        console.error("Login error:", err);
        setError(true);
      }
    } else {
      setError(true);
    }
  };
  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      const token = credentialResponse.credential; // ✅ SEND THE RAW TOKEN

      // const email = decoded.email;

      const success = await login(token); // This still hits your backend
      if (success) {
        onClose();
        navigate("/choose-components");
      } else {
        setError(true);
      }
    } catch (err) {
      console.error("Google login error:", err);
      setError(true);
    }
  };

  return (
    <div className="login-popup-overlay">
      <div className="login-popup">
        <button className="close-popup" onClick={onClose}>
          ×
        </button>
        <h2 className="login-title">Welcome Back</h2>
        <p className="login-subtitle">
          Login with your University Google account
        </p>

        <input
          className="login-input"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        {error && (
          <div className="login-error">Invalid email. Please try again.</div>
        )}

        {/* <button className="login-button" onClick={handleGoogleSuccess}>
          Login
        </button> */}
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={() => {
            setError(true);
            console.log("Login Failed");
          }}
        />
      </div>
    </div>
  );
};

export default LoginPopup;
