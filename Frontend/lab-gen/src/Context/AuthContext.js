import React, { createContext, useState, useEffect } from "react";
import { SendLogin, SendLogout, EnterSystem } from "../services/UserService";

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
    let data = await SendLogout();
    console.log(data);
    if (data.response === "true") {
      return true;
    }
    return false;
  };

  const fetchToken = async () => {
    let data = await EnterSystem();
    if (data) {
      sessionStorage.setItem("sid", data);
      console.log(data);
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
