import React, { useState } from "react";
import { useAuth } from "../../Context/AuthContext"; // Assuming you have this context
import "./LoginPopup.css"; // Add necessary styles
import { useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { jwtDecode } from "jwt-decode";

const LoginPopup = ({ onClose, onLoginSuccess, loginError, setLoginError }) => {
  const [email, setEmail] = useState("");
  const [error, setError] = useState(setLoginError);
  const [errorMsg, setErrorMsg] = useState(loginError);
  const { login, fetchToken } = useAuth(); // Access the login function from context
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (email) {
      try {
        let data = await login(email); // Await the login function to get the result
        if (data.response === "false") {
          setError(true);
        } else {
          setError(false);
          setErrorMsg(data);
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
      //await fetchToken();

      const token = credentialResponse.credential; // ✅ SEND THE RAW TOKEN

      // const email = decoded.email;

      const success = await login(token); // This still hits your backend
      if (success.response === "true") {
        onClose();
        navigate("/choose-components");
      } else {
        setError(true);
        setErrorMsg(success.message);
      }
    } catch (err) {
      console.error("Google login error:", err);
      setErrorMsg(err);
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

        {/* <input
          className="login-input"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        /> */}

        {error && <div className="login-error">{errorMsg}</div>}

        {/* <button className="login-button" onClick={handleGoogleSuccess}>
          Login
        </button> */}
        <GoogleLogin
          onSuccess={handleGoogleSuccess}
          onError={() => {
            setError(true);
            console.log("Login Failed");
          }}
          ux_mode="popup" // ensures a new token is fetched every time
        />
      </div>
    </div>
  );
};

export default LoginPopup;
