import React, { createContext, useContext, useState } from 'react';

const WebsiteContext = createContext();

export const useWebsite = () => {
  return useContext(WebsiteContext);
};

export const WebsiteProvider = ({ children }) => {
  const initialWebsiteData = {
    components: [],
    template: '',
    domain: '',
    websiteName: '',
    created: false
  };

  const [websiteData, setWebsiteData] = useState(initialWebsiteData);

  const setWebsite = (newData) => {
    setWebsiteData(prev => ({
      ...prev,
      ...newData
    }));
  };

  const resetWebsiteData = () => {
    setWebsiteData(initialWebsiteData);
    console.log(websiteData);
  };

  return (
    <WebsiteContext.Provider value={{ websiteData, setWebsite, resetWebsiteData }}>
      {children}
    </WebsiteContext.Provider>
  );
};