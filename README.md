# **Kasparro — Agentic Facebook Performance Analyst**

Kasparro is an AI-powered multi-agent system that analyzes Facebook Ads performance and produces actionable insights.
Built with **Google Gemini**, it automates KPI analysis, trend detection, statistical validation, and creative recommendation generation.

---

## **Key Features**

* **Five-Agent Architecture:** Planner • Data • Insight • Evaluator • Creative
* **Natural Language Querying:** e.g., “Compare Image vs Video ads”
* **Automated Metrics:** ROAS, CTR, CPC, CPA, Revenue, Spend
* **Validated Insights:** Evidence quality, statistical validity, actionability, business relevance
* **AI-Generated Creative Strategies:** Formats, audiences, test budgets, A/B test plans
* **Full Reporting:** Markdown + JSON outputs
* **Logging & Traces:** Stored in `/logs`

---

## **Data Flow Diagram**

![Data Flow Diagram](https://raw.githubusercontent.com/Mukesh0910/kasparro-agentic-fb-analyst-Mukesh-Sahu/main/Data_flow.png)

---

## **Quick Start**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
# Add: GEMINI_API_KEY=your_api_key_here

python run.py "Analyze ROAS trends in last 7 days"
```

### Example Queries

```bash
python run.py "Compare Image vs Video ad performance"
python run.py "Find high-spend low-ROAS campaigns"
python run.py "Suggest improvements for underperforming ads"
python run.py "Why is CTR declining?"
```

---

## **API Key Setup**

1. Get your Gemini API key: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Add it to `.env`:

```
GEMINI_API_KEY=your_api_key_here
```

3. Verify it loaded:

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:10] + '...')"
```

---

## **Project Structure**

```
kaspora/
├── src/
│   ├── agents/            # Planner, Data, Insight, Evaluator, Creative
│   ├── orchestrator/      # Agent workflow controller
│   └── utils/             # Logging, prompts, data tools
├── config/
├── data/
├── tests/                 # Unit tests
├── reports/               # Generated reports
├── logs/                  # Execution traces
└── run.py
```

---

## **How It Works**

1. **Planner Agent:** Converts natural-language queries into structured analysis plans.
2. **Data Agent:** Loads CSV data, filters by dates, computes metrics (ROAS, CTR, CPC, CPA).
3. **Insight Agent:** Uses Gemini to identify trends, anomalies, and opportunities.
4. **Evaluator Agent:** Validates insights on evidence, statistical validity, actionability, and business relevance.
5. **Creative Agent:** Generates ad concepts, formats, audiences, test budgets, and A/B testing strategies.
6. **Reporting:** Produces Markdown and JSON outputs, plus logs in `/logs`.

---

## **Generated Reports**

After running a query, Kasparro automatically creates detailed reports in `/reports`:

* **Markdown Report:** `analysis_report_[timestamp].md`
  Includes:

  * Executive summary
  * Key metrics (ROAS, CTR, CPC, CPA)
  * Top-performing ads/segments
  * Validated insights with evidence and confidence
  * Recommended creative strategies and test budgets
  * Actionable notes

* **JSON Outputs:**

  * `insights_[timestamp].json` → validated insights
  * `creatives_[timestamp].json` → AI-generated ad concepts

**Example:**

```bash
python run.py "Analyze ROAS trends in last 7 days"
# -> reports/analysis_report_2025-11-29_2300.md
# -> reports/insights_2025-11-29_2300.json
# -> reports/creatives_2025-11-29_2300.json
```

---

## **Configuration**

Edit `config/config.yaml`:

```yaml
model: "gemini-1.5-flash"
temperature: 0.7
max_tokens: 2000
confidence_min: 0.6
data_path: "data/synthetic_fb_ads_undergarments.csv"
```

---

## **Testing**

All test files are located in **tests/**.

Run all tests:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=src --cov-report=html
```

---

## **Status**

**Version:** v1.0 — Production Ready

* Full multi-agent pipeline
* Insight validation & creative generation
* Automated reports & logs
* Windows-compatible
* All tests passing
* Complete documentation

---
