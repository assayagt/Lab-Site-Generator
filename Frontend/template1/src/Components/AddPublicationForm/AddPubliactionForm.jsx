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
        <div className="coolinput">
          <label htmlFor="input" className="text">Publication Link:</label>
          <input
            type="text"
            placeholder="publication link"
            name="input"
            className="input"
            value={publication}
            onChange={(e) => setPublication(e.target.value)}
          />
        </div>
        <div className="coolinput">
          <label htmlFor="input" className="text">GitHub Link:</label>
          <input
            type="text"
            placeholder="github link"
            name="input"
            className="input"
            value={githubLink}
            onChange={(e) => setGithubLink(e.target.value)}
          />
        </div>
        <div className="coolinput">
          <label htmlFor="input" className="text">Presentation Link:</label>
          <input
            type="text"
            placeholder="presentation link"
            name="input"
            className="input"
            value={presentationLink}
            onChange={(e) => setPresentationLink(e.target.value)}
          />
        </div>
        <div className="coolinput">
          <label htmlFor="input" className="text">Video Link:</label>
          <input
            type="text"
            placeholder="video link"
            name="input"
            className="input"
            value={videoLink}
            onChange={(e) => setVideoLink(e.target.value)}
          />
        </div>
        <button type="submit">Add Publication</button>
      </form>
    </div>
  );
};

export default AddPublicationForm;
