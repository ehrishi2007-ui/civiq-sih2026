import { mockSchemes } from '../mock/schemes';
import { mockMythResults } from '../mock/myths';

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const mockApi = {
  profile: async ({ body }) => {
    await delay(800);
    return { status: 'success', profile: JSON.parse(body) };
  },

  match: async ({ body }) => {
    await delay(400);
    const parsed = typeof body === 'string' ? JSON.parse(body || '{}') : (body || {});
    const profile = parsed.profile || parsed || {};
    const matches = mockSchemes.map((s) => {
      let isEligible = true;
      if (s.scheme_id === 'pm_kisan') {
        isEligible = !!profile.has_land && profile.occupation === 'Farmer';
      } else if (s.scheme_id === 'apy') {
        isEligible = (profile.age >= 18 && profile.age <= 40) && profile.occupation !== 'Student';
      } else if (s.scheme_id === 'pm_scholarship_warb') {
        const marks = profile.marks_percentage !== undefined ? profile.marks_percentage : 65;
        const income = profile.annual_income !== undefined ? profile.annual_income : 300000;
        isEligible = marks >= 60 && income <= 600000;
      } else if (s.scheme_id === 'standup_india') {
        isEligible = (profile.age || 20) >= 18 && (profile.gender === 'female' || profile.category === 'SC' || profile.category === 'ST');
      } else if (s.scheme_id === 'pmegp') {
        isEligible = (profile.age || 20) >= 18;
      }
      return {
        ...s,
        eligible: isEligible,
        criteria: s.criteria.map((c) => {
          let pass = true;
          if (c.field === 'occupation' && s.scheme_id === 'apy') {
            pass = profile.occupation !== 'Student';
          } else if (c.field === 'has_land') {
            pass = !!profile.has_land;
          } else if (c.field === 'age') {
            pass = (profile.age || 20) >= 18;
          } else if (c.field === 'marks_percentage') {
            pass = (profile.marks_percentage !== undefined ? profile.marks_percentage : 65) >= 60;
          } else if (c.field === 'annual_income' && s.scheme_id === 'pm_scholarship_warb') {
            pass = (profile.annual_income !== undefined ? profile.annual_income : 300000) <= 600000;
          }
          return { ...c, pass };
        }),
      };
    });
    return { matches };
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
    await delay(300);
    const parsed = JSON.parse(body || '{}');
    const scheme_id = parsed.scheme_id || 'pm_scholarship_warb';
    const profile = parsed.user_profile;
    const isFemale = profile?.gender === 'female';
    const delta = isFemale ? '+Rs. 7,200/year' : '+Rs. 6,000/year';
    const oldB = isFemale ? 'Rs. 36,000/year' : 'Rs. 30,000/year';
    const newB = isFemale ? 'Rs. 43,200/year' : 'Rs. 36,000/year';

    return {
      scheme_id: scheme_id,
      scheme_name: "Prime Minister's Scholarship Scheme (WARB)",
      old_version: '2023-24',
      new_version: '2026-27',
      verified: true,
      status: 'VERIFIED',
      message: 'Verified policy comparison between official PMSS 2023-24 guidelines and revised 2026-27 notification.',
      changes: [
        {
          field: 'Monthly Stipend (Girls)',
          parameter: 'Monthly Stipend (Girls)',
          old_value: 'Rs. 3,000/month (Rs. 36,000/year)',
          new_value: 'Rs. 3,600/month (Rs. 43,200/year)',
          change_label: 'Increased by Rs. 600/month — Extra Rs. 7,200 annually',
          direction: 'up',
          impact: 'If you are a girl scholar, you receive Rs. 7,200 more per year under revised guidelines.'
        },
        {
          field: 'Monthly Stipend (Boys)',
          parameter: 'Monthly Stipend (Boys)',
          old_value: 'Rs. 2,500/month (Rs. 30,000/year)',
          new_value: 'Rs. 3,000/month (Rs. 36,000/year)',
          change_label: 'Increased by Rs. 500/month — Extra Rs. 6,000 annually',
          direction: 'up',
          impact: 'If you are a male scholar, you receive Rs. 6,000 more per year under revised guidelines.'
        },
        {
          field: 'Annual Family Income Ceiling',
          parameter: 'Annual Family Income Ceiling',
          old_value: 'Rs. 6,00,000/year',
          new_value: 'Rs. 8,00,000/year',
          change_label: 'Relaxed by Rs. 2,00,000 — More families now eligible',
          direction: 'up',
          impact: 'Families with income between Rs. 6L and Rs. 8L/year are now newly eligible.'
        }
      ],
      impact: {
        scheme_name: "Prime Minister's Scholarship Scheme (WARB)",
        old_benefit: oldB,
        new_benefit: newB,
        delta: delta,
        direction: 'positive',
        status_change: 'Remains Eligible ✅'
      },
      personalized_impact: `As an eligible ${isFemale ? 'female' : 'male'} scholar, your annual scholarship increases by ${delta} (from ${oldB} to ${newB}). Your evaluation status under verified policy is ELIGIBLE.`,
      sources: [
        {
          doc_name: 'PMSS 2023-24.pdf',
          page: 4,
          section: 'Clause 6: Amount of Scholarship',
          quote: 'Rs. 3000/- per month for girls. Rs. 2500/- per month for boys.'
        },
        {
          doc_name: 'PMSS 2023-24.pdf',
          page: 3,
          section: 'Clause 3(A): Eligibility — Family Income',
          quote: 'Family income of the beneficiary from all sources should not exceed Rs. 6.00 Lakh per annum.'
        }
      ]
    };
  },
};

export default mockApi;
