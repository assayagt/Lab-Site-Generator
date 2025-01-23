import React, { createContext, useState, useEffect } from "react";

export const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [hasNewNotifications, setHasNewNotifications] = useState(false);

  useEffect(() => {
    // Only create WebSocket connection once
    const socket = new WebSocket("ws://localhost:5000/ws/notifications");

    // Handle WebSocket open event
    socket.onopen = () => {
      console.log("WebSocket connected");
    };

    // Handle WebSocket message event
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "registration-notification") {
          setNotifications((prev) => [...prev, data]);
          setHasNewNotifications(true);
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    // Handle WebSocket error event
    socket.onerror = (error) => {
      console.log("WebSocket error:", error);
    };

    // Handle WebSocket close event
    socket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    // Cleanup WebSocket on component unmount
    return () => {
      //socket.close();
      console.log("WebSocket closed");
    };
  }, []); // The empty dependency array ensures this effect only runs once when the component mounts

  // Mark notifications as read
  const markNotificationsAsRead = () => {
    setHasNewNotifications(false);
  };

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        hasNewNotifications,
        markNotificationsAsRead,
      }}
    >
      {children}
    </NotificationContext.Provider>
  );
};