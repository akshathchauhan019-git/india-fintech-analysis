# India Fintech Market Analysis

An in-depth analysis of India's digital payments ecosystem — covering UPI growth, market share dynamics, transaction composition, ecosystem scale, fintech funding, global penetration benchmarks, and UPI's international expansion.

Built with **Python (pandas, matplotlib)** — all charts, data, and a shareable PDF report included.

---

## Why this project

I built this to develop a working understanding of the Indian payments landscape ahead of joining **Stripe's Service Delivery Centre in Bengaluru**. It combines my interest in fintech and operations with hands-on data analysis — going from raw public data to a polished, presentation-ready report.

---

## What's covered (8 analyses, 10-page PDF report)

| # | Section | Key question answered |
|---|---|---|
| 1 | UPI Transaction Growth (2016–2025) | How fast did UPI scale, and what drove each acceleration? |
| 2 | UPI App Market Share (2021–2024) | How did PhonePe, Google Pay, and Paytm's positions evolve? |
| 3 | P2P → P2M Structural Shift | When did UPI become a merchant payments network, not just a transfer tool? |
| 4 | UPI Ecosystem Scale | Banks, merchant QR acceptance points, and registered users over time |
| 5 | Fintech Funding Landscape (2017–2024) | How did the ZIRP boom and correction play out — and by sub-sector? |
| 6 | Digital Payments Penetration | How does India compare to China, USA, and Brazil — and how fast is the gap closing? |
| 7 | UPI Goes Global | Which countries accept UPI, and what is the remittance corridor opportunity? |
| 8 | Executive Dashboard | All key metrics on one page |

---

## Key findings

- UPI scaled from **0.09M transactions/month** (Aug 2016) to **18.26 billion** (Mar 2025) — ~200,000× in under 9 years
- PhonePe + Google Pay hold **~85% of UPI volume** — an effective duopoly; Paytm fell from 11% → 6% (2021–2024)
- **P2M (merchant) payments crossed 50% of UPI volume in 2024** for the first time — driven by 390M+ merchant QR codes
- India's digital payments penetration rose from **28% (2019) → 74% (2024)**, a 21% CAGR — fastest of any major economy
- Fintech funding peaked at **$8.5B (2021)**, corrected to $2.5B (2023), and recovered to **$3.1B (2024)**
- UPI is now accepted in **22+ countries**, targeting $120B+/year in diaspora remittance corridors

---

## Output

| File | Description |
|---|---|
| `outputs/India_Fintech_Analysis_Final.pdf` | **10-page shareable PDF report** |
| `outputs/01_upi_growth.png` | Monthly volume + YoY growth + avg ticket size |
| `outputs/02_market_share.png` | Market share stacked bar + trend lines |
| `outputs/03_transaction_composition.png` | P2P vs P2M structural shift |
| `outputs/04_ecosystem_scale.png` | Banks, QR codes, registered users |
| `outputs/05_fintech_funding.png` | Annual funding + deal count + sector donut |
| `outputs/06_penetration_global.png` | Country comparison + CAGR bar |
| `outputs/07_upi_global.png` | International expansion + remittance corridors |
| `outputs/08_dashboard.png` | Executive dashboard (dark theme) |

---

## Project structure

```
india-fintech-analysis/
├── data/
│   ├── build_data.py              # Generates all CSVs from source data
│   ├── upi_monthly.csv            # NPCI monthly UPI data (Aug 2016–Mar 2025)
│   ├── market_share.csv           # UPI app share (PhonePe / GPay / Paytm)
│   ├── fintech_funding.csv        # Annual fintech VC funding
│   ├── digital_penetration.csv    # Country-level penetration (2019–2024)
│   ├── p2m_split.csv              # P2P vs P2M transaction split
│   ├── upi_ecosystem.csv          # Banks, QR codes, users (2017–2024)
│   └── upi_international.csv      # UPI international expansion milestones
├── notebooks/
│   └── India_Fintech_Market_Analysis.ipynb   # Full analysis with commentary
├── outputs/                        # All charts + final PDF report
├── build_report.py                 # Builds the 10-page PDF
└── README.md
```

---

## Run it locally

```bash
git clone https://github.com/akshathchauhan/india-fintech-analysis.git
cd india-fintech-analysis
pip install pandas matplotlib seaborn jupyter numpy

# Regenerate data CSVs
python data/build_data.py

# Build the PDF report
python build_report.py

# Or explore in the notebook
jupyter notebook notebooks/India_Fintech_Market_Analysis.ipynb
```

---

## Data sources

- **NPCI** — UPI ecosystem statistics (monthly transaction volume & value)
- **RBI** — Digital payments data and payment system reports
- **DPIIT** — Digital India metrics
- **World Bank** — Financial inclusion / digital payments penetration
- **Tracxn / Crunchbase aggregates** — Fintech funding figures

*2025 figures reflect partial-year data (Jan–Mar). International remittance figures are estimates from industry sources.*

---

**Author:** Akshath Chauhan
