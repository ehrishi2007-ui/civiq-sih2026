import api from './api';
import { mockSchemes } from '../mock/schemes';

export const getEligibleSchemes = (profileData) => {
  return api.post('/api/v1/match', profileData);
};

export const getSchemeById = (id) => {
  // Always return from mock data for now, since there's no single-scheme endpoint defined
  return Promise.resolve(mockSchemes.find(s => s.scheme_id === id));
};
