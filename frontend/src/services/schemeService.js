import api from './api';
import { mockSchemes } from '../mock/schemes';

export const getEligibleSchemes = (profileData) => {
  return api.post('/api/v1/match', profileData);
};

export const getSchemeById = (id) => {
  return api.get(`/api/v1/schemes/${id}`);
};

export const compareSchemePolicy = (schemeId, userProfile = null) => {
  return api.post('/api/v1/comparator', {
    scheme_id: schemeId,
    user_profile: userProfile,
  });
};
