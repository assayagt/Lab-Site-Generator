import React, { useState } from "react";
import { addPublication } from "../../services/websiteService";
import "./AddPublicationFrom.css";

const AddPublicationForm = ({ onSuccess }) => {
  const [publication, setPublication] = useState("");
  const [githubLink, setGithubLink] = useState("");
  const [presentationLink, setPresentationLink] = useState("");
  const [videoLink, setVideoLink] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

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

      if (response.response === "true") {
        setPublication("");
        setGithubLink("");
        setPresentationLink("");
        setVideoLink("");
        setError(null);

        if (onSuccess) {
          onSuccess();
        }
      } else {
        setError("Failed to add publication. " + response.message);
      }
    } catch (error) {
      setError("An error occurred while adding the publication.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="publication-form-container">
      {error && <div className="error-alert">{error}</div>}

      <form className="publication-form" onSubmit={handleSubmit}>
        <div className="form-field">
          <label className="form-field__label">
            Publication Link <span className="required">*</span>
          </label>
          <input
            type="url"
            placeholder="https://scholar.google.com/xxxx/xxxxx"
            className="form-field__input"
            value={publication}
            onChange={(e) => setPublication(e.target.value)}
            required
          />
        </div>

        <div className="form-field">
          <label className="form-field__label">GitHub Repository</label>
          <input
            type="url"
            placeholder="https://github.com/username/repo"
            className="form-field__input"
            value={githubLink}
            onChange={(e) => setGithubLink(e.target.value)}
          />
        </div>

        <div className="form-field">
          <label className="form-field__label">Presentation</label>
          <input
            type="url"
            placeholder="https://drive.google.com/drive/..."
            className="form-field__input"
            value={presentationLink}
            onChange={(e) => setPresentationLink(e.target.value)}
          />
        </div>

        <div className="form-field">
          <label className="form-field__label">Video</label>
          <input
            type="url"
            placeholder="youtube/google drive video"
            className="form-field__input"
            value={videoLink}
            onChange={(e) => setVideoLink(e.target.value)}
          />
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="button button--primary"
            disabled={loading}
          >
            {loading ? "Adding..." : "Add Publication"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddPublicationForm;
