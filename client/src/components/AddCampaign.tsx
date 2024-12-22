import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/stylesheets/AddCampaign.css';

interface Campaign {
  userId: string;
  campaignName: string;
  campaignRe: string;
  campaignDesc: string;
  campaignDate: string;
  campaignCap: string;
  charId: string;
}

interface user {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  isAdmin: boolean;
  points: number;
}

const AddCampaign = () => {
  const [campaign, setCampaign] = useState<Campaign>({
    userId: '',  // Initially empty, will be set later
    campaignName: '',
    campaignRe: '',
    campaignDesc: '',
    campaignDate: '',
    campaignCap: '',
    charId: ''
  });
  
  const [user, setUser] = useState<user | null>(null);
  const fetchUser = 'http://localhost:5000/security/user';

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

        // Automatically set userId after fetching user data
        setCampaign(prevCampaign => ({
          ...prevCampaign,
          userId: userData.id // Setting userId to the logged-in user's id
        }));

      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchUserData();
  }, []);

  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;
    setCampaign(prevCampaign => ({
      ...prevCampaign,
      [name]: value
    }));
  };

  const handleAddCampaign = () => {
    // Clear all form fields when adding another campaign
    setCampaign({
      userId: '',
      campaignName: '',
      campaignRe: '',
      campaignDesc: '',
      campaignDate: '',
      campaignCap: '',
      charId: ''
    });
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    // Validate that all fields are filled
    if (
      !campaign.campaignName ||
      !campaign.campaignRe ||
      !campaign.campaignDesc ||
      !campaign.campaignCap ||
      !campaign.charId
    ) {
      setError('All fields are required');
      return;
    }

    try {
      const response = await fetch('http://localhost:5000/campaign/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify([campaign]), // Sending one campaign instead of multiple
      });

      const responseData = await response.json();

      if (response.ok) {
        setSuccessMessage('Campaign created successfully!');
        setError('');
      } else {
        console.error('Error response from backend:', responseData);
        setError(responseData.error || 'Failed to create campaign');
      }
    } catch (error) {
      console.error('Error creating campaign:', error);
      setError('An error occurred while creating campaign');
    }
  };

  return (
    <div className="create-campaign-form">
      <h2>Create Campaign</h2>
      {error && <p className="error">{error}</p>}
      {successMessage && <p className="success">{successMessage}</p>}
      <form onSubmit={handleSubmit}>
        <div className="campaign-form-fields">
          <input
            type="text"
            name="campaignName"
            value={campaign.campaignName}
            onChange={handleChange}
            placeholder="Campaign Name"
          />
          <input
            type="text"
            name="campaignRe"
            value={campaign.campaignRe}
            onChange={handleChange}
            placeholder="Campaign Reward"
          />
          <textarea
            name="campaignDesc"
            value={campaign.campaignDesc}
            onChange={handleChange}
            placeholder="Campaign Description"
          />
          <input
            type="text"
            name="campaignDate"
            value={campaign.campaignDate}
            onChange={handleChange}
            placeholder="Campaign Date"
          />
          <input
            type="number"
            name="campaignCap"
            value={campaign.campaignCap}
            onChange={handleChange}
            placeholder="Campaign Capacity"
          />
          <input
            type="text"
            name="charId"
            value={campaign.charId}
            onChange={handleChange}
            placeholder="Charity ID"
          />
        </div>
        <button type="button" onClick={handleAddCampaign}>Add Another Campaign</button>
        <button type="submit">Create Campaign</button>
      </form>
    </div>
  );
};

export default AddCampaign;
