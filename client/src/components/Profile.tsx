import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';  // Import useNavigate
import { FaUser, FaCog, FaShieldAlt, FaChartBar, FaSignOutAlt } from "react-icons/fa";
import { IoAddCircleSharp } from "react-icons/io5";
import { FiHome } from "react-icons/fi";
import '../assets/stylesheets/Profile.css';
import logo from '../assets/images/icon.png';

interface user {
  id: string
  firstName: string,
  lastName: string,
  email: string,
  isAdmin: boolean,
  points: number
}

const Profile = () => {
  const [activeTab, setActiveTab] = useState('appearance');
  const [user, setUser] = useState<user>();
  const fetchUser = 'http://localhost:5000/security/user';

  const navigate = useNavigate(); // Initialize useNavigate here

  const handleHomeButtonClick = () => {
    navigate('/'); // Navigate to the home page
  };

  const handleLogOutButtonClick = () => {
    navigate('/logout'); // Navigate to the logout page
  };

  const handleAddCampaignClick = () => {
    navigate('/addCampaign');
  }

  const handleAddCharityClick = () => {
    navigate('/addCharity');
  }
  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await fetch(fetchUser, {
          method: 'GET',
          credentials: 'include',
        });
        if (!response.ok) {
          throw new Error('Failed to fetch user data');
        }

        const userData = await response.json();
        setUser(userData);
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchUserData();
  }, []);

  const renderContent = () => {
    switch (activeTab) {
      case 'appearance':
        return (
          <div className="content-section">
            <h2>Profile Details</h2>
            <div className="profile-details">
              <div className="detail-item">
                <p>ID: {user?.id}</p>
                <p>Name: {user?.firstName} {user?.lastName}</p>
                <p>Email: {user?.email}</p>
              </div>
            </div>
          </div>
        );

      case 'statistics':
        return (
          <div className="content-section">
            <h2>User Statistics</h2>
            <div className="statistics-grid">
              <div className="stat-item">
                {!user?.isAdmin ? (
                  <>
                    <p>Current Points: {user?.points}</p>
                    <p>Followed Charities: </p>
                    <p>Attended Campaigns: </p>
                    <p>Status: User</p>
                  </>
                ) : (
                  <>
                    <p>Status: Admin</p>
                  </>
                )}

              </div>
            </div>
          </div>
        );

      case 'settings':
        return (
          <div className="content-section">
            <h2>Settings</h2>
            <div className="settings-options">
              <button className="edit-button">Edit Profile</button>
              <button className="edit-button">Change Password</button>
            </div>
          </div>
        );

      case 'privacy':
        return (
          <div className="content-section">
            <h2>Privacy Settings</h2>
            <div className="privacy-options">
              <div className="privacy-item">
                <input type="checkbox" id="public-profile" />
                <label htmlFor="public-profile">Make profile public</label>
              </div>
              <div className="privacy-item">
                <input type="checkbox" id="show-stats" />
                <label htmlFor="show-stats">Show statistics to others</label>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="prof-page">
      <div className="prof-container">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="sidebar-header">
            <img src={logo} alt="Logo" className="logo" /> <h1>Profile</h1>
          </div>
          <nav className="sidebar-nav">
            <button
              className={`nav-item ${activeTab === 'appearance' ? 'active' : ''}`}
              onClick={() => setActiveTab('appearance')}
            >
              <FaUser className="icon" />
              <span>Appearance</span>
            </button>
            <button
              className={`nav-item ${activeTab === 'statistics' ? 'active' : ''}`}
              onClick={() => setActiveTab('statistics')}
            >
              <FaChartBar className="icon" />
              <span>Statistics</span>
            </button>
            <button
              className={`nav-item ${activeTab === 'privacy' ? 'active' : ''}`}
              onClick={() => setActiveTab('privacy')}
            >
              <FaShieldAlt className="icon" />
              <span>Privacy</span>
            </button>
            <button
              className={`nav-item ${activeTab === 'settings' ? 'active' : ''}`}
              onClick={() => setActiveTab('settings')}
            >
              <FaCog className="icon" />
              <span>Settings</span>
            </button>
          </nav>
          {user?.isAdmin && (
            <>
              <button onClick={handleAddCampaignClick} className="home-button">
                <IoAddCircleSharp className="icon" />
                <span>Add Campaign</span>
              </button>
              <button onClick={handleAddCharityClick} className="home-button">
                <IoAddCircleSharp className="icon" />
                <span>Add Charity</span>
              </button>
            </>
          )}
          <button onClick={handleLogOutButtonClick} className="logout-button">
            <FaSignOutAlt className="icon" />
            <span>Log Out</span>
          </button>
          <button onClick={handleHomeButtonClick} className="home-button">
            <FiHome className="icon" />
            <span>Home Page</span>
          </button>
        </div>

        {/* Main Content */}
        <div className="main-content">
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Profile;
