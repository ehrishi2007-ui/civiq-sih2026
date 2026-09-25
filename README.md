<div align="center">

# CiviQ
### Policy Intelligence for Every Indian

**Built in 24 hours for Smart India Hackathon 2026 &mdash; Team Ravens**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-6.0-646CFF?logo=vite&logoColor=white)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Gemini](https://img.shields.io/badge/Gemini-3.5_Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev)
[![Tests](https://img.shields.io/badge/Tests-96%20Passing-22C55E?logo=pytest&logoColor=white)](./backend/tests)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

> **"myScheme tells you what you qualify for. CiviQ tells you *why* &mdash; and shows you when a policy change started mattering to your life."**

</div>

---

## Table of Contents

- [What is CiviQ?](#what-is-civiq)
- [The Problem We Solve](#the-problem-we-solve)
- [The Core Principle - Zero Hallucination](#the-core-principle---zero-hallucination)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Data and Government PDFs](#data-and-government-pdfs)
- [Running Tests](#running-tests)
- [How It Was Built - The 24-Hour Hackathon Story](#how-it-was-built---the-24-hour-hackathon-story)
- [Whats Next Phase 2](#whats-next-phase-2)
- [Team](#team)

---

## What is CiviQ?

CiviQ is an **AI-powered civic intelligence platform** that connects Indian citizens to the government welfare schemes they deserve &mdash; with evidence, transparency, and personalised financial impact analysis.

India has **3,000+ active government welfare schemes**: scholarships, pensions, subsidies, health insurance, startup loans, maternity benefits. The vast majority of eligible citizens never access them. CiviQ changes that.

Unlike any existing tool, CiviQ does not just match you to a scheme &mdash; it:

- **Shows you WHY** you qualify using a visual reasoning tree
- **Proves every answer** with the exact page and clause from the official government gazette PDF
- **Shows what changed** between old and new policy versions
- **Tells you exactly** how that change affects *your* money
- **Debunks WhatsApp scams** about fake government schemes

Everything is grounded in official government documents. Nothing is made up.

---

## The Problem We Solve

| Failure Point | How CiviQ Fixes It |
|:---|:---|
| Citizens do not know the scheme exists | Personalised scheme matching from a canonical database |
| Eligibility rules are dense legal jargon | Visual reasoning tree explains every criterion in plain language |
| No way to verify if you truly qualify | Deterministic Python evaluation &mdash; no AI guessing, pure math |
| Wrong links, broken portals | Verified official `.gov.in` apply links, manually checked |
| Policy changed but no one told you | Autonomous PIB monitoring via Tavily + policy diff engine |
| WhatsApp forwards spreading fake schemes | Myth Buster with deterministic verdict + PIB Fact Check citations |

---

## The Core Principle - Zero Hallucination

> **"AI explains and answers. Code decides."**

This is the single most important architectural decision in CiviQ and it is **enforced in code, not convention**.

```
+-------------------------------------------------------------------+
|  ELIGIBILITY DECISION  ->  evaluator.py  (pure Python math)       |
|  ==, !=, >, >=, <, <=, in  --  zero AI, zero hallucination       |
+-------------------------------------------------------------------+
|  EXPLANATION / ANSWER  ->  Gemini 3.5 Flash  (RAG over PDFs)     |
|  Strictly reads official gazettes  |  temperature = 0.2           |
+-------------------------------------------------------------------+
|  POLICY DIFF           ->  comparator.py + Gemini extraction      |
|  Gemini extracts  |  Python computes the rupee delta              |
+-------------------------------------------------------------------+
|  MYTH VERDICT          ->  myth_checker.py (fuzzy keyword match)  |
|  Deterministic  |  same input = same output, always              |
+-------------------------------------------------------------------+
```

In public welfare, an AI hallucination is catastrophic. A fabricated income limit or imagined age threshold can cause an impoverished citizen to travel to government offices only to be rejected, or miss benefits entirely. CiviQ is designed so it is architecturally impossible for Gemini to return an eligibility verdict.

---

## Features

### 1. Reasoning Tree &mdash; The Core Innovation

Instead of a binary eligible/not-eligible result, CiviQ renders an **interactive visual decision tree**. Every eligibility criterion for a scheme is a node. Green = PASS, Red = FAIL. Click any node to see the exact line from the exact government PDF that created that rule.

### 2. Evidence Drawer &mdash; Every Answer Has a Receipt

A slide-out panel showing the official gazette document name, page number, clause number, and verbatim quoted text. Opens the raw government PDF inline. Zero fabricated citations &mdash; if the source does not exist in the gazette, the system says so.

### 3. Policy Compare &mdash; What Changed?

Side-by-side diff table comparing old and new versions of a scheme. Shows each parameter, its before/after values, and whether the change increased, relaxed, or tightened the criteria.

**Example &mdash; PMSS 2023-24 vs 2026-27:**

| Criterion | Before | After | Change |
|---|---|---|---|
| Stipend (Girls) | Rs. 3,000/month | Rs. 3,600/month | Increased (+20%) |
| Income Ceiling | Rs. 6,00,000/yr | Rs. 8,00,000/yr | Relaxed (more people qualify) |

### 4. Personalised Impact Card

Connects every policy change to the specific citizen's profile. Tells them in one sentence exactly what the amendment means for their money or eligibility.

> *"Because of the 2024 revision, you now receive Rs. 7,200 more per year."*

### 5. Ask CiviQ &mdash; Chat with Government Policy

Free-text Q&A over all official gazette PDFs via Gemini long-context RAG. Every answer includes collapsible citation drawers (document, page, clause, verbatim quote). Temperature locked at 0.2 for strict factual fidelity.

### 6. Myth Buster &mdash; WhatsApp Scam Debunker

Paste any viral WhatsApp claim about a government scheme. The myth checker normalises the text (strips currency symbols, deceptive keywords), runs fuzzy + semantic matching against `data/myths.json`, and returns a deterministic verdict with real facts and official PIB citations.

**Example:** *"Modi giving Rs. 50,000 to all farmers"* -> **FAKE** &mdash; PM-KISAN gives Rs. 6,000/year to landholding farmers. Source: Ministry of Agriculture, Page 2.

### 7. Multilingual Support (EN / HI / TA / TE)

Language switcher in the Navbar. 3-tier translation engine:

1. In-memory dictionary cache (sub-millisecond)
2. Google Cloud Translation v2 API
3. Gemini vernacular fallback

Language preference persists in `localStorage`. Translation results are cached &mdash; same strings are never translated twice.

### 8. Mock DigiLocker Onboarding

One-click "Import from DigiLocker" button with an Aadhaar OTP consent modal and 1.5-second spinner simulation. Pre-populates the full citizen profile instantly. Three demo personas: Priya Sharma (CAPF student), Ramesh Patel (farmer), Anita Devi (entrepreneur). Clearly labelled as a demo/mock flow &mdash; real integration is Phase 2.

### 9. Verified Apply Links

Every scheme card has a direct "Apply Now" button linking to the verified official `.gov.in` application portal. No third-party aggregators. All links manually verified.

### 10. Deadline Alert Banner

Dashboard banner showing any eligible scheme closing within 30 days, with the exact deadline and a direct apply link. Driven by the `deadline` field in `data/schemes_extracted.json`.

### 11. Autonomous Policy Ingestion (Tavily)

`tavily_tracker.py` + `auto_updater.py` form a 4-stage pipeline:

1. Discovers latest PIB circulars via Tavily Search API (restricted to `*.gov.in` / `*.nic.in`)
2. Extracts structured parameter diffs via Gemini
3. Re-runs `evaluator.py` before vs after the amendment (detects eligibility flips)
4. Computes the annual rupee gain and generates a citizen alert

### 12. Live Portal Status Check

`GET /api/v1/schemes/{id}/live-check` verifies official portal operational status in real time. Stand-Up India is flagged as `CLOSED` (officially sunset on 31.03.2025) and its apply action is replaced with a closure warning.

---

## System Architecture

```
+-----------------------------------------------------------------------+
|  LAYER 4 - SCREEN  (React 18 + Vite 6 + Tailwind CSS)                |
|  Home | ProfileWizard | Dashboard | SchemeDetail | AskChat | Myths    |
+-----------------------------------------------------------------------+
                          |
                    HTTP  |  localhost:5173  ->  localhost:8000
                          |
+-----------------------------------------------------------------------+
|  LAYER 3 - API BRIDGE  (FastAPI + Uvicorn)                            |
|  /profile  /match  /schemes  /comparator  /ask  /myths                |
|  /translate  /policy/auto-update  /documents/{filename}               |
+-----------------------------------------------------------------------+
                          |
               Python fn  |  calls
                          |
+-----------------------------------------------------------------------+
|  LAYER 2 - BRAIN  (backend/ai_engine/)                                |
|  evaluator.py    rag.py         comparator.py    myth_checker.py      |
|  tavily_tracker.py  auto_updater.py  translator.py  pdf_service.py    |
+-----------------------------------------------------------------------+
                          |
                   reads  |
                          |
+-----------------------------------------------------------------------+
|  LAYER 1 - DATA VAULT  (data/)                                        |
|  raw_pdfs/  |  schemes_extracted.json  |  myths.json                  |
|  Gemini File API (uploaded_files.json)  |  Supabase (PostgreSQL)      |
+-----------------------------------------------------------------------+
```

---

## Tech Stack

| Technology | Version | Role |
|:---|:---|:---|
| **React** | 18.3.1 | Frontend SPA &mdash; all 6 pages and components |
| **Vite** | 6.0+ | Build tool &mdash; full production build in 2.62 seconds |
| **Tailwind CSS** | 3.4.15 | Utility-first styling |
| **Lucide React** | 0.460.0 | SVG icon set |
| **React Router** | 6.28.0 | Client-side routing |
| **Python** | 3.12+ | Backend runtime |
| **FastAPI** | 0.110.0+ | Async REST API with auto OpenAPI docs |
| **Pydantic** | v2 | Strict runtime type validation |
| **Uvicorn** | 0.28.0+ | ASGI server |
| **Google GenAI SDK** | v2.0+ | Gemini 3.5 Flash Lite for RAG and translation |
| **Gemini File API** | Cloud | Indexes official gazette PDFs with persistent URI cache |
| **Tavily Search API** | Advanced | Autonomous PIB circular discovery on `*.gov.in` |
| **Supabase** | 2.10.0+ | Cloud PostgreSQL for citizen profiles |
| **Google Cloud Translation** | v2 REST | Primary translation tier (with Gemini fallback) |
| **Pytest** | 8.0+ | 96 automated unit and integration tests |

> **Total infrastructure cost: Rs. 0** &mdash; all free-tier or open-source tools.

---

## Project Structure

```
civiq-sih2026/
|
+-- backend/
|   +-- ai_engine/                    # Intelligence core
|   |   +-- evaluator.py              # CORE: Deterministic eligibility engine (pure Python math)
|   |   +-- rag.py                    # Gemini RAG over official gazette PDFs
|   |   +-- comparator.py             # Policy version diff engine (rupee delta calculator)
|   |   +-- myth_checker.py           # WhatsApp scam debunker (fuzzy keyword match)
|   |   +-- tavily_tracker.py         # Autonomous PIB circular discovery engine
|   |   +-- auto_updater.py           # 4-stage citizen impact simulator
|   |   +-- translator.py             # 3-tier multilingual localization engine
|   |   +-- pdf_service.py            # Gemini File API lifecycle manager
|   |   +-- vector_store.py           # PDF chunking and vector index management
|   |   +-- db_client.py              # Supabase PostgreSQL client
|   |   +-- schemas.py                # Shared AI engine data models
|   |   +-- uploaded_files.json       # Gemini File API persistent URI cache
|   |
|   +-- api/                          # FastAPI web server
|   |   +-- main.py                   # App factory, CORS, PDF streaming endpoint
|   |   +-- config.py                 # Pydantic-Settings environment config
|   |   +-- schemas.py                # API request/response Pydantic v2 models
|   |   +-- routes/
|   |       +-- schemes.py            # POST /match | GET /schemes/{id} | live-check
|   |       +-- profile.py            # POST /profile
|   |       +-- ask.py                # POST /ask (Gemini RAG Q&A)
|   |       +-- myths.py              # POST /myths/check
|   |       +-- comparator.py         # POST /comparator
|   |       +-- translate.py          # POST /translate
|   |       +-- policy.py             # POST /policy/auto-update | GET /freshness-feed
|   |
|   +-- tests/                        # 96 automated tests
|   |   +-- test_api.py               # 13 tests
|   |   +-- test_evaluator.py         # 26 tests
|   |   +-- test_comparator.py        #  9 tests
|   |   +-- test_myth_checker.py      # 10 tests
|   |   +-- test_pdf_service.py       #  9 tests
|   |   +-- test_rag.py               # 10 tests
|   |   +-- test_translator_and_db.py # 13 tests
|   |   +-- test_tavily_auto_update.py#  6 tests
|   |
|   +-- scripts/
|   |   +-- demo_auto_update.py       # Terminal demo of the 4-stage auto-update pipeline
|   |
|   +-- requirements.txt
|   +-- .env                          # <- NEVER committed to git
|
+-- frontend/                         # React application
|   +-- src/
|   |   +-- App.jsx                   # Root router + context providers
|   |   +-- pages/
|   |   |   +-- Home.jsx
|   |   |   +-- ProfileWizard.jsx     # 4-step builder + DigiLocker modal
|   |   |   +-- Dashboard.jsx         # Scheme cards, match %, deadline alerts
|   |   |   +-- SchemeDetail.jsx      # Reasoning tree, diff table, impact card, PDF viewer
|   |   |   +-- AskChat.jsx           # Conversational policy Q&A
|   |   |   +-- MythBuster.jsx        # WhatsApp scam checker
|   |   +-- components/
|   |   |   +-- Navbar.jsx
|   |   |   +-- ReasoningTree.jsx     # Interactive SVG eligibility decision tree
|   |   |   +-- EvidenceDrawer.jsx    # Slide-out PDF clause inspector
|   |   |   +-- DiffTable.jsx         # Old vs new policy comparison table
|   |   |   +-- ImpactCard.jsx        # Personalised rupee gain card
|   |   |   +-- SchemeCard.jsx
|   |   |   +-- DigiLockerModal.jsx
|   |   |   +-- LanguageSelector.jsx  # EN / HI / TA / TE dropdown
|   |   +-- context/
|   |   |   +-- ProfileContext.jsx    # Global citizen profile state
|   |   |   +-- LanguageContext.jsx   # Global i18n state
|   |   +-- services/
|   |   |   +-- api.js                # HTTP client with zero-crash offline fallback
|   |   |   +-- schemeService.js
|   |   |   +-- askService.js
|   |   |   +-- mythService.js
|   |   |   +-- profileService.js
|   |   |   +-- translateService.js
|   |   +-- mock/
|   |       +-- digilocker_data.js    # Demo personas (Priya, Ramesh, Anita)
|   |       +-- schemes.js
|   |       +-- myths.js
|   |       +-- diffData.js
|   |       +-- translations.js
|   |       +-- schemeTranslations.js
|   +-- package.json
|   +-- vite.config.js
|   +-- tailwind.config.js
|
+-- data/
    +-- raw_pdfs/
    |   +-- APY.pdf
    |   +-- PM-KISAN.pdf
    |   +-- PMEGP.pdf
    |   +-- PMSS 2023-24.pdf          # "before" version for policy diff demo
    |   +-- PMSS 2026-27.pdf          # "after" version for policy diff demo
    |   +-- StandupIndia.pdf          # flagged CLOSED: 31.03.2025
    +-- schemes_extracted.json        # Canonical scheme rules database
    +-- myths.json                    # 15 curated fake WhatsApp claim verdicts
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- A Gemini API key (free at [ai.google.dev](https://ai.google.dev))

### 1. Clone the repository

```bash
git clone https://github.com/your-org/civiq-sih2026.git
cd civiq-sih2026
```

### 2. Backend setup

```bash
cd backend

# Create and activate virtual environment
python -m venv .venv

# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create `backend/.env`:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - autonomous policy ingestion
TAVILY_API_KEY=tvly-your_tavily_key_here

# Optional - cloud profile persistence
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# Optional
ENVIRONMENT=development
```

> **Never commit `.env` to git.** It is listed in `.gitignore`. Exposing an API key causes immediate revocation.

Start the backend server:

```bash
uvicorn api.main:app --reload --port 8000
```

| URL | What it is |
|---|---|
| `http://127.0.0.1:8000` | API root |
| `http://127.0.0.1:8000/docs` | Swagger UI (interactive API explorer) |
| `http://127.0.0.1:8000/redoc` | ReDoc (clean API documentation) |

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173`

### 4. (Optional) Terminal demo of the autonomous policy pipeline

```bash
python backend/scripts/demo_auto_update.py
```

This runs the full 4-stage pipeline live in the terminal:

1. Scans PIB for PMSS 2026-27 revision
2. Extracts structured parameter diffs
3. Simulates citizen eligibility flip (`NOT_ELIGIBLE` -> `ELIGIBLE`)
4. Calculates `+Rs. 7,200/yr` financial gain delta

---

## API Reference

Base URL: `http://127.0.0.1:8000/api/v1`

| Method | Endpoint | Description |
|:---|:---|:---|
| `POST` | `/profile` | Save citizen profile to Supabase (local session fallback if DB unavailable) |
| `POST` | `/match` | Match profile against all schemes; returns sorted list with match % scores |
| `GET` | `/schemes/{id}` | Full scheme metadata, criteria, required documents, citations |
| `GET` | `/schemes/{id}/live-check` | Real-time portal status; flags Stand-Up India CLOSED since 31.03.2025 |
| `POST` | `/comparator` | Policy version diff (PMSS 2023-24 vs 2026-27) + personalised rupee impact |
| `POST` | `/ask` | Gemini RAG Q&A over gazette PDFs with verbatim citations |
| `POST` | `/myths/check` | Myth verdict (TRUE / FALSE / PARTIALLY TRUE / UNVERIFIED) + PIB advisory |
| `POST` | `/translate` | Translate text to HI / TA / TE and other Indian languages |
| `POST` | `/policy/auto-update` | Tavily discovery -> Gemini diff -> re-evaluation -> citizen alert |
| `GET` | `/policy/freshness-feed` | Stream of recently discovered PIB circulars |
| `GET` | `/documents/{filename}` | Streams official gazette PDF inline (application/pdf) |
| `GET` | `/health` | Health check: `{"status": "ok", "version": "1.0.0"}` |

### Example: ProfileSchema

```json
{
  "age": 20,
  "gender": "female",
  "category": "OBC",
  "state": "Tamil Nadu",
  "annual_income": 300000,
  "has_land": false,
  "occupation": "student",
  "is_capf_ward": true,
  "marks_percentage": 72.0
}
```

### Example: MythCheckResponse

```json
{
  "verdict": "FALSE",
  "normalized_query": "modi giving 50000 farmers",
  "pib_advisory": "PIB Fact Check: No such scheme exists.",
  "real_facts": "PM-KISAN provides Rs. 6,000/year to landholding farmers.",
  "redirect_url": "https://pmkisan.gov.in"
}
```

---

## Data and Government PDFs

All scheme data and eligibility rules are derived **exclusively** from official government documents.

| PDF File | Scheme | Ministry |
|:---|:---|:---|
| `APY.pdf` | Atal Pension Yojana | Ministry of Finance / PFRDA |
| `PM-KISAN.pdf` | PM Kisan Samman Nidhi | Ministry of Agriculture |
| `PMEGP.pdf` | PM Employment Generation Programme | Ministry of MSME / KVIC |
| `PMSS 2023-24.pdf` | PM Scholarship Scheme (Base version) | Ministry of Home Affairs (WARB) |
| `PMSS 2026-27.pdf` | PM Scholarship Scheme (Revised version) | Ministry of Home Affairs (WARB) |
| `StandupIndia.pdf` | Stand Up India | Ministry of Finance / SIDBI |

**Notes:**

- Stand-Up India officially closed on 31.03.2025. The `live-check` endpoint flags it `CLOSED` and replaces the apply button with an official closure notice.
- Both PMSS versions (2023-24 and 2026-27) are included. These two files power the Policy Diff demo &mdash; showing the stipend increase (Rs. 3,000 -> Rs. 3,600/month) and income ceiling relaxation (Rs. 6L -> Rs. 8L).
- `data/schemes_extracted.json` &mdash; canonical structured rule database for all supported schemes.
- `data/myths.json` &mdash; 15 curated fake WhatsApp scheme claims with official verdicts and PIB citations.

---

## Running Tests

```bash
cd backend
python -m pytest
# Expected: 96 passed in ~5.3 seconds
```

```bash
# Verbose output
python -m pytest -v

# Single test file
python -m pytest tests/test_evaluator.py -v
```

| Test File | Tests | What It Covers |
|:---|:---:|:---|
| `test_api.py` | 13 | FastAPI routes, profile validation, CORS headers, error schemas, PDF streaming |
| `test_evaluator.py` | 26 | All operators (==, !=, >, >=, <, <=, in), tri-state logic, boundary conditions |
| `test_comparator.py` | 9 | Policy diff logic, stipend delta calculations, conservatism guardrail |
| `test_myth_checker.py` | 10 | Query normalization, fuzzy matching, PIB verdict generation |
| `test_pdf_service.py` | 9 | Gemini File API upload idempotency, handle caching |
| `test_rag.py` | 10 | Grounded Q&A, temperature constraint (0.2), citation regex extraction |
| `test_translator_and_db.py` | 13 | Translation caching, Gemini vernacular fallback, Supabase adapters |
| `test_tavily_auto_update.py` | 6 | Zero-Trust whitelisting, Tavily search, diff extraction, eligibility flips |
| **Total** | **96** | **All passing** |

### Frontend production build

```bash
cd frontend
npm run build
# 1605 modules transformed in 2.62 seconds - zero warnings
```

---

## How It Was Built - The 24-Hour Hackathon Story

CiviQ was designed, built, and tested entirely from scratch in a single **24-hour sprint** for Smart India Hackathon 2026 by a team of 6.

### Why We Built It

The best existing tool was `myScheme.gov.in` &mdash; a government portal that tells you *what* you qualify for. But it gives no reasoning, no proof, no policy change tracking, and no way to tell real schemes from WhatsApp scams. AI assistants like ChatGPT can answer questions but hallucinate eligibility decisions and have no access to verified government data.

### How the 24 Hours Went

**Hours 0&ndash;4 &mdash; Setup and Faking It**

Dev 2 immediately returned hardcoded mock JSON from all API endpoints. This meant Dev 3 could start building the full React UI without waiting for the AI layer to be ready. The app loaded with fake data on screen by Hour 4.

**Hours 4&ndash;12 &mdash; Core Build**

Dev 1 loaded all official gazette PDFs into Gemini File API, built the rule evaluator, and wired up the RAG pipeline. Dev 2 swapped mock responses for real function calls. Dev 3 built the interactive reasoning tree and evidence drawer. The full golden path (profile -> match -> reasoning tree -> evidence) was working with real data by Hour 10.

**Hours 12&ndash;18 &mdash; Advanced Features and QA**

Myth Buster, policy diff engine, Tavily ingestion pipeline, and multilingual support were all built and wired. Feature freeze at Hour 16 &mdash; no new features after this point.

**Hours 18&ndash;24 &mdash; Pitch Mode**

Two complete dry runs. Offline cache built (stores all demo API responses so the demo works even if internet fails during judging). Team rehearsed the 2-minute demo script.

### The Key Architectural Decision

The most important decision was the strict separation between AI and eligibility logic. Early drafts explored letting Gemini decide eligibility &mdash; faster to build, but we rejected it because:

1. It is not reproducible or auditable.
2. A hallucinated income limit could cause a real citizen to miss a real benefit.
3. Any judge with a technical background would immediately question it.

The final architecture &mdash; deterministic Python evaluator for all eligibility decisions, Gemini strictly for explanation and extraction &mdash; is what makes CiviQ trustworthy rather than just impressive.

### The Tavily Decision

We designed and fully implemented the Tavily autonomous ingestion pipeline (`tavily_tracker.py` + `auto_updater.py`, 6 dedicated Pytest tests). However, we deliberately chose **not** to run live Tavily queries during judging, due to the risk of rate limits or network latency. Instead:

- Core prototype uses verified gazette PDFs and deterministic evaluation &mdash; fully stable.
- `CANONICAL_SCHEME_NOTIFICATIONS` provides verified PIB PRIDs as a fault-tolerant fallback.
- The full Tavily production engine is presented in the slide deck as the Phase 2 scaling path.

---

## Whats Next Phase 2

| Feature | Description |
|:---|:---|
| **Real DigiLocker Integration** | Auto-import Aadhaar, marksheets, income certificates via official NSDL API |
| **Civic Life-Stage Timeline** | Tells you what documents and schemes to get at 18, 21, first job, marriage, age 60+ |
| **Voice Input** | Speak in Hindi, Telugu, etc. and get an answer in your language |
| **Push Notifications** | WhatsApp/SMS alerts 30 days before scheme application deadlines |
| **Mobile App** | React Native version of CiviQ |
| **State Government API** | State governments can plug CiviQ into their own citizen portals |
| **Nightly Refresh** | All gazette PDFs automatically re-indexed as ministries publish new circulars |
| **Full Tavily Production Pipeline** | Autonomous ingestion scaling from 11 schemes to all 3,000+ national and state schemes |

---

## Team

**Team Ravens &mdash; Smart India Hackathon 2026**

| Role | Responsibility |
|:---|:---|
| **Dev 1** &mdash; AI and Data Engineer | `backend/ai_engine/` &mdash; evaluator, RAG, comparator, myth checker, Tavily, translator |
| **Dev 2** &mdash; API and Integration | `backend/api/` &mdash; FastAPI server, all endpoints, offline cache |
| **Dev 3** &mdash; Frontend Engineer | `frontend/` &mdash; all 6 pages, all components, reasoning tree, evidence drawer |
| **Researcher 1** &mdash; Policy Expert | `data/` &mdash; schemes.json, myths.json, apply link verification |
| **Researcher 2** &mdash; UX and QA Lead | UI copy, demo persona data, full QA checklist |
| **Researcher 3** &mdash; Pitch Lead | PowerPoint, demo script, dry runs, presentation |

---

## What Must Never Be Committed

```
backend/.env
frontend/.env
.venv/
node_modules/
__pycache__/
*.pyc
frontend/dist/
```

Committing `.env` exposes all API keys and causes immediate revocation by Google and Supabase.

---

## License

This project was built as part of Smart India Hackathon 2026 and is released under the [MIT License](LICENSE).

---

<div align="center">

*CiviQ &mdash; Policy Intelligence for Every Indian*

*Built in 24 hours &middot; SIH 2026 &middot; Team Ravens*

</div>
