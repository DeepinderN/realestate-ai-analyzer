# 🏠 RealEstate AI Lead Analyzer

An AI-powered lead qualification tool for real estate operations. Feed it a CSV of leads — it scores, grades, and ranks every one using Claude, then outputs a prioritized action report in seconds.

Built to eliminate the manual triage bottleneck in real estate sales pipelines.

---

## The Problem

Real estate teams waste hours manually reviewing leads that have wildly different intent, urgency, and quality. A $1.2M industrial buyer and a cold Zillow inquiry look identical in a CRM row. This tool fixes that.

---

## What It Does

- Reads a CSV of leads (name, budget, timeline, source, notes, etc.)
- Sends each lead to Claude (Anthropic) via API for AI-powered analysis
- Returns a structured assessment for every lead:
  - **Priority Score** (1–10)
  - **Lead Grade** (A / B / C / D)
  - **Intent Classification** (buyer / investor / seller / unknown)
  - **Urgency** (immediate / short-term / long-term / cold)
  - **Recommended Next Action**
  - **Risk Flags**
  - **2-Sentence Summary**
- Saves a ranked CSV report to `/output`
- Displays color-coded terminal output with a pipeline summary

---

## Demo Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🏠  RealEstate AI Lead Analyzer  |  Powered by Claude
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Loaded 8 leads from data/sample_leads.csv
  Sending to Claude for analysis...

  [1/8] Analyzing Priya Nair...     Grade A  Score 10/10 ✓
  [2/8] Analyzing Tom Nakamura...   Grade A  Score  9/10 ✓
  [3/8] Analyzing Marcus Webb...    Grade A  Score  8/10 ✓
  [4/8] Analyzing Sandra Ortiz...   Grade B  Score  6/10 ✓
  [5/8] Analyzing Angela Foster...  Grade B  Score  5/10 ✓
  [6/8] Analyzing James Thornton... Grade C  Score  4/10 ✓
  [7/8] Analyzing Derek Cole...     Grade D  Score  2/10 ✓
  [8/8] Analyzing Beth Simmons...   Grade D  Score  1/10 ✓

────────────────────────────────────────────────────────────
Lead 1/8: Priya Nair  |  Budget: $1,200,000  |  Source: Referral
  Grade:   A   Score: 10/10
  Intent:  Investor
  Urgency: Immediate
  Action:  Call today — confirm decision timeline and send industrial portfolio.
  High-value corporate relocation with immediate timeline and referral credibility.
  Decision expected end of month — this is the hottest lead in the pipeline.

════════════════════════════════════════════════════════════
PIPELINE SUMMARY
════════════════════════════════════════════════════════════
  Total leads analyzed: 8
  Grade A: ███ (3)
  Grade B: ██  (2)
  Grade C: █   (1)
  Grade D: ██  (2)

Top 3 Priority Leads:
  1. Priya Nair    — Grade A — Score 10/10 — Call today, send industrial portfolio
  2. Tom Nakamura  — Grade A — Score  9/10 — Schedule tour this week
  3. Marcus Webb   — Grade A — Score  8/10 — Send school info, close fast

  ✅ Report saved → output/lead_report_20260427_143022.csv
```

Sample output CSV: [`output/sample_output_20260427.csv`](output/sample_output_20260427.csv)

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Engine | Anthropic Claude (`claude-sonnet-4`) |
| Language | Python 3.10+ |
| Input | CSV (leads data) |
| Output | Terminal (color-coded) + CSV report |
| API Client | `anthropic` Python SDK |

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/DeepinderN/realestate-ai-analyzer
cd realestate-ai-analyzer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 4. Run it
python main.py
```

---

## Usage

```bash
# Analyze all leads in default CSV
python main.py

# Use a custom leads file
python main.py --file my_leads.csv

# Analyze only first 5 leads
python main.py --top 5
```

---

## CSV Format

Your leads file should include these columns:

| Column | Description |
|---|---|
| `lead_id` | Unique identifier |
| `name` | Lead name |
| `source` | Where lead came from (Zillow, Referral, etc.) |
| `property_type` | Single Family, Multi-Family, Industrial, etc. |
| `budget` | Budget in USD (number only) |
| `timeline` | Purchase timeline |
| `location` | City, State |
| `notes` | Agent notes / call notes |
| `days_since_contact` | Days since first touch |
| `follow_up_attempts` | Number of follow-up attempts |

See [`data/sample_leads.csv`](data/sample_leads.csv) for a full example.

---

## Extending This Tool

Some directions this can go:

- **CRM Integration** — pipe output directly into HubSpot, Salesforce, or Podio via API
- **Automated Follow-Up** — trigger email sequences based on lead grade
- **Batch Scheduling** — run nightly via cron job on new CRM exports
- **Slack Alerts** — push Grade A leads to a Slack channel instantly
- **Web Dashboard** — serve results through a FastAPI + React frontend

---

## Author

**Deepinder**
[GitHub](https://github.com/DeepinderN) · [Portfolio](https://deepinder-rishi.netlify.app/) · [LinkedIn](https://linkedin.com/in/deepinder-rishi)

---

## License

MIT
