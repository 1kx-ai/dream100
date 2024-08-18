import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { setApiToken, setApiUrl, getApiToken, getApiUrl } from '../services/apiConfig';

const AuthPage = () => {
  const [token, setToken] = useState(getApiToken() || '');
  const [url, setUrl] = useState(getApiUrl());
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    setApiToken(token);
    setApiUrl(url);
    navigate('/');
  };

  return (
    <div className="hero min-h-screen bg-base-200">
      <div className="hero-content flex-col">
        <div className="text-center">
          <h1 className="text-5xl font-bold">API Configuration</h1>
          <p className="py-6">Please enter your API token and URL to continue.</p>
        </div>
        <div className="card flex-shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
          <form onSubmit={handleSubmit} className="card-body">
            <div className="form-control">
              <label className="label">
                <span className="label-text">API Token</span>
              </label>
              <input
                type="text"
                value={token}
                onChange={(e) => setToken(e.target.value)}
                placeholder="Enter API Token"
                className="input input-bordered"
                required
              />
            </div>
            <div className="form-control">
              <label className="label">
                <span className="label-text">API URL</span>
              </label>
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter API URL"
                className="input input-bordered"
                required
              />
            </div>
            <div className="form-control mt-6">
              <button type="submit" className="btn btn-primary">Set Configuration</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;