import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";



export const getCustomWebsites = async (userId) => {
    try {
        const response = await axios.get(`${baseApiUrl}getCustomWebsites`, { params: { user_id: userId } });
        return response.data.websites;
    } catch (error) {
        console.error("Error fetching custom websites:", error);
        return [];
    }
};

export const getCustomSite = async (userId, domain) => {
    try {
        const response = await axios.get(`${baseApiUrl}getCustomSite`, { params: { user_id: userId, domain } });
        return response.data.data;
    } catch (error) {
        console.error("Error getting custom site details:", error);
        return null;
    }
};