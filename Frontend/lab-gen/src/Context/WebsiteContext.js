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
    created: false,
    generated: false,
    about_us: "", // ✅ Add this
    contact_us: {
      // ✅ And this
      address: "",
      email: "",
      phone_num: "",
    },
  };

  const [websiteData, setWebsiteData] = useState(initialWebsiteData);

  const setWebsite = (newData) => {
    setWebsiteData((prev) => ({
      ...prev,
      ...newData,
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
