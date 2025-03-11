import React, { createContext, useState, useContext } from "react";

// Create Context
const EditModeContext = createContext();

// Create Provider
export const EditModeProvider = ({ children }) => {
  const [editMode, setEditMode] = useState(sessionStorage.getItem("editMode") === "true");

  // Function to toggle edit mode and store in sessionStorage
  const toggleEditMode = () => {
    const newMode = !editMode;
    setEditMode(newMode);
    sessionStorage.setItem("editMode", newMode);
  };

  return (
    <EditModeContext.Provider value={{ editMode, toggleEditMode }}>
      {children}
    </EditModeContext.Provider>
  );
};

// Custom hook to use Edit Mode Context
export const useEditMode = () => useContext(EditModeContext);
