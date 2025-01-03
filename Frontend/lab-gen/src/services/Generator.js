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
      components:components,
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