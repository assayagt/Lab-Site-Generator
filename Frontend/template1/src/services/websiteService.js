import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";

export const addLabMember = async (userId, email, fullName, degree, domain) => {
    let data;
    try {
        const response = await axios.post(`${baseApiUrl}addLabMember`, {
            user_id: userId,
            email,
            full_name: fullName,
            degree,
            domain
        });
        data = response.data;
    } catch (error) {
        console.error("Error adding lab member:", error);
        return null;
    }
    return data;
};

export const addLabManager = async (userId, email, domain) => {
    let data;
    try {
        const response = await axios.post(`${baseApiUrl}addLabManager`, {
            user_id: userId,
            email,
            domain
        });
        data = response.data;
       
    } catch (error) {
        console.error("Error adding lab manager:", error);
        return null;
    }
    return data;
};



export const approveRegistration = async (data) => { 
    let data2;
    try {
        const response = await axios.post(`${baseApiUrl}approveRegistration`, data);
        data2 = response.data.message;
    } catch (error) {
        console.error("Error approving registration:", error);
        return null;
    }
    return data2;
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
        let data;
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




export const getApprovedPublications = async (domain) => {
    try {
        const response = await axios.get(`${baseApiUrl}getApprovedPublications`, { params: { domain } });
        return response.data.publications;
    } catch (error) {
        console.error("Error getting approved publications:", error);
        return [];
    }
};

export const addPublication = async (data) => {
    try {
        const response = await axios.post(`${baseApiUrl}addPublication`, data);
        return response.data.message;
    } catch (error) {
        console.error("Error adding publication:", error);
        return null;
    }
};

export const setPublicationVideoLink = async (userId, domain, publicationId, videoLink) => {
    try {
        const response = await axios.post(`${baseApiUrl}setPublicationVideoLink`, {
            user_id: userId,
            domain,
            publication_id: publicationId,
            video_link: videoLink
        });
        return response.data.message;
    } catch (error) {
        console.error("Error setting publication video link:", error);
        return null;
    }
};

export const setPublicationGitLink = async (userId, domain, publicationId, gitLink) => {
    try {
        const response = await axios.post(`${baseApiUrl}setPublicationGitLink`, {
            user_id: userId,
            domain,
            publication_id: publicationId,
            git_link: gitLink
        });
        return response.data.message;
    } catch (error) {
        console.error("Error setting publication Git link:", error);
        return null;
    }
};

export const setPublicationPttxLink = async (userId, domain, publicationId, presentationLink) => {
    try {
        const response = await axios.post(`${baseApiUrl}setPublicationPttxLink`, {
            user_id: userId,
            domain,
            publication_id: publicationId,
            presentation_link: presentationLink
        });
        return response.data.message;
    } catch (error) {
        console.error("Error setting publication presentation link:", error);
        return null;
    }
};




export const removeSiteManager = async (userId, managerEmail, domain) => {
    try {
        const response = await axios.post(`${baseApiUrl}removeSiteManager`, {
            nominator_manager_userId: userId,
            manager_toRemove_email: managerEmail,
            domain
        });
        return response.data.message;
    } catch (error) {
        console.error("Error removing site manager:", error);
        return null;
    }
};

export const getMemberPublications = async (domain, email) => {
    try {
        const response = await axios.get(`${baseApiUrl}getMemberPublications`, { params: { domain, email } });
        return response.data.publications;
    } catch (error) {
        console.error("Error getting member publications:", error);
        return [];
    }
};


export const getHomepageDetails = async (domain) => {
    try {
        const response = await axios.get(`${baseApiUrl}getHomepageDetails`, { params: { domain } });
        return response.data;  // Assuming the backend sends the data in a property named 'data'
    } catch (error) {
        console.error("Error getting homepage details:", error);
        return null;
    }
};