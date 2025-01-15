import React, { useState } from 'react';

const AddPublicationForm = () => {
  const [title, setTitle] = useState('');
  const [publicationYear, setPublicationYear] = useState('');
  const [githubLink, setGithubLink] = useState('');
  const [presentationLink, setPresentationLink] = useState('');
  const [videoLink, setVideoLink] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (title && publicationYear) {
      setTitle('');
      setPublicationYear('');
      setGithubLink('');
      setPresentationLink('');
      setVideoLink('');
    } else {
      alert('Title and Publication Year are required.');
    }
  };

  return (
    <div className="upload-publication-section">
      <h3>Add New Publication</h3>
      <form className="upload-publication-form" onSubmit={handleSubmit}>
        <label>
          <strong>Title:</strong>
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Publication title"
            required
          />
        </label>
        <label>
          <strong>Year:</strong>
          <input
            type="number"
            value={publicationYear}
            onChange={(e) => setPublicationYear(e.target.value)}
            placeholder="Year"
            required
          />
        </label>
        <label>
          <strong>GitHub Link:</strong>
          <input
            type="url"
            value={githubLink}
            onChange={(e) => setGithubLink(e.target.value)}
            placeholder="GitHub URL"
          />
        </label>
        <label>
          <strong>Presentation Link:</strong>
          <input
            type="url"
            value={presentationLink}
            onChange={(e) => setPresentationLink(e.target.value)}
            placeholder="Presentation URL"
          />
        </label>
        <label>
          <strong>Video Link:</strong>
          <input
            type="url"
            value={videoLink}
            onChange={(e) => setVideoLink(e.target.value)}
            placeholder="Video URL"
          />
        </label>
        <button type="submit">Add Publication</button>
      </form>
    </div>
  );
};

export default AddPublicationForm;
