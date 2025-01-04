import React, { createContext, useState, useEffect } from 'react';
import {SendLogin, SendLogout,EnterSystem} from "../services/UserService"

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  

  useEffect(() => {
    const loggedIn = sessionStorage.getItem('isLoggedIn') === 'true';
    const savedUserEmail = sessionStorage.getItem('userEmail');
    
    if (loggedIn) {
      setIsLoggedIn(true);
      setUserEmail(savedUserEmail);
    }
  }, []);

  const login = async (email) => {
    let data = await SendLogin(email,sessionStorage.getItem("sid"));
    if(data){
      if(data.response === "true"){
        setIsLoggedIn(true);
        setUserEmail(email);
        sessionStorage.setItem('isLoggedIn', 'true');
        sessionStorage.setItem('userEmail', email);
        //sessionStorage.setItem('sid',"id"); still doesn't exist
        return true;
      }
      return false;
    }
    return false; 
  };

  const logout = async () => {
    let data =  await SendLogout();
    console.log(data);
    if(data.response === "true"){
      setUserEmail('');
      return true;
    }
    return false; 
  };

  const fetchToken = async () => {
    let data = await EnterSystem(); 
    if (data) {
      sessionStorage.setItem('sid', data); 
      return data;
    }
    return data;
  };
  

  return (
    <AuthContext.Provider value={{ isLoggedIn, userEmail, login, logout ,fetchToken,setIsLoggedIn}}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  return React.useContext(AuthContext);
};
