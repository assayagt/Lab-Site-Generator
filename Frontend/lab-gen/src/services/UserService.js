import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";

export const SendLogin = async(email,sid) => {
  let data;
  return axios
    .post(`${baseApiUrl}Login`, {
      email:email,
      user_id: sid,
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


export const SendLogout = async (
    
  ) => {
    let data;
    const sid = sessionStorage.getItem("sid");
    try {
      const response = await axios.post(`${baseApiUrl}Logout`, {
        user_id: sid,
      });
      data =  response.data;
    } catch (err) {
      console.error("Error sending to signup" + err);
    }
    return data;
  };

  export const EnterSystem = async (
    
  ) => {
    let data;
    await axios
        .get(`${baseApiUrl}enterGeneratorSystem`)
        .then((resp) => {
            data = resp.data.user_id;
            return data;
        })
        .catch((err) => console.log(err.message));
    return data;

  };
  


