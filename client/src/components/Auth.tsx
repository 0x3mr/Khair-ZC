import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaUser, FaLock, FaEnvelope } from "react-icons/fa";
import { TbArrowBadgeLeft } from "react-icons/tb";
import '../assets/stylesheets/Auth.css';
import logo from '../assets/images/KhairZcLogo.png';


const Auth = () => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [fname, setFName] = useState('');
  const [lname, setLName] = useState('');
  const [id, setId] = useState('');
  const [userPass, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [points, setPoints] = useState(0); // Optional, for managing points dynamically

  const toggleAuth = () => { setIsSignUp(!isSignUp); };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (isSignUp && userPass !== confirmPassword) {
      alert("Passwords don't match!");
      return;
    }

    try {
      const authType = isSignUp ? '/auth/register' : '/auth/login';
      const authParameters = isSignUp
        ? { fname, lname, email, userPass,points,id}
        : { email, userPass };

      const response = await fetch(`http://localhost:5000${authType}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(authParameters),
        credentials: 'include', // Allow sending and receiving cookies
      });

      const data = await response.json();

      if (response.ok) {
        console.log('Authentication successful', data);

        if (isSignUp) {
          window.location.href = '/auth';
        } else {
          window.location.href = '/';
        }
      }
      else {
        alert(`Authentication failed: ${data.error || data.message || 'Unknown error'}`);
      }
    }
    catch (error) {
      console.error('Error during authentication: ', error);
      alert('An error occurred during authentication');
    }
  };

  return (
    <>
      <div className="auth-page">
        <Link to="/" className="back-button">
          <TbArrowBadgeLeft className="icon" />
        </Link>
        <div className="auth-box-main">
          <div className="logo-container">
            <img src={logo} alt="Logo" className="logo" />
          </div>
          <div className="auth-content">
            <div className="auth-wrapper">
              <div className="auth-form">
                <h2>{isSignUp ? 'Sign Up' : 'Welcome back!'}</h2>
                <form onSubmit={handleSubmit}>
                  <div className="input-data-container">
                    <input required type="email" placeholder="Email" value={email} onChange={(event) => setEmail(event.target.value)} />
                    <FaEnvelope className="icon" />
                  </div>
                  {isSignUp && (
                    <>
                      <div className="input-data-container">
                        <input required type="text" placeholder="First name" value={fname} onChange={(event) => setFName(event.target.value)} />
                        <FaUser className="icon" />
                      </div>
                      <div className="input-data-container">
                        <input required type="text" placeholder="Last name" value={lname} onChange={(event) => setLName(event.target.value)} />
                        <FaUser className="icon" />
                      </div>
                    </>
                  )}
                  <div className="input-data-container">
                    <input required type="password" placeholder="Password" value={userPass} onChange={(event) => setPassword(event.target.value)} />
                    <FaLock className="icon" />
                  </div>
                  {isSignUp && (
                    <div className="input-data-container">
                      <input required type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(event) => setConfirmPassword(event.target.value)} />
                      <FaLock className="icon" />
                    </div>
                  )}
                  <button type="submit">{isSignUp ? 'Sign Up' : 'Sign In'}</button>
                </form>
              </div>
            </div>
            <div className="auth-separator"></div>
            <div className="auth-with-third-party">
              <div className="block"></div>
            </div>
          </div>
          <div className="auth-link">
            {isSignUp ? (
              <p>
                Already have an account?{' '}
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    toggleAuth();
                  }}
                >
                  Sign In
                </button>
              </p>
            ) : (
              <p>
                Don’t have an account?{' '}
                <button
                  onClick={(e) => {
                    e.preventDefault();
                    toggleAuth();
                  }}
                >
                  Sign Up
                </button>
              </p>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default Auth;