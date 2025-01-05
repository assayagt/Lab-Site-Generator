import React, { useState } from 'react';
import './AccountPage.css';

const AccountPage = () => {
  const [activeSection, setActiveSection] = useState('personal-info'); // Track the active section
  const [notifications, setNotifications] = useState([
    { id: 1, message: 'New publication approval', status: 'pending' },
    { id: 2, message: 'Profile update required', status: 'pending' },
  ]);
  const [publications, setPublications] = useState([
    { id: 1, title: 'Publication 1', content: 'Lorem ipsum dolor sit amet.' },
    { id: 2, title: 'Publication 2', content: 'Consectetur adipiscing elit.' },
  ]);

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

  return (
    <div className="account-page">
      <Sidebar activeSection={activeSection} onSectionChange={handleSectionChange} />
      <div className="main-content">
      {activeSection === 'personal-info' && (
          <form id="personal-info" className="personal-info" onSubmit={(e) => { e.preventDefault(); alert('Form Submitted'); }}>
            <h2>Personal Information</h2>
            <div className="info">
              <img src="default-photo.jpg" alt="User" className="user-photo" />
              <div className="details">
                <label>
                  <strong>Bio:</strong>
                  <textarea defaultValue="Lorem ipsum dolor sit amet." />
                </label>

                <label>
                  <strong>Email:</strong>
                  <input type="email" defaultValue="user@example.com" />
                </label>

                <label>
                  <strong>Secondary Email:</strong>
                  <input type="email" defaultValue="secondary@example.com" />
                </label>

                <label>
                  <strong>Degree:</strong>
                  <input type="text" defaultValue="Bachelor of Science" />
                </label>

                <label>
                  <strong>LinkedIn:</strong>
                  <input type="url" defaultValue="linkedin.com/in/username" />
                </label>
              </div>
            </div>
            <button type="submit">Save Changes</button>
          </form>
        )}
        {activeSection === 'my-publications' && (
          <div id="my-publications" className="my-publications">
            <h2>My Publications</h2>
            <ul>
              {publications.map((publication) => (
                <li key={publication.id}>
                  <div>
                    <strong>{publication.title}</strong>
                  </div>
                  <p>{publication.content}</p>
                  <button onClick={() => handleEditPublication(publication.id)}>
                    Edit
                  </button>
                </li>
              ))}
            </ul>
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
