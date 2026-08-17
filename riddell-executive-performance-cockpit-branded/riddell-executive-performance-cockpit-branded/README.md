
# Riddell Executive Performance Cockpit

A GitHub-ready, Riddell-branded Streamlit prototype for an **AI-powered executive performance intelligence experience**.

This mockup is designed around the Riddell discussion covering:

- 45 prioritized enterprise KPIs
- Six business process areas
- Executive KPI trends
- Exception-first monitoring
- AI-generated business narratives
- KPI drill-down and root-cause storytelling
- Cross-process performance connections
- Natural-language investigation
- KPI lineage, formula, owner, source, and trust metadata

> **Important:** This repository uses simulated/demo data only. Replace it with validated Riddell data before any production or customer decision-making use.

---

## Screens

### 1. Executive Cockpit
A concise enterprise view showing:
- KPI health
- Process-level pulse
- KPIs requiring attention
- AI executive brief
- Trends
- Top business exceptions

### 2. KPI Story
Turns a single KPI into a business story:
- What changed
- How far from target
- What is driving the change
- Where the impact sits
- Suggested investigation
- KPI definition

### 3. Cross-Process Story
Shows how one issue can propagate across:
- Procurement
- Manufacturing
- Fulfillment
- Finance

### 4. Ask Riddell
A natural-language UX with deterministic demo answers.

The production version can be connected to Azure OpenAI or another approved LLM and grounded against governed enterprise data.

### 5. KPI Trust Card
Shows:
- Definition
- Formula
- Source
- Owner
- Refresh cadence
- Benchmark
- Data quality
- Example lineage

---

## Project Structure

```text
riddell-executive-performance-cockpit/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── Dockerfile
│
├── .streamlit/
│   └── config.toml
│
└── data/
    ├── kpis.csv
    ├── kpi_trends.csv
    ├── otif_drivers.csv
    ├── otif_impact.csv
    └── cross_process_story.csv
```

---

## Run Locally

### 1. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Streamlit

```bash
streamlit run app.py
```

Streamlit will display the local URL in the terminal.

---

## Push to GitHub

```bash
git init
git add .
git commit -m "Initial Riddell executive performance cockpit"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

---

## Deploy

This repo is structured so that it can be deployed on a standard Streamlit hosting environment.

Use:

- **Main file:** `app.py`
- **Python dependencies:** `requirements.txt`

Do not commit secrets.

---

## Connecting Azure OpenAI Later

The current **Ask Riddell** screen intentionally uses deterministic sample responses so the prototype works immediately.

A production pattern would look like:

```text
Executive UX
    ↓
Context / Query Orchestrator
    ↓
KPI Semantic Layer
    ↓
Structured Enterprise Data
    ↓
Azure OpenAI
    ↓
Grounded narrative with evidence
```

Recommended grounding inputs:

1. KPI definition
2. KPI formula
3. target / benchmark
4. actual trend
5. dimensions available for drill-down
6. supporting operational data
7. source lineage
8. data quality metadata
9. user permissions

The LLM should explain and synthesize the evidence, not become the source of the KPI itself.

---

## Suggested Production Architecture

```text
                       RIDDELL EXECUTIVE UX
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
       Executive Cockpit    KPI Stories      Ask Riddell
              │                 │                 │
              └─────────────────┼─────────────────┘
                                │
                         CONTEXT / AI LAYER
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
        KPI Context       Business Context      Evidence
              │                 │                 │
              └─────────────────┼─────────────────┘
                                │
                         SEMANTIC KPI MODEL
                                │
              Definitions • Formulas • Owners
              Targets • Benchmarks • Relationships
                                │
                                ▼
                    ENTERPRISE DATA PLATFORM
                                │
                  SAP / Fabric / Other Sources
```

---

## POC Strategy

Instead of implementing all 45 KPIs initially, select **one meaningful KPI from each business process**.

The strongest demo will use six KPIs that create a connected story rather than six unrelated measures.

Example:

```text
Supplier performance
        ↓
Component availability
        ↓
Production schedule adherence
        ↓
Fulfillment / OTIF
        ↓
Revenue or margin exposure
```

That allows Riddell leadership to see the value of moving from:

**Dashboard → Explanation → Business connection → Action**

---

## Disclaimer

All values, KPI names, benchmarks, causes, supplier counts, product groups, business impacts, and AI narratives in this repository are illustrative mock data unless specifically validated against Riddell source systems.


---

## Riddell Branding Included

- Actual Riddell logo in the header and sidebar
- Riddell red `#C8102E` as the primary brand accent
- Black/charcoal, white, and neutral-gray application palette
- Riddell logo used as the Streamlit page icon
- Corporate red kept separate from semantic KPI health colors
- Logo asset stored at `assets/riddell-logo.png`
