"use client"
import React, { useState } from 'react';
import Image from 'next/image';

const Signup: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullname, setFullname] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isSigningUp, setIsSigningUp] = useState(false); // State to track signup status
  const [isResponseOK, setIsResponseOK] = useState(false); // State to track response status

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();

    // Validasi kolom username, password, fullname, dan email
    if (!username || !password || !fullname || !email) {
      setError('All fields are required');
      return;
    }

    setIsSigningUp(true);

    try {
      const response = await fetch('http://localhost:8000/user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
          fullname,
          email,
          role: 'customer',
          token: 'tokenmichael',
        }),
      });
    
      const responseData = await response.json();
    
      if (response.ok) {
        console.log('User created successfully');
    
        // Redirect to the login page after successful signup
        window.location.href = '/';
      } else {
        // Handle error response
        const errorMessages = responseData.detail || [{ msg: 'An unexpected error occurred' }];
        setError(errorMessages[0].msg); // Extract the 'msg' property
        setIsResponseOK(false);
      }
    } catch (error) {
      console.error('Error during signup', error);
      setError('An unexpected error occurred');
      setIsResponseOK(false);
    } finally {
      setIsSigningUp(false);
    }
  };

  return (
    <div className="flex flex-row-reverse justify-center items-center mt-20 pt-20 bg-white">
      <div className="mb-8">
        <Image src="/logo.png" alt="Logo" width={400} height={400} />
      </div>
      <form onSubmit={handleSignup} className="w-full max-w-md">
        <div className="mb-4 px-5 ">
          <label htmlFor="username" className="block text-sm font-medium text-gray-600">
            Username
          </label>
          <input
            type="text"
            id="username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
        </div>

        <div className="mb-4 px-5">
          <label htmlFor="password" className="block text-sm font-medium text-gray-600">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
        </div>

        <div className="mb-4 px-5">
          <label htmlFor="fullname" className="block text-sm font-medium text-gray-600">
            Full Name
          </label>
          <input
            type="text"
            id="fullname"
            name="fullname"
            value={fullname}
            onChange={(e) => setFullname(e.target.value)}
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
        </div>

        <div className="mb-4 px-5">
          <label htmlFor="email" className="block text-sm font-medium text-gray-600">
            Email
          </label>
          <input
            type="text"
            id="email"
            name="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
        </div>

        {error && (
          <div className="text-red-500 mb-4 px-5">
            <p>{error}</p>
          </div>
        )}

        <div className='px-5'>
          <button
            type="submit"
            className={`bg-red-200 text-white p-2 rounded-md mb-4 w-full ${isResponseOK ? 'bg-green-500' : ''}`}
            disabled={isSigningUp} // Disable the button when signing up
          >
            {isSigningUp
              ? 'Signing Up...'
              : isResponseOK
              ? 'Redirecting...'
              : 'Signup'}
          </button>
        </div>

        <div className="text-center">
          <button type="button" className="text-blue-500" onClick={() => window.location.href = '/'}>
            Login
          </button>
        </div>
      </form>
    </div>
  );
};

export default Signup;