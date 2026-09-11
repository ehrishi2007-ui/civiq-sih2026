import api from './api';

export const saveProfile = (profileData) => {
  return api.post('/api/v1/profile', profileData);
};
