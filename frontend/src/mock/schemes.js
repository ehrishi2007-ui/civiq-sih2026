export const mockSchemes = [
  {
    scheme_id: 'pm_kisan',
    scheme_name: 'PM-KISAN Samman Nidhi',
    ministry: 'Ministry of Agriculture & Farmers Welfare',
    description:
      'Income support of ₹6,000/year to small and marginal farmer families, paid in three equal installments of ₹2,000 each.',
    benefit: '₹6,000/year',
    score: 0.92,
    eligible: true,
    application_url: 'https://pmkisan.gov.in',
    tags: ['agriculture', 'income-support', 'central'],
    documents_required: ['Aadhaar', 'Land Record', 'Bank Passbook'],
    criteria: [
      {
        field: 'age',
        label: 'Age ≥ 18',
        pass: true,
        evidence: {
          document: 'PM-KISAN Guidelines 2024.pdf',
          page: 4,
          section: 'Eligibility Criteria',
          quote:
            "All land-holding farmers' families with cultivable land are eligible, provided the applicant is 18 years or older.",
        },
      },
      {
        field: 'has_land',
        label: 'Must be a land-holding farmer',
        pass: true,
        evidence: {
          document: 'PM-KISAN Guidelines 2024.pdf',
          page: 4,
          section: 'Eligibility Criteria',
          quote:
            'The scheme is applicable to all farmer families who hold cultivable land as per the land records of the respective State or UT.',
        },
      },
      {
        field: 'annual_income',
        label: 'Annual income ≤ ₹2,00,000',
        pass: true,
        evidence: {
          document: 'PM-KISAN Guidelines 2024.pdf',
          page: 5,
          section: 'Income Criteria',
          quote:
            'Farmer families with total annual income up to ₹2,00,000 from all sources are eligible for the benefit.',
        },
      },
      {
        field: 'occupation',
        label: 'Occupation: Farmer',
        pass: true,
        evidence: {
          document: 'PM-KISAN Guidelines 2024.pdf',
          page: 3,
          section: 'Definitions',
          quote:
            'A farmer is defined as an individual who owns cultivable land and is engaged in agricultural activities.',
        },
      },
    ],
  },
  {
    scheme_id: 'pm_awas',
    scheme_name: 'PM Awas Yojana (Gramin)',
    ministry: 'Ministry of Rural Development',
    description:
      'Financial assistance for construction of pucca houses to eligible rural households who are houseless or living in kutcha/dilapidated houses.',
    benefit: '₹1,20,000 (plain areas)',
    score: 0.85,
    eligible: true,
    application_url: 'https://pmayg.nic.in',
    tags: ['housing', 'rural', 'central'],
    documents_required: ['Aadhaar', 'BPL Certificate', 'Income Certificate'],
    criteria: [
      {
        field: 'is_rural',
        label: 'Resident of rural area',
        pass: true,
        evidence: {
          document: 'PMAY-G Guidelines 2024.pdf',
          page: 8,
          section: 'Target Beneficiaries',
          quote:
            'The scheme targets rural households who are houseless or living in houses with kutcha walls and kutcha roof.',
        },
      },
      {
        field: 'has_bpl_card',
        label: 'BPL category household',
        pass: true,
        evidence: {
          document: 'PMAY-G Guidelines 2024.pdf',
          page: 9,
          section: 'Selection Criteria',
          quote:
            'Priority is given to households identified under the Socio-Economic Caste Census (SECC) data and BPL list.',
        },
      },
      {
        field: 'annual_income',
        label: 'Annual income ≤ ₹3,00,000',
        pass: true,
        evidence: {
          document: 'PMAY-G Guidelines 2024.pdf',
          page: 10,
          section: 'Income Eligibility',
          quote:
            'Households with annual income not exceeding ₹3,00,000 in rural areas are eligible under the scheme.',
        },
      },
    ],
  },
  {
    scheme_id: 'ayushman_bharat',
    scheme_name: 'Ayushman Bharat PM-JAY',
    ministry: 'Ministry of Health & Family Welfare',
    description:
      'Health insurance coverage of up to ₹5 lakh per family per year for secondary and tertiary care hospitalization to identified vulnerable families.',
    benefit: '₹5,00,000/year health cover',
    score: 0.78,
    eligible: true,
    application_url: 'https://pmjay.gov.in',
    tags: ['health', 'insurance', 'central'],
    documents_required: ['Aadhaar', 'Ration Card', 'Income Certificate'],
    criteria: [
      {
        field: 'ration_card_type',
        label: 'PHH/AAY ration card holder',
        pass: true,
        evidence: {
          document: 'AB-PMJAY Operational Guidelines 2024.pdf',
          page: 12,
          section: 'Beneficiary Identification',
          quote:
            'Families identified through SECC 2011 data and holding PHH or AAY ration cards are automatically eligible.',
        },
      },
      {
        field: 'annual_income',
        label: 'Annual income ≤ ₹5,00,000',
        pass: true,
        evidence: {
          document: 'AB-PMJAY Operational Guidelines 2024.pdf',
          page: 14,
          section: 'Economic Criteria',
          quote:
            'The scheme covers families with annual income up to ₹5,00,000 as per the deprivation criteria.',
        },
      },
    ],
  },
  {
    scheme_id: 'sc_scholarship',
    scheme_name: 'Post-Matric Scholarship for SC Students',
    ministry: 'Ministry of Social Justice & Empowerment',
    description:
      'Financial assistance to Scheduled Caste students studying at post-matriculation or post-secondary stage to enable them to complete their education.',
    benefit: 'Full tuition + ₹1,200/month stipend',
    score: 0.35,
    eligible: false,
    application_url: 'https://scholarships.gov.in',
    tags: ['education', 'scholarship', 'SC', 'central'],
    documents_required: ['Aadhaar', 'Caste Certificate', 'Income Certificate', 'Marksheet'],
    criteria: [
      {
        field: 'category',
        label: 'Must belong to Scheduled Caste (SC)',
        pass: false,
        evidence: {
          document: 'Post-Matric Scholarship SC Guidelines 2024.pdf',
          page: 3,
          section: 'Eligibility',
          quote:
            'The scholarship is exclusively for students belonging to Scheduled Castes as notified by the Government of India.',
        },
      },
      {
        field: 'education',
        label: 'Studying post-matriculation',
        pass: true,
        evidence: {
          document: 'Post-Matric Scholarship SC Guidelines 2024.pdf',
          page: 4,
          section: 'Educational Qualification',
          quote:
            'Students who have passed the matriculation examination and are pursuing higher education are eligible.',
        },
      },
      {
        field: 'annual_income',
        label: 'Family income ≤ ₹2,50,000',
        pass: true,
        evidence: {
          document: 'Post-Matric Scholarship SC Guidelines 2024.pdf',
          page: 5,
          section: 'Income Ceiling',
          quote: 'The annual family income from all sources should not exceed ₹2,50,000.',
        },
      },
    ],
  },
  {
    scheme_id: 'ujjwala',
    scheme_name: 'PM Ujjwala Yojana 2.0',
    ministry: 'Ministry of Petroleum & Natural Gas',
    description:
      'Free LPG connections to women from Below Poverty Line (BPL) households to replace unclean cooking fuels with clean LPG.',
    benefit: 'Free LPG connection + first refill',
    score: 0.88,
    eligible: true,
    application_url: 'https://pmuy.gov.in',
    tags: ['energy', 'LPG', 'women', 'central'],
    documents_required: ['Aadhaar', 'BPL Certificate', 'Bank Account'],
    criteria: [
      {
        field: 'is_rural',
        label: 'Rural household',
        pass: true,
        evidence: {
          document: 'PMUY 2.0 Guidelines 2024.pdf',
          page: 6,
          section: 'Target Group',
          quote:
            'The scheme primarily targets women from BPL households in rural and semi-urban areas.',
        },
      },
      {
        field: 'has_bpl_card',
        label: 'Below Poverty Line household',
        pass: true,
        evidence: {
          document: 'PMUY 2.0 Guidelines 2024.pdf',
          page: 7,
          section: 'Eligibility Criteria',
          quote:
            'Applicant must belong to a BPL household as identified under the SECC 2011 data.',
        },
      },
      {
        field: 'gender',
        label: 'Adult woman in household',
        pass: true,
        evidence: {
          document: 'PMUY 2.0 Guidelines 2024.pdf',
          page: 7,
          section: 'Applicant Requirements',
          quote:
            'The LPG connection is issued in the name of an adult woman member of the eligible BPL household.',
        },
      },
    ],
  },
];
