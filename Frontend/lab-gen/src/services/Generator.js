import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";

export const changeComponents= async (domain, components) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(domain);
  return axios
    .post(`${baseApiUrl}chooseComponents`, {
      user_id: sid,
      components: components,
      domain:domain, 
    
    })
    .then((response) => {
      data = response.data;
      console.log(data);
      return data; 
    })
    .catch((err) => {
      console.error("Error sending to login: " + err); 
      return null;
    });
};


export const changeDomain= async(oldDomain, domain) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}chooseDomain`, {
      user_id: sid,
      old_domain: oldDomain,
      domain : domain
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

export const changeName= async(domain, name) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}chooseName`, {
      user_id: sid,
      website_name: name,
      domain : domain
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

export const createCustomSite= async(domain, name, components, template) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}startCustomSite`, {
      user_id: sid,
      website_name: name,
      domain:domain,
      components:components.join(", "),
      template:template,
    })
    .then((response) => {
      data = response.data;
      console.log(data);
      return data; 
    })
    .catch((err) => {
      console.error("Error creating site: " + err); 
      return null;
    });
};


export const changeTemplate= async(domain, template) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}chooseTemplate`, {
      user_id: sid,
      domain:domain,
      template:template,
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


export const getAllLabManagers = async (domain) => {
  try {
      let data;
      const response = await axios.get(`${baseApiUrl}getAllLabManagers?domain=${domain}`);
      console.log(response.data);
      return response.data.managers;
  } catch (error) {
      console.error("Error getting all lab managers:", error);
      return [];
  }
};

export const getAllLabMembers = async (domain) => {
  try {
      const response = await axios.get(`${baseApiUrl}getAllLabMembers?domain=${domain}`);
      console.log(response.data);
      return response.data.members;
  } catch (error) {
      console.error("Error getting all lab members:", error);
      return [];
  }
};


export const getAllAlumni = async (domain) => {
  try {
      const response = await axios.get(`${baseApiUrl}getAllAlumni?domain=${domain}`);
      console.log(response.data);
      return response.data.alumni;
  } catch (error) {
      console.error("Error getting all alumni:", error);
      return [];
  }
};


export const createNewSiteManager = async (nominatorManagerUserId, nominatedManagerEmail, domain) => {
  try {
    const response = await axios.post(`${baseApiUrl}CreateNewSiteManagerFromGenerator`, {
      nominator_manager_userId: nominatorManagerUserId,
      nominated_manager_email: nominatedManagerEmail,
      domain: domain,
    });
  console.log(response.data);
      return response.data;
  } catch (error) {
    console.error('Error creating new site manager:', error);
    alert('An error occurred while adding the site manager.');
  }
};

export const removeSiteManager = async (nominatorManagerUserId, managerToRemoveEmail, domain) => {
  try {
    const response = await axios.post(`${baseApiUrl}removeSiteManager`, {
      nominator_manager_userId: nominatorManagerUserId,
      manager_toRemove_email: managerToRemoveEmail,
      domain: domain,
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error removing site manager:', error);
    alert('An error occurred while removing the site manager.');
  }
};



export const addLabMember = async (managerUserId, emailToRegister, labMemberFullName, labMemberDegree, domain) => {
  try {
    const response = await axios.post(`${baseApiUrl}addLabMemberFromGenerator`, {
      manager_userId: managerUserId,
      email_to_register: emailToRegister,
      lab_member_fullName: labMemberFullName,
      lab_member_degree: labMemberDegree,
      domain: domain
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error adding lab member:', error);
    alert('An error occurred while adding the lab member.');
  }
};

export const setSiteAboutUs = async (userId, domain, aboutUs) => {
  try {
    const response = await axios.post(`${baseApiUrl}setSiteAboutUsByManagerFromGenerator`, {
      user_id: userId,
      domain: domain,
      about_us: aboutUs,
    });

    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error setting About Us:', error);
    alert('An error occurred while setting the About Us section.');
  }
};


export const setSiteContactInfo = async (userId, domain, labAddress, labMail, labPhoneNum) => {
  try {
    const response = await axios.post(`${baseApiUrl}setSiteContactInfoByManagerFromGenerator`, {
      user_id: userId,
      domain: domain,
      lab_address: labAddress,
      lab_mail: labMail,
      lab_phone_num: labPhoneNum,
    });

    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error setting contact info:', error);
    alert('An error occurred while setting the contact information.');
  }
};