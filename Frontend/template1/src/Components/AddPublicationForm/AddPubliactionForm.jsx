import React, { useState } from 'react';
import { addPublication } from '../../services/websiteService';

const AddPublicationForm = () => {

  const [publication, setPublication] = useState('');
  const [githubLink, setGithubLink] = useState('');
  const [presentationLink, setPresentationLink] = useState('');
  const [videoLink, setVideoLink] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (publication) {
      const domain = sessionStorage.getItem('domain');
      const data = await addPublication(publication, domain, githubLink, videoLink, presentationLink);
      console.log(data);
      //if(data.response === "true"){
        setPublication('');
        setGithubLink('');
        setPresentationLink('');
        setVideoLink('');
      //}
     // else{
       // alert(data.data);
      //}

      
    } else {
      alert('Publication Link is required.');
    }
  };

  return (
    <div className="upload-publication-section">
      <h3>Add New Publication</h3>
      <form className="upload-publication-form" onSubmit={handleSubmit}>
        <label>
          <strong>publication-link:</strong>
          <input
            type="text"
            value={publication}
            onChange={(e) => setPublication(e.target.value)}
            placeholder="Publication link"
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
