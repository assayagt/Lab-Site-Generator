import React, { useState, useEffect } from 'react';
import './AccountPage.css';
import accountIcon from "../../images/account_avatar.svg";
import cameraIcon from "../../images/camera_icon.svg";
import publicationsData from "../../publications.json";
import searchIcon from "../../images/search_icon.svg";
import AddPublicationForm from '../../Components/AddPublicationForm/AddPubliactionForm';
const AccountPage = () => {
  const [activeSection, setActiveSection] = useState('personal-info'); // Track the active section
  const [notifications, setNotifications] = useState([
    { id: 1, message: 'New publication approval', status: 'pending' },
    { id: 2, message: 'Profile update required', status: 'pending' },
  ]);
  const [publications, setPublications] = useState(publicationsData);
  const [uploadedPhoto, setUploadedPhoto] = useState(accountIcon);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;
  const [searchTerm, setSearchTerm] = useState('');

  const handleSectionChange = (section) => {
    setActiveSection(section);
  };

  const handleApproveNotification = (id) => {
    setNotifications((prev) => prev.filter((notif) => notif.id !== id));
  };

  const handleRejectNotification = (id) => {
    setNotifications((prev) => prev.filter((notif) => notif.id !== id));
  };

  const handleEditPublication = (id) => {
    const newContent = prompt('Edit publication content:');
    if (newContent) {
      setPublications((prev) =>
        prev.map((pub) =>
          pub.id === id ? { ...pub, content: newContent } : pub
        )
      );
    }
  };

  const handleUploadPhoto = () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.onchange = (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          setUploadedPhoto(reader.result);
        };
        reader.readAsDataURL(file);
      }
    };
    fileInput.click();
  };

  const filteredPublications = publications.filter((pub) =>
    pub.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSavePhoto = () => {
    alert('Photo saved successfully!');
  };
  const totalPages = Math.ceil(filteredPublications.length / itemsPerPage);
  const paginatedPublications = filteredPublications.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );


  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div className="account-page">
      <Sidebar activeSection={activeSection} onSectionChange={handleSectionChange} />
      <div className="main-content">
        {activeSection === 'personal-info' && (
          <form id="personal-info" className="personal-info" onSubmit={(e) => { e.preventDefault(); alert('Form Submitted'); }}>
            <h2>Personal Information</h2>
            <div className="info">
              <div className='user-photo-div'>
                <img src={uploadedPhoto} alt="User" className="user-photo" />
                <div className="camera-icon" onClick={handleUploadPhoto}>
                  <img src={cameraIcon} alt="Upload" />
                </div>
                <button className="save-photo" onClick={handleSavePhoto}>Save Photo</button>
              </div>
              <div className="details">
                <label className='detail-bio'>
                  <strong>Bio:</strong>
                  <input className="text-detail" defaultValue="Lorem ipsum dolor sit amet." />
                </label>

                <label className='detail-bio'>
                  <strong>Email:</strong>
                  <div className="text-detail" type="email">user@example.com</div>
                </label>

                <label className='detail-bio'>
                  <strong>Secondary Email:</strong>
                  <input className="text-detail" type="email" defaultValue="secondary@example.com" />
                </label>

                <label className='detail-bio'>
                  <strong>Degree:</strong>
                  <input className="text-detail" type="text" defaultValue="Bachelor of Science" />
                </label>

                <label className='detail-bio'>
                  <strong>LinkedIn:</strong>
                  <input className="text-detail" type="url" defaultValue="linkedin.com/in/username" />
                </label>
              </div>
            </div>
            <button className="save-changes" type="submit">Save Changes</button>
          </form>
        )}
        {activeSection === 'my-publications' && (
          <div id="my-publications" className="my-publications">
            <h2>My Publications</h2>
            <AddPublicationForm/>
            <div className="search-bar">
              <img src={searchIcon} alt="Search" className="search-icon" />
              <input
                type="text"
                placeholder="Search by title"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>

              {paginatedPublications.map((publication) => (
                <div key={publication.id} className='publication-item'>
                  <from className='publication-form'>
                    <strong>{publication.title}</strong>
                    <div>
                      {publication.publication_year}
                    </div>
                    <label className='detail-bio'>
                      <strong>Git-Hub:</strong>
                      <input className="text-detail" type="url" defaultValue="github//" />
                    </label>
                    <label className='detail-bio'>
                      <strong>Presentation:</strong>
                      <input className="text-detail" type="url" defaultValue="github//" />
                    </label>
                    <label className='detail-bio'>
                      <strong>Video:</strong>
                      <input className="text-detail" type="url" defaultValue="youtubr" />
                    </label>
                    <button  className= "save-publications" type="submit">Save Changes</button>
                  </from>
                  
                  
                </div>
              ))}
          <div className="pagination">
              <button onClick={handlePrevPage} disabled={currentPage === 1}>
                Previous
              </button>
              <span>
                Page {currentPage} of {totalPages}
              </span>
              <button onClick={handleNextPage} disabled={currentPage === totalPages}>
                Next
              </button>
            </div>
          </div>
        )}

        {activeSection === 'notifications' && (
          <div id="notifications" className="notifications">
            <h2>Notifications</h2>
            {notifications.length === 0 ? (
              <p>No notifications available.</p>
            ) : (
              notifications.map((notif) => (
                <div key={notif.id} className={`notification ${notif.status}`}>
                  <p>{notif.message}</p>
                  <button onClick={() => handleApproveNotification(notif.id)}>Approve</button>
                  <button onClick={() => handleRejectNotification(notif.id)}>Reject</button>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  );
};

const Sidebar = ({ activeSection, onSectionChange }) => (
  <div className="sidebar">
    <h3>Account</h3>
    <ul>
      <li>
        <button
          className={activeSection === 'personal-info' ? 'active' : ''}
          onClick={() => onSectionChange('personal-info')}
        >
          Personal Info
        </button>
      </li>
      <li>
        <button
          className={activeSection === 'my-publications' ? 'active' : ''}
          onClick={() => onSectionChange('my-publications')}
        >
          My Publications
        </button>
      </li>
      <li>
        <button
          className={activeSection === 'notifications' ? 'active' : ''}
          onClick={() => onSectionChange('notifications')}
        >
          Notifications
        </button>
      </li>
    </ul>
  </div>
);

export default AccountPage;
