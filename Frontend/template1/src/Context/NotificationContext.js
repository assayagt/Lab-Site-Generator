import React, { createContext, useState, useEffect } from "react";
import { io } from "socket.io-client";

export const NotificationContext = createContext();

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([]);
  const [hasNewNotifications, setHasNewNotifications] = useState(false);
  const socket = io("http://localhost:5000/socket.io/",
   {transports: ["websocket", "polling"],}
  );
  useEffect(() => {
    
    
    
      socket.on("registration-notification", () => {
        setHasNewNotifications(true);
        console.log("harray");
      });
      socket.on("connect", () => {
        console.log("harray");
      });

    //   socket.on("connect_error", (error) => {
    //     console.error("Socket.IO connection error. Retrying in 2 seconds...", error);
    //     //setTimeout(connectSocket, 2000);
    //   });

    //   socket.on("disconnect", (reason) => {
    //     console.log("Socket.IO disconnected:", reason);
    //   });

      // Clean up connection on unmount
      return () => {
        socket.off("registration-notification");
        
      };

  }, []); // Run only on component mount

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
