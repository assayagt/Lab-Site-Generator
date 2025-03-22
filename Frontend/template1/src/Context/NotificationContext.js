import React, { createContext, useState, useEffect } from "react";
import { io } from "socket.io-client";

export const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [hasNewNotifications, setHasNewNotifications] = useState(false);

  useEffect(() => {
    const socket = io("http://localhost:5000", {
      transports: ["websocket", "polling"],
    });

    socket.on("connect", () => {
      console.log("Connected to WebSocket server.");
    });

    socket.on("registration-notification", (data) => {
      console.log("Received notification:", data);
      setHasNewNotifications(true);
      setNotifications((prev) => [...prev, data]);
    });

    socket.on("disconnect", () => {
      console.log("Disconnected from WebSocket server.");
    });

    // Clean up connection on unmount
    return () => {
      socket.off("registration-notification");
      socket.disconnect();
    };
  }, []); // Run only on component mount

  const markNotificationAsRead = (id) => {
    const updatedNotifications = notifications.filter(
      (notif) => notif.id !== id
    );
    setNotifications(updatedNotifications);
    // localStorage.setItem("notifications", JSON.stringify(updatedNotifications));

    if (updatedNotifications.length === 0) {
      setHasNewNotifications(false);
    }
  };
  const updateNotifications = (newNotifs) => {
    setNotifications(newNotifs);
    setHasNewNotifications(true);
  };

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        hasNewNotifications,
        markNotificationAsRead,
        updateNotifications,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};
