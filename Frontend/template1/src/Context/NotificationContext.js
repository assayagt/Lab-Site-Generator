import React, { createContext, useState, useEffect } from "react";
import { io } from "socket.io-client";
import { useAuth } from "../Context/AuthContext";

export const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [hasNewNotifications, setHasNewNotifications] = useState(false);
  const { user } = useAuth(); // get user email
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = io("http://localhost:5000", {
      transports: ["websocket", "polling"],
    });

    newSocket.on("connect", () => {
      console.log("Connected to WebSocket server.");
    });

    newSocket.on("registration-notification", (data) => {
      console.log("Received notification:", data);

      setNotifications((prev) => [...prev, data]);
      if (notifications.length !== 0) {
        setHasNewNotifications(true);
      }
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
    if (socket && user?.email) {
      console.log("Registering user to socket:", user.email);
      socket.emit("register_manager", { email: user.email });
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
