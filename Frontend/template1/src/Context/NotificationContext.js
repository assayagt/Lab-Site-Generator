import React, { createContext, useState, useEffect } from "react";

export const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [hasNewNotifications, setHasNewNotifications] = useState(false);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:5000/ws/notifications"); 

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "new_notification") {
        setNotifications((prev) => [...prev, data]); 
        setHasNewNotifications(true);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      ws.close(); 
    };
  }, []);

  const markNotificationsAsRead = () => {
    setHasNewNotifications(false);
  };

  return (
    <NotificationContext.Provider
      value={{ notifications, hasNewNotifications, markNotificationsAsRead }}
    >
      {children}
    </NotificationContext.Provider>
  );
};
