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
    let errorMessage;
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || 'An error occurred';
    } catch {
      errorMessage = 'An error occurred';
    }
    throw new Error(errorMessage);
  }

  // Only try to parse JSON if there's content
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    const text = await response.text();
    return text ? JSON.parse(text) : null;
  }

  return null; // Return null for empty responses
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