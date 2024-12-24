import React, { createContext, useState, useEffect } from 'react';

// Create context for authentication
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
  };

  const logout = () => {
    setIsLoggedIn(false);
    setUserEmail('');
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userEmail');
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, userEmail, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return React.useContext(AuthContext);
};
