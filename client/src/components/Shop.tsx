import React from 'react';
import { useState,useEffect } from 'react';
import '../assets/stylesheets/Shop.css';
import { IoArrowBackCircleOutline } from "react-icons/io5";
import { useNavigate } from 'react-router-dom';

interface product{
  id: number,
  name: string,
  description: string,
  price: number,
  image: string
}
interface user {
  id: string
  firstName: string,
  lastName: string,
  email: string,
  isAdmin: boolean,
  points: number
}

const Points=35;
const Shop = () => {

  const [products, setProducts] = useState<product[]>([]);
  const [user, setUser] = useState<user>();
  const fetchProducts='http://localhost:5000/shop/products'
  const fetchUser = 'http://localhost:5000/security/user'
  const fetchRedeem='http://localhost:5000/points/change'
  const [redemptionCodes, setRedemptionCodes] = useState([
    'XZ9Q2KJ4P7', 'BQ9L3T4F8H', 'M8R7K6C5S1', 'V9Y3A6WZQ1', 
    'J7C2N5L9G0', 'X4D5P7S9K3', 'R1H2Q4M8Z9', 'F6A5T2J7K9',
    'L2U7O8V4N1', 'C3P9W5E6X7', 'Z8K0T2L5M3', 'S7F3P8J1R6'
  ]);
  useEffect(() => {
    fetch(fetchProducts)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch products');
        }
        return response.json();
      })
      .then(data => {
        console.log("Fetched products:", data);
        setProducts(data);
      })
      .catch(error => {
        console.error('Error:', error);
      });

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
  
  const navigate = useNavigate();

  const goBack = () => {
    navigate(-1);}

    const handleRedeem = async (productName: string, productPoints: number) => {
      if (!user || user.points < productPoints) {
        alert('Insufficient points or user not logged in.');
        return;
      }
    
      const userConfirmed = window.confirm(
        `Are you sure you want to redeem the ${productName} with ${productPoints} points?`
      );
    
      if (userConfirmed) {
        try {
          const response = await fetch(fetchRedeem, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ user_id: user.id, points: -productPoints }),
          });
    
          if (!response.ok) {
            throw new Error('Failed to redeem product.');
          }
    
          const updatedPoints = user.points - productPoints;
          setUser((prevUser) =>
            prevUser ? { ...prevUser, points: updatedPoints } : undefined
          );
    
          if (redemptionCodes.length > 0) {
            const redemptionCode = redemptionCodes[0]; 
    
            // Remove the used code from the list
            setRedemptionCodes((prevCodes) => prevCodes.slice(1));
    
            // Show the redemption code
            alert(`Redemption successful! Use this code to redeem your product from the admin:\n\nCode: ${redemptionCode}`);
          } else {
            alert('No redemption codes left.');
          }
        } catch (error) {
          console.error('Error redeeming product:', error);
          alert('An error occurred while redeeming the product.');
        }
      }
    };    
  return (
    <div className='Products-Container'>
      <div>
        <nav className='ShopBar'>
        <IoArrowBackCircleOutline className='BackArrow' onClick={goBack}/>
          <div className='ShopBar-container'>
            <div className='Available-points'>
                <p>Available Points: {user?.points}</p>
            </div>
          </div>
        </nav>
      </div>
      {products.map((product) => (
        <div className='Product-Card'>
          <div className='Product-image'>
            <img src={product.image} alt={product.name} />
          </div>
          <div className='Product-info'>
            <h2>{product.name}</h2>
            <p>{product.description}</p>
            <h3>{product.price} points</h3>
          </div>
          <button onClick={()=>handleRedeem(product.name,product.price)} className="btn-donate">
            Redeem
          </button>
        </div>
      ))}
    </div>
  );
};

export default Shop;

