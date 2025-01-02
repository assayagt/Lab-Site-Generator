import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";

export const SendLogin = (email) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  console.log(sid)
  return axios
    .post(`${baseApiUrl}Login`, {
      email:email,
      user_id: sid,
    })
    .then((response) => {
      data = response.data;
      console.log(data);
      return data; // Return the data after the promise resolves
    })
    .catch((err) => {
      console.error("Error sending to login: " + err); // Handle error
      return null; // Return null or handle error data as needed
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
      console.log(data);
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
            data = resp.data;
            console.log(data);
        })
        .catch((err) => console.log(err.message));
    return data;

  };
  




// export const SendSignupVerification = async (email, verificationCode) => {
//   try {
//     const response = await axios.post(`${baseApiUrl}Verification`, {
//       email: email,
//       verification_code: verificationCode,
//     });
//     return response.data;
//   } catch (err) {
//     console.error("Error sending singup verification");
//   }
// };
