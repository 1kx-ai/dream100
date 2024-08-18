import React, { useState } from 'react';
import { setApiToken, setApiUrl, getApiToken, getApiUrl } from './apiConfig';

const ApiConfigComponent = () => {
  const [token, setToken] = useState(getApiToken() || '');
  const [url, setUrl] = useState(getApiUrl());

  const handleTokenSubmit = (e) => {
    e.preventDefault();
    setApiToken(token);
    alert('API Token updated');
  };

  const handleUrlSubmit = (e) => {
    e.preventDefault();
    setApiUrl(url);
    alert('API URL updated');
  };

  return (
    <div>
      <form onSubmit={handleTokenSubmit}>
        <input
          type="text"
          value={token}
          onChange={(e) => setToken(e.target.value)}
          placeholder="Enter API Token"
        />
        <button type="submit">Set API Token</button>
      </form>
      <form onSubmit={handleUrlSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter API URL"
        />
        <button type="submit">Set API URL</button>
      </form>
    </div>
  );
};

export default ApiConfigComponent;