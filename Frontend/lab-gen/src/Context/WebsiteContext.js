import React, { createContext, useContext, useState } from 'react';

const WebsiteContext = createContext();

export const useWebsite = () => {
  return useContext(WebsiteContext);
};

export const WebsiteProvider = ({ children }) => {
  const [websiteData, setWebsiteData] = useState({
    components: [],
    template: '',
    domain: '',
    websiteName: '',
    created : false
  });

  const setWebsite = (newData) => {
    setWebsiteData(prev => ({
      ...prev,
      ...newData
    }));
  };

  return (
    <WebsiteContext.Provider value={{ websiteData, setWebsite }}>
      {children}
    </WebsiteContext.Provider>
  );
};
