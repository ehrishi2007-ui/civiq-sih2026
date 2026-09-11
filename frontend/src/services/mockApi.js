import { mockSchemes } from '../mock/schemes';
import { mockMythResults } from '../mock/myths';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const mockApi = {
  profile: async ({ body }) => {
    await delay(800);
    return { status: 'success', profile: JSON.parse(body) };
  },

  match: async ({ body }) => {
    await delay(1500);
    const profile = JSON.parse(body);
    // In mock mode, we just return the predefined list
    // Actual logic happens on the backend
    return { matches: mockSchemes };
  },

  ask: async ({ body }) => {
    await delay(1200);
    const { question } = JSON.parse(body);
    return {
      answer: `Mock answer to: "${question}". This is a placeholder since the backend is not connected.`,
      sources: [],
    };
  },

  'myths/check': async ({ body }) => {
    await delay(1000);
    const { claim } = JSON.parse(body);
    return mockMythResults[claim] || {
      verdict: 'UNKNOWN',
      explanation: 'This claim is not in the mock database.',
      sources: [],
    };
  },

  translate: async ({ body }) => {
    await delay(300);
    const { text, target_language } = JSON.parse(body);
    return { translated_text: `[${target_language}] ${text}` };
  },
};

export default mockApi;
