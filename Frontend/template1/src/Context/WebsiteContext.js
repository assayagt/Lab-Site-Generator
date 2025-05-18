import React, { createContext, useContext, useState } from "react";

const WebsiteContext = createContext();

export const useWebsite = () => {
  return useContext(WebsiteContext);
};

export const WebsiteProvider = ({ children }) => {
  const initialWebsiteData = {
    components: [],
    template: "",
    domain: "",
    websiteName: "",
    logo: "",
    home_picture: " ",
    about_us: " ",
    contact_us: {
      email: "",
      phone: "",
      address: "",
    },
  };

  const [websiteData, setWebsiteData] = useState(initialWebsiteData);

  const setWebsite = (newData) => {
    setWebsiteData((prev) => ({
      ...prev,
      ...newData,
      contact_us: {
        ...prev.contact_us,
        ...(newData.contact_us || {}),
      },
    }));
  };

  const resetWebsiteData = () => {
    setWebsiteData(initialWebsiteData);
  };

  return (
    <WebsiteContext.Provider
      value={{ websiteData, setWebsite, resetWebsiteData }}
    >
      {children}
    </WebsiteContext.Provider>
  );
};
