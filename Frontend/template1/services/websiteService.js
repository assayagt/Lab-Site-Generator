import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";

export const addLabMember = async (userId, email, fullName, degree, domain) => {
    try {
        const response = await axios.post(`${baseApiUrl}addLabMember`, {
            user_id: userId,
            email,
            full_name: fullName,
            degree,
            domain
        });
        return response.data.message;
    } catch (error) {
        console.error("Error adding lab member:", error);
        return null;
    }
};

export const addLabManager = async (userId, email, domain) => {
    try {
        const response = await axios.post(`${baseApiUrl}addLabManager`, {
            user_id: userId,
            email,
            domain
        });
        return response.data.message;
    } catch (error) {
        console.error("Error adding lab manager:", error);
        return null;
    }
};

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
        console.error("Error fetching custom site details:", error);
        return null;
    }
};

export const approveRegistration = async (data) => {
    try {
        const response = await axios.post(`${baseApiUrl}approveRegistration`, data);
        return response.data.message;
    } catch (error) {
        console.error("Error approving registration:", error);
        return null;
    }
};

export const rejectRegistration = async (data) => {
    try {
        const response = await axios.post(`${baseApiUrl}rejectRegistration`, data);
        return response.data.message;
    } catch (error) {
        console.error("Error rejecting registration:", error);
        return null;
    }
};

export const getAllLabManagers = async (domain) => {
    try {
        const response = await axios.get(`${baseApiUrl}getAllLabManagers`, { params: { domain } });
        return response.data.managers;
    } catch (error) {
        console.error("Error getting all lab managers:", error);
        return [];
    }
};

export const getAllLabMembers = async (domain) => {
    try {
        const response = await axios.get(`${baseApiUrl}getAllLabMembers`, { params: { domain } });
        return response.data.members;
    } catch (error) {
        console.error("Error getting all lab members:", error);
        return [];
    }
};

export const getAllAlumni = async (domain) => {
    try {
        const response = await axios.get(`${baseApiUrl}getAllAlumni`, { params: { domain } });
        return response.data.alumni;
    } catch (error) {
        console.error("Error getting all alumni:", error);
        return [];
    }
};

// You can add more functions as needed for other endpoints in a similar fashion.
export const setSecondEmailByMember = async (userId, secondEmail, domain) => {
    try {
        const response = await axios.post(`${baseApiUrl}setSecondEmail`, {
            userid: userId,
            secondEmail,
            domain
        });
        return response.data.message;
    } catch (error) {
        console.error("Error setting second email:", error);
        return null;
    }
};

export const setLinkedInLinkByMember = async (userId, linkedInLink, domain) => {
    try {
        const response = await axios.post(`${baseApiUrl}setLinkedInLink`, {
            userid: userId,
            linkedin_link: linkedInLink,
            domain
        });
        return response.data.message;
    } catch (error) {
        console.error("Error setting LinkedIn link:", error);
        return null;
    }
};

export const setFullNameByMember = async (userId, fullName, domain) => {
    try {
        const response = await axios.post(`${baseApiUrl}setFullName`, {
            userid: userId,
            fullName,
            domain
        });
        return response.data.message;
    } catch (error) {
        console.error("Error setting full name:", error);
        return null;
    }
};

export const setDegreeByMember = async (userId, degree, domain) => {
    try {
        const response = await axios.post(`${baseApiUrl}setDegree`, {
            userid: userId,
            degree,
            domain
        });
        return response.data.message;
    } catch (error) {
        console.error("Error setting degree:", error);
        return null;
    }
};

export const setBioByMember = async (userId, bio, domain) => {
    try {
        const response = await axios.post(`${baseApiUrl}setBio`, {
            userid: userId,
            bio,
            domain
        });
        return response.data.message;
    } catch (error) {
        console.error("Error setting bio:", error);
        return null;
    }
};

export const setMediaByMember = async (userId, media, domain) => {
    try {
        const response = await axios.post(`${baseApiUrl}setMedia`, {
            userid: userId,
            media,
            domain
        });
        return response.data.message;
    } catch (error) {
        console.error("Error setting media:", error);
        return null;
    }
};



export const fetchAllLabWebsites = async (userId) => {
    try {
        const response = await axios.get(`${baseApiUrl}getAllLabWebsites`, {
            params: { user_id: userId }
        });
        return response.data.websites;
    } catch (error) {
        console.error("Error fetching all lab websites:", error);
        return [];
    }
};
