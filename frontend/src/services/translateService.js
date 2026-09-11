import api from './api';

export const translateText = (text, targetLanguage) => {
  return api.post('/api/v1/translate', { text, target_language: targetLanguage });
};
