import React, { createContext, useState, useEffect } from 'react';
import {SendLogin, SendLogout,EnterSystem} from "../services/UserService"

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  
  // Retrieve from localStorage to persist login state across page reloads
  useEffect(() => {
    const loggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const savedUserEmail = localStorage.getItem('userEmail');
    
    if (loggedIn) {
      setIsLoggedIn(true);
      setUserEmail(savedUserEmail);
    }
  }, []);

  const login = (email) => {
    setIsLoggedIn(true);
    setUserEmail(email);
    localStorage.setItem('isLoggedIn', 'true');
    localStorage.setItem('userEmail', email);
    localStorage.setItem('sid',"id");
  };

  const logout = () => {
    setIsLoggedIn(false);
    setUserEmail('');
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('sid');
  };

  const fetchToken = async () => {
    let data = EnterSystem();
    if(data){
      localStorage.setItem('sid',data.user_id);
      
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
