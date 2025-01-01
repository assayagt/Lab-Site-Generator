import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";

export const SendLogin = async (
  email,
) => {
  let data;
  const sid = sessionStorage.getItem("sid");
  try {
    const response = await axios.post(`${baseApiUrl}Login`, {
      user_id: sid,
    });
    data = response.data;
  } catch (err) {
    console.error("Error sending to signup" + err);
  }
  return data;
};

export const SendLogout = async (
    
  ) => {
    let data;
    const sid = sessionStorage.getItem("sid");
    try {
      const response = await axios.post(`${baseApiUrl}Login`, {
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
            data = resp.data;
        })
        .catch((err) => console.log(err.message));
    console.log(data);
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
