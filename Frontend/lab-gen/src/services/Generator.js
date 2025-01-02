import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";

export const changeComponents= (domain, components) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}`, {
      
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


export const changeDomain= (oldDomain, domain) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}`, {
      
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

export const changeName= (domain, name) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}`, {
      
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

export const createCustomSite= (domain, name) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}startCustomSite`, {
      user_id: sid,
      website_name: name,
      domain:domain,
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


export const changeTemplate= (domain, template) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}`, {
      
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