import axios from "axios";

import { baseApiUrl } from "./BaseUrl"; // Ensure the path is correct relative to this file

export const SendLogin = async (token, sid, domain) => {
  return axios
    .post(`${baseApiUrl}loginWebsite`, {
      domain: domain,
      google_token: token,
      user_id: sid,
    })
    .then((response) => response.data)
    .catch((err) => {
      console.error("Error sending to login: " + err);
      return null;
    });
};

export const SendLogout = async () => {
  let data;
  const sid = sessionStorage.getItem("sid");
  try {
    const response = await axios.post(`${baseApiUrl}logoutWebsite`, {
      user_id: sid,
      domain: sessionStorage.getItem("domain"),
    });
    data = response.data;
  } catch (err) {
    console.error("Error sending to signup" + err);
  }
  return data;
};

export const EnterSystem = async () => {
  let data;
  await axios
    .get(
      `${baseApiUrl}enterLabWebsite?domain=${sessionStorage.getItem("domain")}`
    )
    .then((resp) => {
      data = resp.data.user_id;
      return data;
    })
    .catch((err) => console.log(err.message));
  return data;
};

export const fetchUserNotifications = async (email) => {
  try {
    const data = await axios.get(
      `${baseApiUrl}getAllMembersNotifications?user_id=${sessionStorage.getItem(
        "sid"
      )}&domain=${sessionStorage.getItem("domain")}`
    );
    if (data.data.response === "true") {
      return data.data.notifications || [];
    }
    return [];
  } catch (error) {
    console.error("Failed to fetch notifications:", error);
    return [];
  }
};

export const uploadProfilePicture = async (file, domain) => {
  const formData = new FormData();
  formData.append("profile_picture", file);
  formData.append("user_id", sessionStorage.getItem("sid"));
  formData.append("domain", domain);

  try {
    const response = await axios.post(
      `${baseApiUrl}uploadProfilePicture`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error uploading profile picture:", error);
    throw error;
}
};
