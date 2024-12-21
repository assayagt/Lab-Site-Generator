// import React, { useState } from 'react';
// import { useHistory } from 'react-router-dom';

// const UploadFilesPage = () => {
//   const [files, setFiles] = useState({});
//   const history = useHistory();

//   const handleFileChange = (e, component) => {
//     const file = e.target.files[0];
//     setFiles((prev) => ({ ...prev, [component]: file }));
//   };

//   const handleGenerateClick = () => {
//     if (Object.keys(files).length === 0) {
//       alert('Please upload all required files!');
//       return;
//     }
//     history.push('/generate-website');
//   };

//   const handleBack = () => {
//     history.push('/choose-components');
//   };

//   return (
//     <div>
//       <h2>Upload Files for Each Component</h2>
//       {['Header', 'Footer', 'Sidebar'].map((component) => (
//         <div key={component}>
//           <h3>Upload {component} File</h3>
//           <input
//             type="file"
//             onChange={(e) => handleFileChange(e, component)}
//           />
//         </div>
//       ))}
//       <button onClick={handleBack}>Back</button>
//       <button onClick={handleGenerateClick}>Generate Website</button>
//     </div>
//   );
// };

// export default UploadFilesPage;
