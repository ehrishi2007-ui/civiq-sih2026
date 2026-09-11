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

  'schemes': async ({ url, id }) => {
    await delay(300);
    return mockSchemes.find(s => s.scheme_id === id);
  },

  comparator: async ({ body }) => {
    await delay(500);
    const { scheme_id } = JSON.parse(body || '{}');
    return {
      scheme_id: scheme_id || 'pm_scholarship_warb',
      scheme_name: "Prime Minister's Scholarship Scheme (WARB)",
      old_version: '2023-24',
      new_version: '2026-27',
      verified: false,
      status: 'UNVERIFIED_NEW_VERSION',
      message: 'Comparison between PMSS 2023-24 and 2026-27 is pending OCR/multimodal verification. PMSS 2026-27.pdf is a scanned image document with zero extractable digital text; no policy differences are asserted to prevent fabricating ungrounded comparisons.',
      changes: [],
      diff_matrix: [],
      personalized_impact: 'Policy comparison between 2023-24 and 2026-27 requires document-level multimodal verification.',
      sources: [
        {
          document: 'PMSS 2023-24.pdf',
          page: 4,
          section: 'Clause 6: Amount of Scholarship',
          quote: 'Rs. 3000/- per month for girls. Rs. 2500/- per month for boys.',
        },
      ],
    };
  },
};

export default mockApi;
