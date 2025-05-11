import React, { useState, useContext, useEffect } from "react";
import "./AboutUs2.css";
import { useEditMode } from "../../Context/EditModeContext";
import { setSiteAboutUsByManager } from "../../services/websiteService";
import SuccessPopup from "../PopUp/SuccessPopup";
import ErrorPopup from "../PopUp/ErrorPopup";
import { useWebsite } from "../../Context/WebsiteContext";

function AboutUs(props) {
  const { editMode } = useEditMode();
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [saveButtonText, setSaveButtonText] = useState("Save");
  const [popupMessage, setPopupMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const { websiteData, setWebsite } = useWebsite();
  const [aboutUsText, setAboutUsText] = useState(websiteData.about_us || "");
  useEffect(() => {
    if (popupMessage || errorMessage) {
      const timer = setTimeout(() => {
        setPopupMessage("");
        setErrorMessage("");
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [popupMessage, errorMessage]);

  const handleSave = async () => {
    const userId = sessionStorage.getItem("sid");
    const domain = sessionStorage.getItem("domain");
    const response = await setSiteAboutUsByManager(userId, domain, aboutUsText);
    if (response?.response === "true") {
      setPopupMessage("Changes saved successfully!");
      setSaveButtonText("Saved");
      setHasUnsavedChanges(false);
      setWebsite({ about_us: aboutUsText });
      // window.location.reload();
    } else {
      setErrorMessage("An error occurred while saving.");
      setAboutUsText(websiteData.about_us);
    }
  };

  const handleChange = (e) => {
    setAboutUsText(e.target.value);
    setHasUnsavedChanges(true);
    setSaveButtonText("Save");
  };

  return (
    <div className="AboutUsComponent">
      {/* <div className="aboutUsTitle">About Us</div> */}
      {editMode ? (
        <div className="editModeContainer">
          <textarea
            className="aboutUsTextarea"
            value={aboutUsText}
            onChange={handleChange}
          />
          <button
            className="saveButton"
            onClick={handleSave}
            disabled={!hasUnsavedChanges}
          >
            {saveButtonText}
          </button>
        </div>
      ) : (
        <div className="aboutUsParagraph">{aboutUsText}</div>
      )}
      {popupMessage && (
        <SuccessPopup
          message={popupMessage}
          onClose={() => setPopupMessage("")}
        />
      )}
      {errorMessage && (
        <ErrorPopup
          message={errorMessage}
          onClose={() => setErrorMessage("")}
        />
      )}
    </div>
  );
}

export default AboutUs;
