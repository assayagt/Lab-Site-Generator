import axios from "axios";

import { baseApiUrl } from "./BaseUrl"; // Ensure the path is correct relative to this file

export const getCustomWebsites = async (userId) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}getCustomWebsites?user_id=${userId}`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching custom websites:", error);
    return [];
  }
};

export const getCustomSite = async (userId, domain) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}getCustomSite?domain=${domain}&user_id=${userId}`
    );
    return response.data;
  } catch (error) {
    console.error("Error getting custom site details:", error);
    return null;
  }
};

export const deleteWebsite = async (userId, domain) => {
  try {
    const response = await axios.delete(`${baseApiUrl}deleteWebsite`, {
      params: {
        user_id: userId,
        domain: domain,
      },
    });

    return response.data;
  } catch (error) {
    console.error("Error deleting website:", error);
    return null;
  }
};
