import axios from "axios";

const baseApiUrl = "http://127.0.0.1:5000/api/";

export const SendLogin = async (email, sid, domain) => {
  let data;
  return axios
    .post(`${baseApiUrl}loginWebsite`, {
      domain: domain,
      email: email,
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

export const SendLogout = async () => {
  let data;
  const sid = sessionStorage.getItem("sid");
  try {
    const response = await axios.post(`${baseApiUrl}logoutWebsite`, {
      user_id: sid,
      domain: sessionStorage.getItem("domain"),
    });
    data = response.data;
    console.log(data);
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
      `http://127.0.0.1:5000/api/getAllMembersNotifications?user_id=${sessionStorage.getItem(
        "sid"
      )}&domain=${sessionStorage.getItem("domain")}`
    );
    console.log(data.data);
    if (data.data.response === "true") {
      return data.data.notifications || [];
    }
    return [];
  } catch (error) {
    console.error("Failed to fetch notifications:", error);
    return [];
  }
};
