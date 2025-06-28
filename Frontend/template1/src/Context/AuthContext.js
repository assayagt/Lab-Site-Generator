import React, { createContext, useState, useEffect } from "react";
import { SendLogin, SendLogout, EnterSystem } from "../services/UserService";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // ✅ NEW: hold user info (email)

  const login = async (token) => {
    let data = await SendLogin(
      token,
      sessionStorage.getItem("sid"),
      sessionStorage.getItem("domain")
    );
    console.log(data);

    if (data && data.response === "true") {
      sessionStorage.setItem("isLoggedIn", true);
      sessionStorage.setItem("userEmail", data.email);
      const email = data.email;
      setUser({ email });
      sessionStorage.setItem('sid', data.user_id);
      return true;
    }
    return false;
  };

  const logout = async () => {
    sessionStorage.removeItem("isLoggedIn");
    sessionStorage.removeItem("userEmail");
    sessionStorage.removeItem("sid");
    return true
  };

  const fetchToken = async () => {
    let data = await EnterSystem();
    if (data) {
      sessionStorage.setItem("sid", data);
      return data;
    }
    return data;
  };
  useEffect(() => {
    const savedEmail = sessionStorage.getItem("userEmail");
    if (savedEmail) {
      setUser({ email: savedEmail });
    }
  }, []);
  return (
    <AuthContext.Provider value={{ login, logout, fetchToken, user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return React.useContext(AuthContext);
};
