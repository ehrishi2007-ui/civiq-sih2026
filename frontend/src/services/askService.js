import api from './api';

export const askQuestion = (question, context = {}) => {
  return api.post('/api/v1/ask', { question, context });
};
