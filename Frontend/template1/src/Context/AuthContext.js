import React, { createContext, useState, useEffect } from "react";
import { SendLogin, SendLogout, EnterSystem } from "../services/UserService";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null); // ✅ NEW: hold user info (email)

  const login = async (email) => {
    let data = await SendLogin(
      email,
      sessionStorage.getItem("sid"),
      sessionStorage.getItem("domain")
    );
    console.log(data);
    if (data) {
      if (data.response === "true") {
        sessionStorage.setItem("isLoggedIn", true);
        sessionStorage.setItem("userEmail", email);
        setUser({ email });
        //sessionStorage.setItem('sid',"id"); still doesn't exist
        return true;
      }

      return false;
    }
    return false;
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
    <AuthContext.Provider value={{ login, logout, fetchToken, user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return React.useContext(AuthContext);
};
