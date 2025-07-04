import axios from "axios";

import { baseApiUrl } from "./BaseUrl"; // Ensure the path is correct relative to this file

export const changeComponents = async (domain, components) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  return axios
    .post(`${baseApiUrl}chooseComponents`, {
      user_id: sid,
      components: components.join(", "),
      domain: domain,
    })
    .then((response) => {
      data = response.data;
      return data;
    })
    .catch((err) => {
      console.error("Error sending to login: " + err);
      return null;
    });
};

export const changeDomain = async (oldDomain, domain) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  return axios
    .post(`${baseApiUrl}chooseDomain`, {
      user_id: sid,
      old_domain: oldDomain,
      domain: domain,
    })
    .then((response) => {
      data = response.data;

      return data;
    })
    .catch((err) => {
      console.error("Error sending to login: " + err);
      return null;
    });
};

export const changeName = async (domain, name) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  return axios
    .post(`${baseApiUrl}chooseName`, {
      user_id: sid,
      website_name: name,
      domain: domain,
    })
    .then((response) => {
      data = response.data;

      return data;
    })
    .catch((err) => {
      console.error("Error sending to login: " + err);
      return null;
    });
};

export const createCustomSite = async (domain, name, components, template) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  return axios
    .post(`${baseApiUrl}startCustomSite`, {
      user_id: sid,
      website_name: name,
      domain: domain,
      components: components.join(", "),
      template: template,
    })
    .then((response) => {
      data = response.data;
      return data;
    })
    .catch((err) => {
      console.error("Error creating site: " + err);
      return null;
    });
};

export const changeTemplate = async (domain, template) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  return axios
    .post(`${baseApiUrl}chooseTemplate`, {
      user_id: sid,
      domain: domain,
      template: template,
    })
    .then((response) => {
      data = response.data;
      return data;
    })
    .catch((err) => {
      console.error("Error templte: " + err);
      return null;
    });
};

export const getAllLabManagers = async (domain) => {
  try {
    let data;
    const response = await axios.get(
      `${baseApiUrl}getAllLabManagers?domain=${domain}`
    );
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
    return response.data.alumni;
  } catch (error) {
    console.error("Error getting all alumni:", error);
    return [];
  }
};

export const createNewSiteManager = async (
  nominatorManagerUserId,
  nominatedManagerEmail,
  domain
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}CreateNewSiteManagerFromGenerator`,
      {
        nominator_manager_userId: nominatorManagerUserId,
        nominated_manager_email: nominatedManagerEmail,
        domain: domain,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error creating new site manager:", error);
    //alert('An error occurred while adding the site manager.');
  }
};

export const addAlumni = async (
  nominatorManagerUserId,
  nominatedManagerEmail,
  domain
) => {
  try {
    const response = await axios.post(`${baseApiUrl}AddAlumniFromGenerator`, {
      manager_userId: nominatorManagerUserId,
      email_toSetAlumni: nominatedManagerEmail,
      domain: domain,
    });
    return response.data;
  } catch (error) {
    console.error("Error creating new ALUMNI:", error);
    //alert('An error occurred while adding the aluni.');
  }
};

export const removeSiteManager = async (
  nominatorManagerUserId,
  managerToRemoveEmail,
  domain
) => {
  try {
    const response = await axios.post(`${baseApiUrl}removeSiteManager`, {
      nominator_manager_userId: nominatorManagerUserId,
      manager_toRemove_email: managerToRemoveEmail,
      domain: domain,
    });
    return response.data;
  } catch (error) {
    console.error("Error removing site manager:", error);
    //alert('An error occurred while removing the site manager.');
  }
};

export const addLabMember = async (
  managerUserId,
  emailToRegister,
  labMemberFullName,
  labMemberDegree,
  domain
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}addLabMemberFromGenerator`,
      {
        manager_userId: managerUserId,
        email_to_register: emailToRegister,
        lab_member_fullName: labMemberFullName,
        lab_member_degree: labMemberDegree,
        domain: domain,
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error adding lab member:", error);
    //alert('An error occurred while adding the lab member.');
  }
};

export const setSiteAboutUs = async (userId, domain, aboutUs) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}setSiteAboutUsByManagerFromGenerator`,
      {
        user_id: userId,
        domain: domain,
        about_us: aboutUs,
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error setting About Us:", error);
    //alert('An error occurred while setting the About Us section.');
  }
};

export const setSiteContactInfo = async (
  userId,
  domain,
  labAddress,
  labMail,
  labPhoneNum
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}setSiteContactInfoByManagerFromGenerator`,
      {
        user_id: userId,
        domain: domain,
        lab_address: labAddress,
        lab_mail: labMail,
        lab_phone_num: labPhoneNum,
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error setting contact info:", error);
    //alert('An error occurred while setting the contact information.');
  }
};

export const saveLogo = async (userId, domain) => {
  try {
    const response = await axios.post(`${baseApiUrl}ChangeSiteLogoByManager`, {
      user_id: userId,
      domain: domain,
    });

    return response.data;
  } catch (error) {
    //alert('Error saving logo: ' + error.message);
  }
};

export const saveHomePicture = async (userId, domain) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}ChangeSiteHomePictureByManager`,
      {
        user_id: userId, // User ID
        domain: domain,
      }
    );

    return response.data;
  } catch (error) {
    // alert('Error saving home picture: ' + error.message);
  }
};

export const generate = async (
  domain,
  aboutUsContent,
  email,
  address,
  phoneNumber,
  participants
) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}generateWebsite`,
      {
        domain: domain,
        about_us: aboutUsContent,
        lab_address: address,
        lab_mail: email,
        lab_phone_num: phoneNumber,
        participants: participants.map((p) => ({
          fullName: p.fullName,
          email: p.email,
          degree: p.degree,
          isLabManager: p.isLabManager,
          alumni: p.alumni || false,
        })),
      },
      {
        headers: { "Content-Type": "application/json" },
      }
    );

    const data = response.data;
    return data;
  } catch (error) {
    //alert("Error: " + (error.response?.data?.message || error.message));
  }
};

export const removeAlumni = async (managerUserId, alumniEmail, domain) => {
  try {
    const response = await axios.post(
      `${baseApiUrl}RemoveAlumniFromGenerator`,
      {
        manager_userId: managerUserId,
        email_toRemoveAlumni: alumniEmail,
        domain: domain,
      }
    );

    return response.data;
  } catch (error) {
    console.error("Error removing alumni:", error);
    return null;
  }
};

export const deleteGalleryImage = async (userId, domain, imageName) => {
  try {
    const response = await axios.post(`${baseApiUrl}deleteGalleryImage`, {
      user_id: userId,
      image_name: imageName,
      domain: domain,
    });

    return response.data;
  } catch (error) {
    console.error("Error deleting gallery image:", error);
    return { response: "false", error: error.message };
  }
};
