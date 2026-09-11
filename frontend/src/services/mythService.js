import api from './api';

export const checkMyth = (claim) => {
  return api.post('/api/v1/myths/check', { claim });
};
