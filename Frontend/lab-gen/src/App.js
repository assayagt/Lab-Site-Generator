import React, { useState } from 'react';
import './App.css';

function App() {
  const [siteData, setSiteData] = useState({
    title: '',
    description: '',
    components: [],
  });

  const handleChange = (e) => {
    setSiteData({ ...siteData, [e.target.name]: e.target.value });
  };

  const handleAddComponent = () => {
    const newComponent = document.getElementById('newComponent').value;
    setSiteData((prevState) => ({
      ...prevState,
      components: [...prevState.components, newComponent],
    }));
    document.getElementById('newComponent').value = '';
  };

  const handleGenerateSite = async () => {
    try {
      const response = await fetch('http://localhost:5000/generateWebsite', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(siteData), // Pass the data you want to generate the site
      });
  
      // Check if the response is OK (status code 200)
      if (response.ok) {
        const data = await response.json();
        console.log(data); // Log the response to verify
  
        if (data.websiteLink) {
          // Redirect to the generated website
          window.location.href = `http://localhost:5000${data.websiteLink}`;
        }
      } else {
        console.error('Error generating website:', response.statusText);
      }
    } catch (error) {
      console.error('Failed to fetch:', error);
    }
  };

  return (
    <div className="App">
      <h1>Website Generator</h1>
      <div>
        <label>Website Title: </label>
        <input
          type="text"
          name="title"
          value={siteData.title}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>Description: </label>
        <textarea
          name="description"
          value={siteData.description}
          onChange={handleChange}
        />
      </div>
      <div>
        <label>New Component (Text): </label>
        <input type="text" id="newComponent" />
        <button onClick={handleAddComponent}>Add Component</button>
      </div>
      <div>
        <h3>Components:</h3>
        <ul>
          {siteData.components.map((component, index) => (
            <li key={index}>{component}</li>
          ))}
        </ul>
      </div>
      <button onClick={handleGenerateSite}>Generate Website</button>
    </div>
  );
}

export default App;
