import { getApiToken, getApiUrl } from './apiConfig';

async function fetchWithAuth(endpoint, options = {}) {
  const apiToken = getApiToken();
  const apiUrl = getApiUrl();

  if (!apiToken) {
    throw new Error('API token is not set. Please configure it in the Auth page.');
  }

  const defaultHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiToken}`
  };

  const response = await fetch(`${apiUrl}${endpoint}`, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'An error occurred');
  }

  return response.json();
}

export const api = {
  get: (endpoint) => fetchWithAuth(endpoint),
  post: (endpoint, data) => fetchWithAuth(endpoint, {
    method: 'POST',
    body: JSON.stringify(data)
  }),
  put: (endpoint, data) => fetchWithAuth(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data)
  }),
  delete: (endpoint) => fetchWithAuth(endpoint, {
    method: 'DELETE'
  })
};