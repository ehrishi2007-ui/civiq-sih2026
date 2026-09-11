export const mockMythClaims = [
  'PM-KISAN gives ₹10,000 per year',
  'Ayushman Bharat covers up to ₹5 lakh per family per year',
  'Only BPL families can get PM Awas Yojana',
  'PM Ujjwala Yojana provides free gas cylinders every month',
  'Senior citizens get free rail travel under a government scheme',
];

export const mockMythResults = {
  'PM-KISAN gives ₹10,000 per year': {
    verdict: 'FALSE',
    explanation:
      'PM-KISAN Samman Nidhi provides ₹6,000 per year, not ₹10,000. The amount is disbursed in three equal installments of ₹2,000 each, directly into the bank accounts of eligible farmer families.',
    sources: [
      {
        document: 'PM-KISAN Guidelines 2024.pdf',
        page: 2,
        quote:
          'Under the scheme, an income support of ₹6,000 per year is provided to all eligible land-holding farmer families in three equal installments of ₹2,000.',
      },
    ],
  },
  'Ayushman Bharat covers up to ₹5 lakh per family per year': {
    verdict: 'TRUE',
    explanation:
      'This is correct. Ayushman Bharat PM-JAY provides health coverage of up to ₹5,00,000 per family per year for secondary and tertiary care hospitalization at empanelled hospitals.',
    sources: [
      {
        document: 'AB-PMJAY Operational Guidelines 2024.pdf',
        page: 8,
        quote:
          'Each eligible family is entitled to a health cover of ₹5,00,000 per family per year on a family floater basis for listed secondary and tertiary care conditions.',
      },
    ],
  },
  'Only BPL families can get PM Awas Yojana': {
    verdict: 'PARTIALLY TRUE',
    explanation:
      'While BPL families are given priority under PM Awas Yojana, the scheme also covers other vulnerable groups identified through the SECC 2011 data, including households with no adult member between 16-59, female-headed households, and households with disabled members.',
    sources: [
      {
        document: 'PMAY-G Guidelines 2024.pdf',
        page: 9,
        quote:
          'Beneficiaries are identified using SECC 2011 data based on housing deprivation parameters. Priority is given to houseless households, followed by households living in zero, one or two room kutcha houses.',
      },
    ],
  },
  'PM Ujjwala Yojana provides free gas cylinders every month': {
    verdict: 'FALSE',
    explanation:
      'PM Ujjwala Yojana provides a free LPG connection and the first refill free of cost. Subsequent refills must be purchased by the beneficiary. The scheme does not provide free monthly cylinders.',
    sources: [
      {
        document: 'PMUY 2.0 Guidelines 2024.pdf',
        page: 4,
        quote:
          'Under Ujjwala 2.0, beneficiaries receive a free LPG connection along with the first refill and a hotplate at no cost. Regular refills are to be purchased at market or subsidized rates.',
      },
    ],
  },
  'Senior citizens get free rail travel under a government scheme': {
    verdict: 'FALSE',
    explanation:
      'There is no government scheme providing completely free rail travel for senior citizens. Indian Railways previously offered concessions (40% for men above 60, 50% for women above 58) but these concessions were suspended during COVID-19 and have not been fully restored.',
    sources: [
      {
        document: 'Indian Railways Concession Policy 2024.pdf',
        page: 1,
        quote:
          'Senior citizen concessions in rail travel, which were suspended w.e.f. 20th March 2020, have not been restored. No free travel scheme exists for senior citizens.',
      },
    ],
  },
};
