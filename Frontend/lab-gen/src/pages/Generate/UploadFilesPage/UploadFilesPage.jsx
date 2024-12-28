import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate instead of useHistory

const UploadFilesPage = () => {
  const [files, setFiles] = useState({});
  const navigate = useNavigate(); // Use useNavigate hook

  const handleFileChange = (e, component) => {
    const file = e.target.files[0];
    setFiles((prev) => ({ ...prev, [component]: file }));
  };

  const handleGenerateClick = () => {
    if (Object.keys(files).length === 0) {
      alert('Please upload all required files!');
      return;
    }
    navigate('/generate-website'); // Use navigate to go to the next page
  };

  const handleBack = () => {
    navigate('/choose-components'); // Use navigate to go back
  };

  return (
    <div>
      <h2>Upload Files for Each Component</h2>
      {['Header', 'Footer', 'Sidebar'].map((component) => (
        <div key={component}>
          <h3>Upload {component} File</h3>
          <input
            type="file"
            onChange={(e) => handleFileChange(e, component)}
          />
        </div>
      ))}
      <button onClick={handleBack}>Back</button>
      <button onClick={handleGenerateClick}>Generate Website</button>
    </div>
  );
};

export default UploadFilesPage;
