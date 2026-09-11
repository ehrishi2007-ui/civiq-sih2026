import mockApi from './mockApi';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL && import.meta.env.VITE_API_BASE_URL.trim() !== '')
  ? import.meta.env.VITE_API_BASE_URL
  : 'http://127.0.0.1:8000';

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
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

    return await response.json();
  } catch (networkError) {
    console.warn(`[CiviQ Live API] Backend call to ${url} failed; falling back to local fallback:`, networkError);
    const cleanPath = endpoint.replace(/^\/api\/v1\//, '');
    if (cleanPath.startsWith('schemes/')) {
      const id = cleanPath.split('/')[1];
      return mockApi['schemes']({ ...options, id });
    }
    if (mockApi[cleanPath]) {
      return mockApi[cleanPath](options);
    }
    throw networkError;
  }
}

export default {
  post: (endpoint, data) => request(endpoint, { method: 'POST', body: JSON.stringify(data) }),
  get: (endpoint) => request(endpoint, { method: 'GET' }),
};
