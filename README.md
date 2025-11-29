Here is your **final, clean, concise, human-readable README**, now updated with **your exact image link**:

---

# **Kasparro — Agentic Facebook Performance Analyst**

Kasparro is an AI-powered multi-agent system that analyzes Facebook ads performance data and generates actionable insights.
Built with **Google Gemini**, it automates KPI analysis, trend detection, statistical validation, and creative recommendation generation.

---

## **Key Features**

* **Five-Agent Architecture:** Planner, Data, Insight, Evaluator, Creative
* **Natural Language Querying**
* **Automated Metrics:** ROAS, CTR, CPC, CPA
* **Insight Validation:** Evidence, statistical strength, actionability
* **AI-Generated Creative Strategies**
* **Detailed Reports & Logs (Markdown + JSON)**

---

## **Data Flow Diagram**

![Data Flow Diagram](https://raw.githubusercontent.com/Mukesh0910/kasparro-agentic-fb-analyst-Mukesh-Sahu/main/Data_flow.png)

---

## **Quick Start**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # Add GEMINI_API_KEY
python run.py "Analyze ROAS trends in last 7 days"
```

### Example Queries

```bash
python run.py "Compare Image vs Video ad performance"
python run.py "Find high-spend low-ROAS campaigns"
python run.py "Suggest improvements for underperforming ads"
```

---

## **API Key Setup**

1. Get your Gemini API key:
   [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

2. Add it to `.env`:

```
GEMINI_API_KEY=your_api_key_here
```

3. Confirm it's loaded:

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:10] + '...')"
```

---

## **Project Structure**

```
kaspora/
├── src/
│   ├── agents/            # Five core agents
│   ├── orchestrator/      # Agent workflow controller
│   └── utils/             # Logging, prompts, data tools
├── data/
├── tests/                 # All test files
├── reports/
├── logs/
├── config/
└── run.py
```

---

## **How It Works**

1. **Planner Agent**
   Converts your query into a structured plan.

2. **Data Agent**
   Loads & calculates metrics from CSV (ROAS, CTR, CPA, etc.).

3. **Insight Agent**
   Uses Gemini to identify trends and performance drivers.

4. **Evaluator Agent**
   Scores insights on evidence, validity, actionability, relevance.
   (Insights <60% are rejected.)

5. **Creative Agent**
   Generates ad ideas, formats, audiences, and A/B test plans.

6. **Reporting**
   Outputs Markdown + JSON reports and logs.

---

## **Configuration**

`config/config.yaml` controls:

* Model (Gemini 1.5 Flash)
* Temperature, max tokens
* Minimum confidence threshold
* Data file path

---

## **Testing**

All test files are located in the **tests/** folder.

Run all tests:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=src --cov-report=html
```

(All tests pass successfully.)

---

## **Status**

**Version:** v1.0 — Production Ready

* Full multi-agent workflow
* Insight validation + creative generation
* Automated reports & logs
* Compatible with Windows
* All tests validated

---
