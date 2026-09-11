export const mockDiffData = {
  pm_kisan: {
    changes: [
      { field: 'Income Limit', old_value: '₹2,00,000', new_value: '₹2,50,000', change_label: '▲ +₹50,000', direction: 'up' },
      { field: 'Age Limit', old_value: '18–60 years', new_value: '18–65 years', change_label: '▲ +5 years', direction: 'up' },
      { field: 'Installment Amount', old_value: '₹2,000 × 3', new_value: '₹2,667 × 3', change_label: '▲ +₹667', direction: 'up' },
    ],
  },
  pm_awas: {
    changes: [
      { field: 'Assistance (Plain)', old_value: '₹1,20,000', new_value: '₹1,50,000', change_label: '▲ +₹30,000', direction: 'up' },
      { field: 'Assistance (Hilly)', old_value: '₹1,30,000', new_value: '₹1,60,000', change_label: '▲ +₹30,000', direction: 'up' },
      { field: 'Completion Timeline', old_value: '36 months', new_value: '24 months', change_label: '▼ −12 months', direction: 'down' },
    ],
  },
};

export const mockImpactData = {
  pm_kisan: {
    scheme_name: 'PM-KISAN Samman Nidhi',
    old_benefit: '₹6,000/year',
    new_benefit: '₹8,000/year',
    delta: '+₹2,000/year',
    direction: 'positive',
    status_change: 'Remains Eligible ✅',
  },
  pm_awas: {
    scheme_name: 'PM Awas Yojana (Gramin)',
    old_benefit: '₹1,20,000',
    new_benefit: '₹1,50,000',
    delta: '+₹30,000',
    direction: 'positive',
    status_change: 'Now Eligible (income limit raised) ✅',
  },
};
