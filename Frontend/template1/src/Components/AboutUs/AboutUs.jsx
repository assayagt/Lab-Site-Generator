import React, { useState, useContext } from "react";
import "./AboutUs.css";
import { useEditMode } from "../../Context/EditModeContext";
import { setSiteAboutUsByManager } from "../../services/websiteService";

function AboutUs(props) {
  const { editMode } = useEditMode(); // Get edit mode state
  const [aboutUsText, setAboutUsText] = useState(props.info || "");
  const handleSave = async () => {
    const userId = sessionStorage.getItem("sid"); // or props.userId
    const domain = sessionStorage.getItem("domain"); // make sure to pass this in from parent component

    const response = await setSiteAboutUsByManager(userId, domain, aboutUsText);
    if (response?.response === "true") {
    } else {
    }
  };
  return (
    <div className="AboutUsComponent">
      <div className="aboutUsTitle">About Us</div>
      {editMode ? (
        <div className="editModeContainer">
          <textarea
            className="aboutUsTextarea"
            value={aboutUsText}
            onChange={(e) => setAboutUsText(e.target.value)}
          />
          <button className="saveButton" onClick={handleSave}>
            Save
          </button>
        </div>
      ) : (
        <div className="aboutUsParagraph">{aboutUsText}</div>
      )}
      <div></div>
    </div>
  );
}

export default AboutUs;
