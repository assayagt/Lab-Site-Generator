import axios from "axios";

import { baseApiUrl } from "./BaseUrl"; // Ensure the path is correct relative to this file

export const SendLogin = async (token, sid) => {
  let data;
  return axios
    .post(`${baseApiUrl}Login`, {
      google_token: token,
      user_id: sid,
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

export const EnterSystem = async () => {
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
