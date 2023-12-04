"use client"
// Import useEffect and useState from React
import React, { useEffect, useState } from 'react';

const LandingPage: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  useEffect(() => {
    const token = localStorage.getItem('token');

    if (token) {
      setIsAuthenticated(true);
    } else {
      window.location.href = '/';
    }
  }, []);

  if (!isAuthenticated) {
    return <div>Unauthorized</div>;
  }

  return (
    <div className="flex flex-col items-center mt-20 pt-20">
      <h1 className="text-4xl font-bold mb-6">Welcome to KidoQuest</h1>

      <div className="flex space-x-4 pt-4">
      
        
        <button
          type="button"
          onClick={handleLogout}
          className="bg-red-300 text-white py-2 px-4 rounded"
        >
          Logout
        </button>
      </div>
    </div>
  );
};

export default LandingPage;