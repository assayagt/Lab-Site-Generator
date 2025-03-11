import React, { useState, useContext } from "react";
import "./AboutUs.css";
import { useEditMode } from "../../Context/EditModeContext";

function AboutUs(props) {
  const { editMode } = useEditMode(); // Get edit mode state
  const [aboutUsText, setAboutUsText] = useState(props.info || "");
  const handleSave = () => {
    // sessionStorage.setItem('AboutUs', aboutUsText);
    // alert("About Us updated!");
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
