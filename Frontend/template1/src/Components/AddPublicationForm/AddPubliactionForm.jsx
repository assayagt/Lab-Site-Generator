import React, { useState } from "react";
import { addPublication } from "../../services/websiteService";
import "./AddPublicationFrom.css";

const AddPublicationForm = ({ onSuccess }) => {
  const [publication, setPublication] = useState("");
  const [githubLink, setGithubLink] = useState("");
  const [presentationLink, setPresentationLink] = useState("");
  const [videoLink, setVideoLink] = useState("");
  const [error, setError] = useState(null); // Error message state
  const [loading, setLoading] = useState(false); // Loading state

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    if (!publication.trim()) {
      setError("Publication link is required.");
      setLoading(false);
      return;
    }

    try {
      const domain = sessionStorage.getItem("domain");
      const response = await addPublication(
        publication,
        domain,
        githubLink,
        videoLink,
        presentationLink
      );
      console.log(response);
      if (response.response === "true") {
        // Reset fields on success
        setPublication("");
        setGithubLink("");
        setPresentationLink("");
        setVideoLink("");
        setError(null);

        // Close the form if onSuccess function is provided
        if (onSuccess) {
          onSuccess();
        }
      } else {
        setError(response.data || "Failed to add publication. Try again.");
      }
    } catch (error) {
      setError("An error occurred while adding the publication.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-publication-section">
      <h3>Add New Publication</h3>
      {error && <p className="error-message">{error}</p>}{" "}
      {/* Show error message if exists */}
      <form className="upload-publication-form" onSubmit={handleSubmit}>
        <div className="coolinput">
          <label className="text">Publication Link:</label>
          <input
            type="text"
            placeholder="Publication link"
            className="input"
            value={publication}
            onChange={(e) => setPublication(e.target.value)}
          />
        </div>

        <div className="coolinput">
          <label className="text">GitHub Link:</label>
          <input
            type="text"
            placeholder="GitHub link"
            className="input"
            value={githubLink}
            onChange={(e) => setGithubLink(e.target.value)}
          />
        </div>

        <div className="coolinput">
          <label className="text">Presentation Link:</label>
          <input
            type="text"
            placeholder="Presentation link"
            className="input"
            value={presentationLink}
            onChange={(e) => setPresentationLink(e.target.value)}
          />
        </div>

        <div className="coolinput">
          <label className="text">Video Link:</label>
          <input
            type="text"
            placeholder="Video link"
            className="input"
            value={videoLink}
            onChange={(e) => setVideoLink(e.target.value)}
          />
        </div>

        <button type="submit" className="submit-pub" disabled={loading}>
          {loading ? "Adding..." : "Add Publication"}
        </button>
      </form>
    </div>
  );
};

export default AddPublicationForm;
