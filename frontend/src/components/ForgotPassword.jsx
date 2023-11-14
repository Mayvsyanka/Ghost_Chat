import React, { useState } from 'react';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [showForm, setShowForm] = useState(true);

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/auth/reset-password/request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessage(data.message);
        setShowForm(false);
      } else {
        setMessage('Error occurred. Please try again.');
      }
    } catch (error) {
      setMessage('Error occurred. Please try again.');
    }
  };

  return (
    <div>
      {showForm ? (
        <form onSubmit={handleSubmit}>
          <label>Email:</label>
          <input            type="email"
                            placeholder="Enter email"
                            value={email}
                            onChange={handleEmailChange} required
                            className="input"/>
          <button className="button is-warning is-text is-light mt-1" type="submit">Submit</button>
        </form>
      ) : (
        <p>{message}</p>
      )}
    </div>
  );
};

export default ForgotPassword;