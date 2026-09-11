export const mockSchemes = [
  {
    scheme_id: 'pm_kisan',
    scheme_name: "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
    ministry: "Ministry of Agriculture & Farmers' Welfare",
    description:
      "Income support of ₹6,000 per year to all landholding farmer families across the country, released in three 4-monthly installments of ₹2,000 each via DBT.",
    benefit: "₹6,000/year via DBT",
    score: 0.92,
    eligible: true,
    application_url: "https://pmkisan.gov.in",
    tags: ["agriculture", "income-support", "central-sector", "farmer"],
    documents_required: ["Aadhaar", "Land Record / RoR", "Bank Account Details"],
    criteria: [
      {
        field: "has_land",
        label: "Landholding Farmer Family",
        pass: true,
        evidence: {
          document: "PM-KISAN.pdf",
          page: 2,
          section: "Clause 3: Definition of farmer's family",
          quote:
            "A landholder farmer's family is defined as 'a family comprising of husband, wife and minor children who owns cultivable land as per land records of the concerned State/UT'.",
        },
      },
      {
        field: "occupation",
        label: "Primary Occupation: Farmer",
        pass: true,
        evidence: {
          document: "PM-KISAN.pdf",
          page: 2,
          section: "Clause 1: Scheme",
          quote:
            "With a view to provide income support to all landholding farmers' families in the country, having cultivable land, the Central Government has implemented a Central Sector Scheme, namely, 'Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)'.",
        },
      },
    ],
  },
  {
    scheme_id: "pmegp",
    scheme_name: "Prime Minister's Employment Generation Programme (PMEGP)",
    ministry: "Ministry of Micro, Small and Medium Enterprises (MSME)",
    description:
      "Credit-linked subsidy programme to generate self-employment micro-enterprises in non-farm sector.",
    benefit: "Margin money subsidy up to 35% on project loans up to ₹50 Lakhs",
    score: 0.88,
    eligible: true,
    application_url: "https://www.kviconline.gov.in/pmegpeportal",
    tags: ["employment", "micro-enterprise", "subsidy", "msme", "business"],
    documents_required: [
      "Aadhaar",
      "Project Report",
      "Education Certificate (VIII pass for >10L Mfg)",
      "Bank Account Details",
    ],
    criteria: [
      {
        field: "age",
        label: "Age ≥ 18 Years",
        pass: true,
        evidence: {
          document: "PMEGP.pdf",
          page: 5,
          section: "Section 4.1: For PMEGP new enterprises (Units), Clause (i)",
          quote: "Any individual, above 18 years of age",
        },
      },
    ],
  },
  {
    scheme_id: "pm_scholarship_warb",
    scheme_name: "Prime Minister's Scholarship Scheme (WARB)",
    ministry: "Ministry of Home Affairs",
    description:
      "Scholarship to encourage higher technical and professional education for dependent wards & widows of CAPFs, Assam Rifles, and State Police Personnel.",
    benefit: "₹3,000/mo (Girls) / ₹2,500/mo (Boys)",
    score: 0.95,
    eligible: true,
    application_url: "https://scholarships.gov.in",
    tags: ["education", "scholarship", "capf", "higher-education"],
    documents_required: [
      "Aadhaar",
      "CAPF Wards Certificate / Discharge Book",
      "MEQ Marksheet (Min 60%)",
      "Bank Account Details",
    ],
    criteria: [
      {
        field: "marks_percentage",
        label: "Minimum Educational Qualification (MEQ) Marks ≥ 60%",
        pass: true,
        evidence: {
          document: "PMSS 2023-24.pdf",
          page: 2,
          section: "Clause 3: Minimum Educational Qualification (MEQ)",
          quote: "MEQ for entry into technical courses: Minimum 60% marks in MEQ.",
        },
      },
      {
        field: "annual_income",
        label: "Annual Family Income ≤ ₹6,00,000 (Base Policy)",
        pass: true,
        evidence: {
          document: "PMSS 2023-24.pdf",
          page: 3,
          section: "Clause 3(A): Eligibility — Family Income",
          quote: "Family income of the beneficiary from all sources should not exceed Rs. 6.00 Lakh per annum.",
        },
      },
    ],
  },
  {
    scheme_id: "standup_india",
    scheme_name: "Stand-Up India Scheme",
    ministry: "Ministry of Finance",
    description:
      "Bank loans between ₹10 Lakhs and ₹1 Crore to at least one SC/ST borrower and at least one woman borrower per bank branch for setting up greenfield enterprises.",
    benefit: "Composite loan between ₹10 Lakhs and ₹1 Crore",
    score: 0.85,
    eligible: true,
    application_url: "https://www.standupmitra.in",
    closing_date: "2025-03-31",
    status: "CLOSED",
    is_closed: true,
    closure_notice: "Stand-Up India scheme has closed on 31.03.2025 as officially notified on www.standupmitra.in.",
    tags: ["entrepreneurship", "business", "women-empowerment", "sc-st", "credit"],
    documents_required: [
      "Identity Proof (Aadhaar / Voter ID / Passport)",
      "Proof of Category (SC/ST Certificate or Female Gender)",
      "Project Report (Business Plan)",
      "Bank Account Statements",
    ],
    criteria: [
      {
        field: "age",
        label: "Borrower Age ≥ 18 Years",
        pass: true,
        evidence: {
          document: "StandupIndia.pdf",
          page: 3,
          section: "Clause 1: Eligibility",
          quote: "SC/ST and/or women entrepreneurs, above 18 years of age.",
        },
      },
      {
        field: "gender",
        label: "Target Beneficiary: Woman or SC/ST Entrepreneur",
        pass: true,
        evidence: {
          document: "StandupIndia.pdf",
          page: 3,
          section: "Clause 1: Objective",
          quote:
            "The objective of the Stand Up India scheme is to facilitate bank loans between 10 lakh and 1 Crore to at least one Scheduled Caste (SC) or Scheduled Tribe (ST) borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise.",
        },
      },
    ],
  },
  {
    scheme_id: "apy",
    scheme_name: "Atal Pension Yojana (APY)",
    ministry: "Ministry of Finance",
    description:
      "Guaranteed minimum monthly pension of ₹1,000 to ₹5,000 to unorganized sector workers after age 60.",
    benefit: "Monthly pension of ₹1,000 to ₹5,000 based on contribution",
    score: 0.70,
    eligible: false,
    application_url: "https://www.npscra.nsdl.co.in",
    tags: ["pension", "social-security", "financial-inclusion", "senior-citizen"],
    documents_required: ["Aadhaar Card", "Active Savings Bank Account", "Mobile Number"],
    criteria: [
      {
        field: "age",
        label: "Entry Age ≥ 18 Years",
        pass: true,
        evidence: {
          document: "APY.pdf",
          page: 3,
          section: "Clause A.10: GOI APY Guidelines",
          quote: "Adhere to any notification issued by Government of India on APY, including minimum entry age of 18 years.",
        },
      },
      {
        field: "age",
        label: "Entry Age ≤ 40 Years",
        pass: true,
        evidence: {
          document: "APY.pdf",
          page: 3,
          section: "Clause A.10: GOI APY Guidelines",
          quote: "Adhere to any notification issued by Government of India on APY, including maximum entry age of 40 years.",
        },
      },
      {
        field: "occupation",
        label: "Unorganized Sector Worker (Not Full-Time Student)",
        pass: false,
        evidence: {
          document: "APY.pdf",
          page: 1,
          section: "Clause 1: Target Beneficiaries",
          quote: "APY is focused on all citizens in the unorganized sector who are not covered under statutory social security schemes.",
        },
      },
    ],
  },
];
