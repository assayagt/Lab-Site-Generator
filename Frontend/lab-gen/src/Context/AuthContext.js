import React, { createContext } from "react";
import { SendLogin, EnterSystem } from "../services/UserService";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const login = async (token) => {
    let data = await SendLogin(token, sessionStorage.getItem("sid"));
    if (data) {
      if (data.response === "true") {
        sessionStorage.setItem("isLoggedIn", true);
        sessionStorage.setItem("userEmail", data.email);
        sessionStorage.setItem('sid', data.user_id);
        return data;
      }
      return data;
    }
    return data;
  };

  const logout = async () => {
    sessionStorage.removeItem("isLoggedIn");
    sessionStorage.removeItem("userEmail");
    sessionStorage.removeItem('sid');
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

  return (
    <AuthContext.Provider value={{ login, logout, fetchToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return React.useContext(AuthContext);
};
