import mockApi from './mockApi';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

async function request(endpoint, options = {}) {
  // Use mock API if no backend URL is configured
  if (!API_BASE_URL || API_BASE_URL.trim() === '') {
    const cleanPath = endpoint.replace(/^\/api\/v1\//, '');
    if (cleanPath.startsWith('schemes/')) {
      const id = cleanPath.split('/')[1];
      return mockApi['schemes']({ ...options, id });
    }
    return mockApi[cleanPath](options);
  }

  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export default {
  post: (endpoint, data) => request(endpoint, { method: 'POST', body: JSON.stringify(data) }),
  get: (endpoint) => request(endpoint, { method: 'GET' }),
};
