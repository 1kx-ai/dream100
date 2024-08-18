let API_URL = 'http://localhost:8000';  // Default URL
let API_TOKEN = null;

export const setApiToken = (token) => {
  API_TOKEN = token;
  localStorage.setItem('API_TOKEN', token);  // Store token in localStorage
};

export const getApiToken = () => {
  if (!API_TOKEN) {
    API_TOKEN = localStorage.getItem('API_TOKEN');  // Retrieve token from localStorage
  }
  return API_TOKEN;
};

export const setApiUrl = (url) => {
  API_URL = url;
  localStorage.setItem('API_URL', url);  // Store URL in localStorage
};

export const getApiUrl = () => {
  if (API_URL === 'http://localhost:8000') {
    const storedUrl = localStorage.getItem('API_URL');
    if (storedUrl) API_URL = storedUrl;
  }
  return API_URL;
};

// Initialize from localStorage on module load
getApiToken();
getApiUrl();