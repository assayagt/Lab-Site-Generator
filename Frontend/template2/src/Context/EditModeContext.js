import React, { createContext, useState, useContext } from "react";

const EditModeContext = createContext();

export const EditModeProvider = ({ children }) => {
  const [editMode, setEditMode] = useState(sessionStorage.getItem("editMode") === "true");

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

export const useEditMode = () => useContext(EditModeContext); 