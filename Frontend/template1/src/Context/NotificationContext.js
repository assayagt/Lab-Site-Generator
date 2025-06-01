import React, { createContext, useState, useEffect } from "react";
import { io } from "socket.io-client";
import { useAuth } from "../Context/AuthContext";
import { socketUrl } from "../services/BaseUrl";

export const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [hasNewNotifications, setHasNewNotifications] = useState(() => {
    const saved = localStorage.getItem("hasNewNotifications");
    return saved ? JSON.parse(saved) : false;
  });

  const { user } = useAuth(); // get user email
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    localStorage.setItem(
      "hasNewNotifications",
      JSON.stringify(hasNewNotifications)
    );
  }, [hasNewNotifications]);

  useEffect(() => {
    const newSocket = io(socketUrl, {
    transports: ["websocket", "polling"],
    });

    newSocket.on("connect", () => {
      console.log("Connected to WebSocket server.");
    });

    newSocket.on("registration-notification", (data) => {
      console.log("Received notification:", data);
      setNotifications((prev) => [...prev, data]);
      setHasNewNotifications(true);
    });

    newSocket.on("final-publication-notification", (data) => {
      console.log("Received notification:", data);
      setNotifications((prev) => [...prev, data]);
      setHasNewNotifications(true);
    });

    newSocket.on("initial-publication-notification", (data) => {
      console.log("Received notification:", data);
      setNotifications((prev) => [...prev, data]);
      setHasNewNotifications(true);
    });

    newSocket.on("disconnect", () => {
      console.log("Disconnected from WebSocket server.");
    });

    setSocket(newSocket);

    return () => {
      newSocket.off("registration-notification");
      newSocket.disconnect();
    };
  }, []);

  useEffect(() => {
    console.log("socket?", socket);
    console.log("user?", user);
    if (socket && user?.email) {
      console.log("Registering user to socket:", user.email);
      socket.emit("register_manager", {
        email: user.email,
        domain: sessionStorage.getItem("domain"),
      });
    }
  }, [socket, user]);

  const markNotificationAsRead = (id) => {
    const updatedNotifications = notifications.filter(
      (notif) => notif.id !== id
    );
    setNotifications(updatedNotifications);

    if (updatedNotifications.length === 0) {
      setHasNewNotifications(false);
    }
  };

  const updateNotifications = (newNotifs) => {
    setNotifications(newNotifs);
    if (newNotifs != null && newNotifs) {
      setHasNewNotifications(true);
    }
  };

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        hasNewNotifications,
        markNotificationAsRead,
        updateNotifications,
        setHasNewNotifications,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};
