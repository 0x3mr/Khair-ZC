import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../assets/stylesheets/AddCharity.css';

interface Charity {
  name: string;
  address: string;
  description: string;
  category: string;
  image: string;
  userId: string; // Add userId to track the logged-in user
}

interface User {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  isAdmin: boolean;
  points: number;
}

const AddCharity = () => {
  const [charities, setCharities] = useState<Charity[]>([{
    name: '',
    address: '',
    description: '',
    category: '',
    image: '',
    userId: '', // Initialize userId as empty
  }]);

  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(''); 
  const [successMessage, setSuccessMessage] = useState<string | null>(''); 
  const navigate = useNavigate();

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

        setCharities(prevCharities => prevCharities.map(charity => ({
          ...charity,
          userId: userData.id 
        })));

      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchUserData();
  }, []);

  const handleChange = (
    index: number,
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = event.target;

    if (name in charities[index]) {
      const updatedCharities = [...charities];
      updatedCharities[index][name as keyof Charity] = value;
      setCharities(updatedCharities);
    }
  };

  const handleAddCharityClick = () => {
    setCharities([
      ...charities,
      {
        name: '',
        address: '',
        description: '',
        category: '',
        image: '',
        userId: user?.id || '', 
      }
    ]);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
  
    // Check if userId is present
    if (!user?.id) {
      setError('User not found');
      return;
    }
  
    for (const charity of charities) {
      if (
        !charity.name ||
        !charity.category ||
        !charity.description ||
        !charity.image ||
        !charity.address ||
        !charity.userId // Make sure userId is not empty
      ) {
        setError('All fields are required');
        return;
      }
    }
  
    try {
      const response = await fetch('http://localhost:5000/charity/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(charities), // Ensure this is correct
      });
  
      const data = await response.json();
  
      if (response.ok) {
        setSuccessMessage('Charities created successfully!');
        setError('');  // Clear any previous errors
      } else {
        console.error('Error response from backend:', data);
        setError(data.error || 'Failed to create charities');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('An error occurred while creating the charities.');
    }
  };
  

  return (
    <div className="create-charity-form">
      <h2>Create Charity</h2>

      {/* Display error or success messages */}
      {error && <div className="alert alert-danger">{error}</div>}
      {successMessage && <div className="alert alert-success">{successMessage}</div>}

      <form onSubmit={handleSubmit}>
        {charities.map((charity, index) => (
          <div key={index} className="charity-form-fields">
            <input
              type="text"
              name="name"
              value={charity.name}
              onChange={(e) => handleChange(index, e)}
              placeholder="Charity Name"
            />
            <input
              type="text"
              name="address"
              value={charity.address}
              onChange={(e) => handleChange(index, e)}
              placeholder="Charity Address"
            />
            <textarea
              name="description"
              value={charity.description}
              onChange={(e) => handleChange(index, e)}
              placeholder="Charity Description"
            />
            <input
              type="text"
              name="category"
              value={charity.category}
              onChange={(e) => handleChange(index, e)}
              placeholder="Category"
            />
            <input
              type="text"
              name="image"
              value={charity.image}
              onChange={(e) => handleChange(index, e)}
              placeholder="Charity Image URL"
            />
          </div>
        ))}
        <button type="button" onClick={handleAddCharityClick}>Add Another Charity</button>
        <button type="submit">Add Charity</button>
      </form>
    </div>
  );
};

export default AddCharity;
