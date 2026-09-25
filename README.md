> **Hackathon Prototype Notice:** CiviQ was built as a 24-hour project for Smart India Hackathon 2026.
> This repository is a working prototype. It currently includes a limited set of government scheme PDFs
> (6 gazettes covering key central schemes) as a proof of concept. All features demonstrated here are functional and tested against real official government documents.

---

<div align="center">

# CiviQ
### Policy Intelligence for Every Indian

**Smart India Hackathon 2026 &mdash; 24-Hour Prototype &mdash; Team Ravens**

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-6.0-646CFF?logo=vite&logoColor=white)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![Gemini](https://img.shields.io/badge/Gemini-3.5_Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev)
[![Tavily](https://img.shields.io/badge/Tavily-Policy_Drone-FF6B35?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PC9zdmc+)](https://tavily.com)
[![Tests](https://img.shields.io/badge/Tests-96%20Passing-22C55E?logo=pytest&logoColor=white)](./backend/tests)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

> **"myScheme tells you what you qualify for. CiviQ tells you *why* &mdash; and the moment a policy
> is updated on PIB, CiviQ already knows how it changes your eligibility and your money."**

</div>

---

## Table of Contents

- [What is CiviQ?](#what-is-civiq)
- [The Problem We Solve](#the-problem-we-solve)
- [The Core Innovation - Tavily Live Policy Tracking](#the-core-innovation---tavily-live-policy-tracking)
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

---

## What is CiviQ?

CiviQ is an **AI-powered civic intelligence platform** that connects Indian citizens to the government
welfare schemes they deserve &mdash; with evidence, transparency, and personalised financial impact
analysis that updates automatically the moment a policy changes on the official Press Information Bureau.

India has **4000+ active government welfare schemes**: scholarships, pensions, subsidies, health
insurance, startup loans, maternity benefits. The vast majority of eligible citizens never access them.
Not because the schemes don't exist &mdash; but because no one told them the rules changed, the
stipend increased, or the income ceiling was just relaxed to include them.

CiviQ fixes this at the source. The moment the Cabinet announces a welfare revision on PIB, CiviQ:

1. Detects the announcement autonomously via Tavily Search API
2. Extracts exactly what changed (which parameter, old value, new value)
3. Re-evaluates every citizen profile against the new rules
4. Tells the affected citizen: *"You are now eligible"* or *"You receive Rs. 7,200 more per year"*

No manual data entry. No waiting 3-6 months for a government webmaster to update a portal.
Policy intelligence, the moment it is official.

---

## The Problem We Solve

| Failure Point | How CiviQ Fixes It |
|:---|:---|
| Citizens do not know the scheme exists | Personalised scheme matching from a structured rule database |
| Eligibility rules are dense legal jargon | Every criterion explained in plain language with the exact gazette clause |
| No way to verify if you truly qualify | Deterministic Python evaluation &mdash; no AI guessing, pure math |
| Policy changed but no one was notified | Tavily autonomously monitors PIB and triggers instant re-evaluation |
| Static portals lag 3-6 months behind Cabinet decisions | PIB press releases are discovered the day they are published |
| WhatsApp forwards spreading fake schemes | Myth Buster with deterministic verdict and official PIB Fact Check citations |
| Wrong links, broken portals | Verified official `.gov.in` apply links |

---

## Features

### 1. Real-Time Policy Updates via Tavily

The moment a new scheme version is published on PIB, `auto_updater.py` detects it, extracts what
changed, and re-evaluates citizen eligibility. No manual refresh. No waiting for a portal to catch up.

### 2. Evidence Drawer &mdash; Every Answer Has a Receipt

A slide-out panel showing the official gazette document name, page number, clause number, and verbatim
quoted text for every eligibility criterion. Opens the raw government PDF inline. Zero fabricated
citations &mdash; if the clause does not exist in the gazette, the system says so.

### 3. Policy Compare &mdash; What Changed?

Side-by-side diff table comparing old and new versions of a scheme. Shows each parameter, its
before/after values, and whether the change increased, relaxed, or tightened the criteria.

**Example &mdash; PMSS 2023-24 vs 2026-27:**

| Criterion | Before | After | Change |
|---|---|---|---|
| Stipend (Girls) | Rs. 3,000/month | Rs. 3,600/month | Increased (+20%) |
| Income Ceiling | Rs. 6,00,000/yr | Rs. 8,00,000/yr | Relaxed (more people qualify) |

### 4. Personalised Impact Card

Connects every policy change to the specific citizen's profile. Tells them in one sentence exactly
what the amendment means for their money or eligibility.

> *"Because of the 2024 revision, you now receive Rs. 7,200 more per year."*

### 5. Visual Reasoning Tree

Interactive decision tree showing every eligibility criterion for a scheme. Green = PASS, Red = FAIL.
Click any node to open the Evidence Drawer showing the exact gazette clause that created that rule.

### 6. Ask CiviQ &mdash; Chat with Government Policy

Free-text Q&A over all official gazette PDFs via Gemini long-context RAG. Every answer includes
collapsible citation drawers (document, page, clause, verbatim quote). Temperature locked at 0.2
for strict factual fidelity.

### 7. Myth Buster &mdash; WhatsApp Scam Debunker

Paste any viral WhatsApp claim about a government scheme. Deterministic fuzzy + semantic matching
against `data/myths.json` returns a verdict with real facts and official PIB Fact Check citations.

**Example:** *"Modi giving Rs. 50,000 to all farmers"* -> **FAKE** &mdash; PM-KISAN gives
Rs. 6,000/year to landholding farmers. Source: Ministry of Agriculture, Page 2.

### 8. Multilingual Support (EN / HI / TA / TE)

Language switcher with a 3-tier translation engine:
1. In-memory dictionary cache (sub-millisecond)
2. Google Cloud Translation v2 API
3. Gemini vernacular fallback

### 9. Mock DigiLocker Onboarding

One-click "Import from DigiLocker" with Aadhaar OTP consent modal. Pre-populates citizen profile
instantly with demo personas. Clearly labelled as a prototype flow &mdash; real integration is Phase 2.

### 10. Live Portal Status Check

`GET /api/v1/schemes/{id}/live-check` verifies official portal operational status. Stand-Up India
is flagged as `CLOSED` (officially sunset on 31.03.2025) and the apply button is replaced with
an official closure notice.

---

## The Core Innovation - Tavily Live Policy Tracking

This is what separates CiviQ from every existing civic platform, including the official `myScheme.gov.in`.

### The Problem with Static Policy Portals

When the Union Cabinet approves a welfare amendment &mdash; a stipend increase, an income ceiling
relaxation, a new eligibility category &mdash; it is announced the same day on the
**Press Information Bureau** (`pib.gov.in`). But the journey from that announcement to an updated
government portal takes **3 to 6 months** of bureaucratic processing.

During this window, an eligible citizen who checks `myScheme.gov.in` gets told they do not qualify
&mdash; because the portal is running on outdated data. CiviQ skips the queue entirely.

### How Tavily Solves This

The Tavily Search API is not a standard web crawler. A standard crawler follows hyperlinks &mdash; it
can only find pages that are explicitly linked from somewhere. Tavily performs **AI-native semantic
search** across official government domains, capable of discovering press releases, circular annexures,
and gazette notifications the moment they appear, even before any portal links to them.

CiviQ uses Tavily as an **autonomous policy drone**:

```
Every scheme has a Tavily watcher
        |
        v
Tavily queries pib.gov.in, pmindia.gov.in, scholarships.gov.in, pmkisan.gov.in, etc.
        |
        v
New PIB press release detected for PM Scholarship (PRID: 2110356)
        |
        v
Gemini extracts structured diff from the press release text:
  { parameter: "Stipend (Girls)", old: "Rs. 3,000/mo", new: "Rs. 3,600/mo" }
  { parameter: "Income Ceiling",  old: "Rs. 6,00,000", new: "Rs. 8,00,000" }
        |
        v
evaluator.py re-runs BEFORE the change:
  Citizen with Rs. 7,20,000 income -> NOT_ELIGIBLE
        |
        v
evaluator.py re-runs AFTER the change:
  Citizen with Rs. 7,20,000 income -> ELIGIBLE
        |
        v
Citizen alert generated:
  "The income ceiling for PM Scholarship was just raised.
   You are now eligible. Apply before November 15."
```

### Zero-Trust Domain Whitelisting

Tavily is never allowed to ingest content from unofficial sources. Every URL returned by Tavily is
passed through a strict domain validator before any content is processed:

```python
# Only these domains are ever trusted
ALLOWED_DOMAINS = [
    "pib.gov.in",        # Press Information Bureau
    "pmindia.gov.in",    # PMO India
    "scholarships.gov.in",
    "pmkisan.gov.in",
    "mha.gov.in",
    "education.gov.in",
    "msme.gov.in",
    "egazette.gov.in",
    "gov.in",
    "nic.in"
]

# Any URL not ending in .gov.in or .nic.in is silently rejected
def is_allowed(url: str) -> bool:
    host = urlparse(url).hostname or ""
    return host.endswith(".gov.in") or host.endswith(".nic.in")
```

Commercial blogs, affiliate pages, SEO-optimised "scheme guides", and phishing portals are blocked
at the ingestion layer. If the information did not come from a verified government domain, CiviQ
does not use it.

### The 4-Stage Auto-Update Pipeline

Implemented in `backend/ai_engine/auto_updater.py` and `backend/ai_engine/tavily_tracker.py`:

| Stage | What Happens |
|:---|:---|
| **1. Discovery** | `TavilyPolicyTracker` searches PIB and ministry domains for the latest scheme revision |
| **2. Diff Extraction** | Gemini parses the unstructured press release text and outputs a structured JSON diff |
| **3. Re-Evaluation** | `evaluator.py` runs the citizen's profile through the old rules, then the new rules. Detects exact eligibility flips |
| **4. Impact Alert** | Calculates the annual rupee gain delta and generates a plain-language citizen alert |

### Verified PIB Sources (Built-In Fallback)

`CANONICAL_SCHEME_NOTIFICATIONS` in `tavily_tracker.py` contains verified PIB press release IDs for
all canonical schemes, used as a fault-tolerant fallback when live Tavily queries are unavailable:

| Scheme | Verified PIB PRID |
|---|---|
| PM Scholarship (WARB) | `pib.gov.in/PressReleasePage.aspx?PRID=2110356` |
| PM-KISAN | `pib.gov.in/PressReleasePage.aspx?PRID=2242295` |
| PMEGP | `pib.gov.in/PressReleasePage.aspx?PRID=2079789` |
| Atal Pension Yojana | `pib.gov.in/PressReleasePage.aspx?PRID=2204271` |
| Stand-Up India | `standupmitra.in` (closure notice) |

---

## The Core Principle - Zero Hallucination

> **"AI explains and answers. Code decides."**

This is enforced architecturally &mdash; not just as a convention.

```
+-------------------------------------------------------------------+
|  ELIGIBILITY DECISION  ->  evaluator.py  (pure Python math)       |
|  ==, !=, >, >=, <, <=, in  --  zero AI, zero hallucination       |
+-------------------------------------------------------------------+
|  EXPLANATION / ANSWER  ->  Gemini 3.5 Flash  (RAG over PDFs)     |
|  Strictly reads official gazettes  |  temperature = 0.2           |
+-------------------------------------------------------------------+
|  POLICY DIFF DETECTION ->  Tavily + Gemini extraction             |
|  Tavily finds the source  |  Gemini reads it  |  Python decides   |
+-------------------------------------------------------------------+
|  MYTH VERDICT          ->  myth_checker.py (fuzzy keyword match)  |
|  Deterministic  |  same input = same output, always              |
+-------------------------------------------------------------------+
```

A government benefit decision must be reproducible and auditable. If a citizen asks
*"why am I not eligible?"*, CiviQ can show the exact rule, the exact field, the exact operator,
and the exact threshold &mdash; all derived from verified government data.
An AI answer can never provide that level of accountability.

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
                          ^
                          |  Autonomous discovery
+-----------------------------------------------------------------------+
|  TAVILY POLICY DRONE                                                   |
|  Monitors pib.gov.in, pmindia.gov.in, scholarships.gov.in, etc.       |
|  Triggers auto_updater.py the moment a new circular is published       |
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
| **Tavily Search API** | Advanced | Autonomous PIB circular discovery on `*.gov.in` / `*.nic.in` |
| **Supabase** | 2.10.0+ | Cloud PostgreSQL for citizen profiles |
| **Google Cloud Translation** | v2 REST | Primary translation tier (Gemini fallback) |
| **Pytest** | 8.0+ | 96 automated unit and integration tests |

> **Total infrastructure cost: Rs. 0** &mdash; all free-tier or open-source tools.

---

## Project Structure

```
civiq-sih2026/
|
+-- backend/
|   +-- ai_engine/                    # Intelligence core
|   |   +-- evaluator.py              # Deterministic eligibility engine (pure Python math)
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
    +-- raw_pdfs/                     # Official government gazette PDFs (prototype subset)
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

# Required for live policy tracking
TAVILY_API_KEY=tvly-your_tavily_key_here

# Optional - cloud profile persistence
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# Optional
ENVIRONMENT=development
```

> **Never commit `.env` to git.** It is in `.gitignore`. Exposing an API key causes immediate revocation.

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

### 4. Run the Tavily policy pipeline demo

```bash
python backend/scripts/demo_auto_update.py
```

This runs the full 4-stage pipeline live in the terminal:

1. Scans PIB for PMSS 2026-27 revision
2. Extracts structured parameter diffs via Gemini
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
| `POST` | `/comparator` | Policy version diff + personalised rupee impact |
| `POST` | `/ask` | Gemini RAG Q&A over gazette PDFs with verbatim citations |
| `POST` | `/myths/check` | Myth verdict (TRUE / FALSE / PARTIALLY TRUE / UNVERIFIED) + PIB advisory |
| `POST` | `/translate` | Translate text to HI / TA / TE and other Indian languages |
| `POST` | `/policy/auto-update` | **Tavily pipeline:** discovery -> Gemini diff -> re-evaluation -> citizen alert |
| `GET` | `/policy/freshness-feed` | Stream of recently discovered PIB circulars |
| `GET` | `/documents/{filename}` | Streams official gazette PDF inline (application/pdf) |
| `GET` | `/health` | Health check: `{"status": "ok", "version": "1.0.0"}` |

### Example: ProfileSchema (sent to `/match`)

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

### Example: AutoUpdateResponse (from `/policy/auto-update`)

```json
{
  "scheme_id": "pmss",
  "pib_url": "https://pib.gov.in/PressReleasePage.aspx?PRID=2110356",
  "circular_headline": "Cabinet approves enhanced stipend for CAPF wards under PM Scholarship",
  "parameter_diffs": [
    { "parameter": "Stipend (Girls)", "old_value": "Rs. 3,000/month", "new_value": "Rs. 3,600/month" },
    { "parameter": "Income Ceiling",  "old_value": "Rs. 6,00,000/yr", "new_value": "Rs. 8,00,000/yr" }
  ],
  "eligibility_before": "NOT_ELIGIBLE",
  "eligibility_after": "ELIGIBLE",
  "annual_gain_rupees": 7200,
  "citizen_alert": "The income ceiling for PM Scholarship was just raised. You are now eligible."
}
```

---

## Data and Government PDFs

> **Prototype scope:** This repository includes 6 official gazette PDFs covering key central schemes.
> The full production system would ingest all 3,000+ national and state schemes, with Tavily
> continuously monitoring PIB for new revisions across every ministry.

All eligibility rules are derived **exclusively** from official government documents.

| PDF File | Scheme | Ministry |
|:---|:---|:---|
| `APY.pdf` | Atal Pension Yojana | Ministry of Finance / PFRDA |
| `PM-KISAN.pdf` | PM Kisan Samman Nidhi | Ministry of Agriculture |
| `PMEGP.pdf` | PM Employment Generation Programme | Ministry of MSME / KVIC |
| `PMSS 2023-24.pdf` | PM Scholarship Scheme (Base version) | Ministry of Home Affairs (WARB) |
| `PMSS 2026-27.pdf` | PM Scholarship Scheme (Revised version) | Ministry of Home Affairs (WARB) |
| `StandupIndia.pdf` | Stand Up India (CLOSED 31.03.2025) | Ministry of Finance / SIDBI |

- `data/schemes_extracted.json` &mdash; Canonical structured rule database for all supported schemes.
- `data/myths.json` &mdash; 15 curated fake WhatsApp scheme claims with official verdicts and PIB citations.

---

### Frontend production build

```bash
cd frontend
npm run build
# 1605 modules transformed in 2.62 seconds - zero warnings
```

---

## How It Was Built - The 24-Hour Hackathon Story

CiviQ was designed, built, and tested entirely from scratch in a single **24-hour sprint** for
Smart India Hackathon 2026.

### Why We Built It

The best existing tool was `myScheme.gov.in` &mdash; a government portal that tells you *what*
you qualify for. But it shows no reasoning, no proof, no policy change tracking, and lags months
behind Cabinet decisions. AI assistants can answer questions but hallucinate eligibility decisions
and have no access to verified government data.

The problem we were actually solving was not "help people find schemes". It was
**"help people know the moment a scheme changes, before any portal does"**. That is what Tavily enabled.

### The Tavily Strategy Call

We built and tested the full Tavily pipeline during the hackathon. But we deliberately chose
**not** to run live Tavily queries during judging &mdash; the risk of rate limits or network
latency during a timed demo was too high. Instead:

- Core prototype runs on verified gazette PDFs and deterministic evaluation &mdash; fully stable.
- `CANONICAL_SCHEME_NOTIFICATIONS` provides verified PIB PRIDs as a built-in fallback.
- The full Tavily production engine is demonstrated via `demo_auto_update.py` and presented
  in the slide deck as the Phase 2 production scaling path.

---

## Whats Next Phase 2

The core architecture is already built for production scale. What is needed is deployment
and government API partnerships:

| Feature | Description |
|:---|:---|
| **Full Tavily Production Pipeline** | Autonomous ingestion scaling from 6 prototype PDFs to all 4,000+ national and state schemes |
| **Real DigiLocker Integration** | Auto-import Aadhaar, marksheets, income certificates via official NSDL API |
| **Nightly Gazette Re-index** | All PDFs automatically re-indexed as ministries publish new circulars |
| **Civic Life-Stage Timeline** | Tells you what documents and schemes to get at 18, 21, first job, marriage, 60+ |
| **Voice Input** | Speak in Hindi, Telugu, etc. and get an answer in your language |
| **Push Notifications** | WhatsApp/SMS alerts when a scheme you qualify for changes or closes |
| **Mobile App** | React Native version of CiviQ |
| **State Government API** | State governments can plug CiviQ into their own citizen portals |

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

---

## License

Built as part of Smart India Hackathon 2026. Released under the [MIT License](LICENSE).

---

<div align="center">

*CiviQ &mdash; Policy Intelligence for Every Indian*

*24-Hour Hackathon Prototype &middot; SIH 2026 &middot; Team Ravens*

</div>
