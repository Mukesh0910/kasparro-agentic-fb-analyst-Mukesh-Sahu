# **Kasparro — Agentic Facebook Performance Analyst**

Kasparro is an AI-powered multi-agent system designed to analyze Facebook Ads performance and produce actionable insights.
Built with **Google Gemini**, it automates KPI analysis, trend detection, statistical validation, and creative recommendation generation.

---

## **Key Features**

* **Five-Agent Architecture**
  Planner • Data • Insight • Evaluator • Creative
* **Natural Language Querying**
  “Compare image vs video ads”, “Find low-ROAS campaigns”, etc.
* **Automated Performance Metrics**
  ROAS, CTR, CPC, CPA, Spend, Revenue
* **Validated Insights**
  Evidence quality, statistical strength, business relevance
* **AI-Generated Creative Strategies**
  Complete with formats, audiences, and A/B test plans
* **Full Reporting**
  JSON + Markdown output inside `/reports`
* **Logging & Traces**
  Stored in `/logs`

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

### Additional Query Examples

```bash
python run.py "Compare Image vs Video ad performance"
python run.py "Find high-spend low-ROAS campaigns"
python run.py "Suggest improvements for underperforming ads"
python run.py "Why is CTR declining?"
```

---

## **API Key Setup**

1. Get your Gemini API key
   [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

2. Add it to your `.env` file:

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
│   └── utils/             # Logging, prompts, data loading
├── config/
├── data/
├── tests/                 # Unit tests for agents + evaluator
├── reports/               # Generated analysis outputs
├── logs/                  # Execution traces
└── run.py
```

---

## **How It Works**

### **1. Planner Agent**

Translates natural-language queries into structured analysis plans.

### **2. Data Agent**

Loads CSV data, filters by date ranges, and computes metrics (ROAS, CTR, CPC, CPA).

### **3. Insight Agent**

Gemini analyzes patterns, trends, anomalies, and opportunities.

### **4. Evaluator Agent**

Validates each insight on:

* Evidence quality
* Statistical validity
* Actionability
* Business relevance

Insights scoring **<60%** are rejected.

### **5. Creative Agent**

Generates platform-ready ad concepts, audiences, formats, and test budgets.

### **6. Reporting**

Creates:

* `analysis_report_[timestamp].md`
* `insights_[timestamp].json`
* `creatives_[timestamp].json`
* Execution logs

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

All test files are located in the **tests/** folder.

Run all tests:

```bash
pytest -v
```

With coverage:

```bash
pytest --cov=src --cov-report=html
```

---

## **Status**

**Version:** v1.0
**State:** Production Ready

* Full multi-agent pipeline
* Insight validation & creative generation
* Robust error handling
* Windows-compatible
* All tests passing
* Complete documentation

---
