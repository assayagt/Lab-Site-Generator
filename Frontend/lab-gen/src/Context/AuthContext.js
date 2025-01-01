import React, { createContext, useState, useEffect } from 'react';
import {SendLogin, SendLogout,EnterSystem} from "../services/UserService"

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  
  // Retrieve from localStorage to persist login state across page reloads
  useEffect(() => {
    const loggedIn = sessionStorage.getItem('isLoggedIn') === 'true';
    const savedUserEmail = sessionStorage.getItem('userEmail');
    
    if (loggedIn) {
      setIsLoggedIn(true);
      setUserEmail(savedUserEmail);
    }
  }, []);

  const login = (email) => {
    setIsLoggedIn(true);
    setUserEmail(email);
    sessionStorage.setItem('isLoggedIn', 'true');
    sessionStorage.setItem('userEmail', email);
    sessionStorage.setItem('sid',"id");
  };

  const logout = () => {
    setIsLoggedIn(false);
    setUserEmail('');
    sessionStorage.removeItem('isLoggedIn');
    sessionStorage.removeItem('userEmail');
    sessionStorage.removeItem('sid');
  };

  const fetchToken = async () => {
    let data = await EnterSystem(); // Wait for the result of EnterSystem
    if (data) {
      sessionStorage.setItem('sid', data.user_id); 
    }
    
    return data;
  };
  

  return (
    <AuthContext.Provider value={{ isLoggedIn, userEmail, login, logout ,fetchToken}}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return React.useContext(AuthContext);
};
