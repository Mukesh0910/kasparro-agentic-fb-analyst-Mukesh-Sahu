Here is the **complete, clean, final one-shot README.md** including the **Data Flow Diagram**:

---

# **Kasparro — Agentic Facebook Ads Performance Analyst**

Kasparro is a production-ready, multi-agent AI system for analyzing Facebook advertising data.
Powered by Google Gemini, it automates KPI analysis, discovers performance insights, validates them statistically, and generates actionable creative recommendations.

---

## **Features**

* **Five-Agent Architecture:** Planner, Data, Insight, Evaluator, Creative
* **Natural-Language Querying**
* **Automated Metric Computation (ROAS, CTR, CPC, CPA)**
* **Statistical Insight Validation**
* **Creative Concept & A/B Test Generation**
* **Full Reporting (Markdown + JSON) and Logging**

---

## **Quick Start**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # Add GEMINI_API_KEY
python run.py "Analyze ROAS trends in last 7 days"
```

Example queries:

```bash
python run.py "Compare Image vs Video ad performance"
python run.py "Identify low-ROAS high-spend campaigns"
python run.py "Suggest improvements for underperforming ads"
```

---

## **Project Structure**

```
src/
  agents/ (planner, data, insight, evaluator, creative)
  orchestrator/
  utils/
reports/
logs/
config/
data/
run.py
```

---

## **Data Flow Diagram**

![Data Flow Diagram](https://raw.githubusercontent.com/Mukesh0910/kasparro-agentic-fb-analyst-Mukesh-Sahu/main/Data_flow.png)

---

## **Pipeline Overview**

1. **Planner** → Converts query into analysis plan
2. **Data Agent** → Loads & computes metrics
3. **Insight Agent** → Finds trends & anomalies
4. **Evaluator** → Scores insights & filters low confidence
5. **Creative Agent** → Generates ad concepts & testing ideas
6. **Reports** → Produces Markdown + JSON outputs

---

## **Configuration**

`config/config.yaml` includes:

* model (Gemini 1.5 Flash)
* temperature, max tokens
* insight confidence threshold
* data path

---

## **Testing**

```bash
pytest -v
pytest --cov=src --cov-report=html
```

---

## **Status**

**Version:** v1.0
Fully stable, production-ready, with complete multi-agent workflow and test coverage.
