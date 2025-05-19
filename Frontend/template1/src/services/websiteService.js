import axios from "axios";
import { useId } from "react";

import { baseApiUrl } from "./BaseUrl"; // Ensure the path is correct relative to this file

export const addLabMember = async (userId, email, fullName, degree, domain) => {
  let data;
  try {
    const response = await axios.post(`${baseApiUrl}addLabMember`, {
      user_id: userId,
      email,
      full_name: fullName,
      degree,
      domain,
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
      domain,
    });
    data = response.data;
  } catch (error) {
    console.error("Error adding lab manager:", error);
    return null;
  }
  return data;
};

export const approveRegistration = async ({
  domain,
  manager_userId,
  notification_id,
  requested_full_name,
  requested_degree,
}) => {
  try {
    const response = await axios.post(`${baseApiUrl}approveRegistration`, {
      domain,
      manager_userId,
      requested_full_name,
      requested_degree,
      notification_id,
    });
    console.log(response.data);
    return response.data.message;
  } catch (error) {
    console.error("Error approving registration:", error);
    return null;
  }
};

export const rejectRegistration = async ({
  domain,
  manager_userId,
  notification_id,
}) => {
  try {
    const response = await axios.post(`${baseApiUrl}rejectRegistration`, {
      domain,
      manager_userId,
      notification_id,
    });
    console.log(response.data);
    return response.data.message;
  } catch (error) {
    console.error("Error rejecting registration:", error);
    return null;
  }
};

export const getAllLabManagers = async (domain) => {
  try {
    let data;
    const response = await axios.get(
      `${baseApiUrl}getAllLabManagers?domain=${domain}`
    );
    console.log(response.data);
    return response.data.managers;
  } catch (error) {
    console.error("Error getting all lab managers:", error);
    return [];
  }
};

export const getAllLabMembers = async (domain) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}getAllLabMembers?domain=${domain}`
    );
    console.log(response.data);
    return response.data.members;
  } catch (error) {
    console.error("Error getting all lab members:", error);
    return [];
  }
};

export const getAllAlumni = async (domain) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}getAllAlumni?domain=${domain}`
    );
    console.log(response.data);
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
      domain,
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
      domain,
    });
    console.log(response);
    return response.data;
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
      domain,
    });
    return response.data;
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
      domain,
    });
    return response.data;
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
      domain,
    });
    console.log(response.data);
    return response.data;
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
      domain,
    });
    return response.data.message;
  } catch (error) {
    console.error("Error setting media:", error);
    return null;
  }
};

export const getApprovedPublications = async (domain) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}getApprovedPublications?domain=${domain}`
    );
    console.log(response.data);
    return response.data.publications;
  } catch (error) {
    console.error("Error getting approved publications:", error);
    return [];
  }
};

export const addPublication = async (
  publication_link,
  domain,
  git_link,
  video_link,
  presentation_link
) => {
  try {
    console.log(publication_link);
    const response = await axios.post(`${baseApiUrl}addPublication`, {
      user_id: sessionStorage.getItem("sid"),
      publication_link: publication_link,
      domain: domain,
      video_link: video_link || "",
      git_link: git_link || "",
      presentation_link: presentation_link || "",
    });
    if (response) {
      console.log(response.data);
      return response.data;
    }
  } catch (error) {
    console.error("Error adding publication:", error);
    return null;
  }
  return "d";
};

export const setPublicationVideoLink = async (
  userId,
  domain,
  publicationId,
  videoLink
) => {
  try {
    const response = await axios.post(`${baseApiUrl}setPublicationVideoLink`, {
      user_id: userId,
      domain: domain,
      publication_id: publicationId,
      video_link: videoLink,
    });
    console.log(response);
    return response.data;
  } catch (error) {
    console.error("Error setting publication video link:", error);
    return null;
  }
};

export const setPublicationGitLink = async (
  userId,
  domain,
  publicationId,
  gitLink
) => {
  try {
    const response = await axios.post(`${baseApiUrl}setPublicationGitLink`, {
      user_id: userId,
      domain: domain,
      publication_id: publicationId,
      git_link: gitLink,
    });
    return response.data;
  } catch (error) {
    console.error("Error setting publication Git link:", error);
    return null;
  }
};

export const setPublicationPttxLink = async (
  userId,
  domain,
  publicationId,
  presentationLink
) => {
  try {
    const response = await axios.post(`${baseApiUrl}setPublicationPttxLink`, {
      user_id: userId,
      domain: domain,
      publication_id: publicationId,
      presentation_link: presentationLink,
    });
    const dd = response.data;
    console.log(dd);
    return dd;
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
      domain,
    });
    return response.data.message;
  } catch (error) {
    console.error("Error removing site manager:", error);
    return null;
  }
};

export const getMemberPublications = async (domain) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}getMemberPublications?domain=${domain}&user_id=${sessionStorage.getItem(
        "sid"
      )}`
    );
    console.log(response.data);
    return response.data.publications;
  } catch (error) {
    console.error("Error getting member publications:", error);
    return [];
  }
};

export const getHomepageDetails = async (domain) => {
  let data;
  await axios
    .get(`${baseApiUrl}getHomepageDetails?domain=${domain}`)
    .then((resp) => {
      data = resp.data;
      console.log(data);
      return data;
    })
    .catch((err) => console.log(err.message));
  return data;
};
export const getContactUs = async (domain) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}getContactUs?domain=${domain}`
    );
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error getting all alumni:", error);
    return [];
  }
};

export const getUserDetails = async (domain, user_id) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}getUserDetails?domain=${domain}&user_id=${user_id}`
    );
    console.log(response.data); // Log the response data
    return response.data; // Return the data
  } catch (error) {
    console.error("Error getting user details:", error); // Log the error
    return {}; // Return an empty object if there's an error
  }
};

export const addAlumniFromLabWebsite = async (
  managerUserId,
  memberEmail,
  domain
) => {
  try {
    const response = await axios.post(`${baseApiUrl}addAlumniFromLabWebsite`, {
      manager_user_id: managerUserId,
      member_email: memberEmail,
      domain,
    });
    return response.data;
  } catch (error) {
    console.error("Error adding alumni from lab website:", error);
    return null;
  }
};

export const addLabMemberFromWebsite = async (
  userId,
  email,
  fullName,
  degree,
  domain
) => {
  try {
    const response = await axios.post(`${baseApiUrl}addLabMemberFromWebsite`, {
      user_id: userId,
      email,
      full_name: fullName,
      degree,
      domain,
    });
    return response.data;
  } catch (error) {
    console.error("Error adding lab member from website:", error);
    return null;
  }
};

export const createNewSiteManagerFromLabWebsite = async (
  userId,
  email,
  domain
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}createNewSiteManagerFromLabWebsite`,
      {
        user_id: userId,
        email,
        domain,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error creating new site manager from lab website:", error);
    return null;
  }
};

export const siteCreatorResignationFromLabWebsite = async (
  userId,
  domain,
  email,
  newRole
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}siteCreatorResignationFromLabWebsite`,
      {
        user_id: userId,
        domain,
        email,
        new_role: newRole,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error processing site creator resignation:", error);
    return null;
  }
};

export const setSiteAboutUsByManager = async (userId, domain, aboutUs) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}setSiteAboutUsByManagerFromLabWebsite`,
      {
        user_id: userId,
        domain,
        about_us: aboutUs,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error setting About Us info:", error);
    return null;
  }
};

export const setSiteContactInfoByManager = async (
  userId,
  domain,
  labAddress,
  labMail,
  labPhoneNum
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}setSiteContactInfoByManagerFromLabWebsite`,
      {
        user_id: userId,
        domain,
        lab_address: labAddress,
        lab_mail: labMail,
        lab_phone_num: labPhoneNum,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error setting site contact info:", error);
    return null;
  }
};

export const initialApprovePublicationByAuthor = async (
  userId,
  domain,
  notificationId
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}initialApprovePublicationByAuthor`,
      {
        user_id: userId,
        domain: domain,
        notification_id: notificationId,
      }
    );
    return response.data; // includes { message, response: "true" | "false" }
  } catch (error) {
    console.error(
      "Error during initial publication approval by author:",
      error
    );
    return null;
  }
};

// Final approval of publication by lab manager
export const finalApprovePublicationByManager = async (
  userId,
  domain,
  notificationId
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}finalApprovePublicationByManager`,
      {
        user_id: userId,
        domain: domain,
        notification_id: notificationId,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error during final publication approval by manager:", error);
    return null;
  }
};

// Reject publication
export const rejectPublication = async (userId, domain, notificationId) => {
  try {
    const response = await axios.post(`${baseApiUrl}RejectPublication`, {
      user_id: userId,
      domain: domain,
      notification_id: notificationId,
    });
    return response.data;
  } catch (error) {
    console.error("Error rejecting publication:", error);
    return null;
  }
};

export const removeManagerPermission = async (
  managerUserId,
  managerEmail,
  domain
) => {
  try {
    const response = await axios.post(`${baseApiUrl}removeManagerPermission`, {
      manager_userId: managerUserId,
      manager_toRemove_email: managerEmail,
      domain,
    });
    return response.data;
  } catch (error) {
    console.error("Error removing manager permission:", error);
    return null;
  }
};

export const removeAlumniFromLabWebsite = async (
  managerUserId,
  alumniEmail,
  domain
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}removeAlumniFromLabWebsite`,
      {
        manager_user_id: managerUserId,
        alumni_email: alumniEmail,
        domain: domain,
      }
    );
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error removing alumni from lab website:", error);
    return null;
  }
};

export const crawlPublicationsForLabMember = async (userId, domain) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}crawlPublicationsForLabMember`,
      {
        user_id: userId,
        domain: domain,
      }
    );
    return response.data; // { message: "...", response: "true" | "false" }
  } catch (error) {
    console.error("Error crawling publications for lab member:", error);
    return null;
  }
};

export const rejectMultiplePublications = async (
  userId,
  domain,
  publicationIds
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}rejectMultiplePublications`,
      {
        user_id: userId,
        domain: domain,
        publication_IDs: publicationIds, // should be an array of strings
      }
    );
    return response.data; // { message: "...", response: "true" | "false" }
  } catch (error) {
    console.error("Error rejecting multiple publications:", error);
    return null;
  }
};
export const initialApproveMultiplePublicationsByAuthor = async (
  userId,
  domain,
  publicationIds
) => {
  try {
    console.log(publicationIds);
    const response = await axios.post(
      `${baseApiUrl}initialApproveMultiplePublicationsByAuthor`,
      {
        user_id: userId,
        domain: domain,
        publication_IDs: publicationIds,
      }
    );
    return response.data; // { message: "...", response: "true" | "false" }
  } catch (error) {
    console.error("Error during multiple initial approvals:", error);
    return null;
  }
};

export const setScholarLinkByMember = async (userId, scholarLink, domain) => {
  try {
    const response = await axios.post(`${baseApiUrl}setScholarLink`, {
      userid: userId,
      scholar_link: scholarLink,
      domain: domain,
    });
    return response.data; // { message, response: "true" | "false" }
  } catch (error) {
    console.error("Error setting Google Scholar link:", error);
    return null;
  }
};

export const getNotApprovedMemberPublications = async (domain, userId) => {
  try {
    const response = await axios.get(
      `${baseApiUrl}getNotApprovedMemberPublications?domain=${domain}&user_id=${userId}`
    );
    return response.data.publications || []; // Or handle error if response.response === "false"
  } catch (error) {
    console.error("Error getting not-approved member publications:", error);
    return [];
  }
};
