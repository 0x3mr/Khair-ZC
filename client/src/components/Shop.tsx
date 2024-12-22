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
          const response = await fetch('http://localhost:5000/points/change', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ id: user.id, points: -productPoints }),
          });
    
          if (!response.ok) {
            throw new Error('Failed to redeem product.');
          }
    
          const updatedPoints = user.points - productPoints;
          setUser((prevUser) =>
            prevUser ? { ...prevUser, points: updatedPoints } : undefined
          );
          alert(`You have successfully redeemed the ${productName}`);
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

