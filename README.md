# **Kasparro — Agentic Facebook Performance Analyst**

Kasparro is an AI-powered, production-ready multi-agent system for analyzing Facebook advertising data and generating actionable insights.
Built on Google Gemini AI, Kasparro combines five specialized agents to process historical performance data, validate insights statistically, and produce data-driven creative recommendations.

Overview

Kasparro automates end-to-end Facebook ads analysis using a coordinated multi-agent architecture. It ingests structured datasets, identifies performance patterns, evaluates insight quality, and generates creative concepts optimized for your marketing objectives.

Key Features

Five-Agent Architecture: Planner, Data, Insight, Evaluator, and Creative agents

Automated Natural Language Analysis

Statistical Insight Validation

Creative Concept Generation

Robust Observability & Logging

Production-Ready Workflow (error handling, fallbacks, configuration management)

Quick Start
# 1. Check Python version (>= 3.10)
python -V

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Add your GEMINI_API_KEY in .env

# 5. Run analysis
python run.py "Analyze ROAS trends in last 7 days"


To run additional queries:

python run.py "Compare Image vs Video ad performance"

Project Structure
kaspora/
├── src/
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── data_agent.py
│   │   ├── insight_agent.py
│   │   ├── evaluator_agent.py
│   │   └── creative_agent.py
│   ├── orchestrator/
│   │   └── agent_graph.py
│   └── utils/
│       ├── data_loader.py
│       ├── prompt_manager.py
│       └── logger.py
├── config/
├── prompts/
├── data/
├── tests/
├── reports/
├── logs/
├── run.py
└── requirements.txt

## **Data Flow Diagram**

![Data Flow Diagram](https://raw.githubusercontent.com/Mukesh0910/kasparro-agentic-fb-analyst-Mukesh-Sahu/main/Data_flow.png)


Agent Architecture

Phase 1: Planning & Data Collection

Planner Agent

Converts natural-language queries into structured analysis plans

Defines objectives, steps, and data requirements

Offers fallback strategies if the LLM is unavailable

Data Agent

Loads, filters, and aggregates CSV data

Computes ROAS, CTR, CPC, CPA, and more

Handles date ranges and comparative periods

Phase 2: Insight Generation & Validation

Insight Agent

Identifies trends, anomalies, and performance drivers

Uses Gemini AI for pattern recognition

Produces evidence-backed insights with confidence estimates

Evaluator Agent

Assesses insights on 4 dimensions:

Evidence Quality

Statistical Validity

Actionability

Business Relevance

Rejects low-confidence insights (<60% score)

Phase 3: Creative Generation

Creative Agent

Generates ad concepts based on validated insights

Recommends formats, audiences, messaging, and budgets

Includes A/B testing frameworks and expected performance metrics

Configuration

config/config.yaml:

model: "gemini-1.5-flash"
temperature: 0.7
max_tokens: 2000

confidence_min: 0.6
data_path: "data/synthetic_fb_ads_undergarments.csv"

langfuse:
  enabled: false
  public_key: ""
  secret_key: ""

Example Queries
# Performance
python run.py "Analyze ROAS trends in last 7 days"
python run.py "Which creative types have the highest ROAS?"

# Comparisons
python run.py "Compare Image vs Video ad performance"

# Trends
python run.py "Why is CTR declining on Instagram?"

# Optimization
python run.py "Identify low-ROAS high-spend campaigns"

# Creative
python run.py "Suggest improvements for underperforming ads"

Sample Output
Console Output
============================================================
Kasparro - Agentic Facebook Ads Analyst
============================================================

Query: Analyze ROAS trends in last 7 days

[PHASE 1] Planning & Data Loading
  [OK] Plan created
  [OK] Data loaded (4500 rows)

[PHASE 2] Insight Generation & Validation
  [OK] Generated 5 insights
  [OK] 3 insights validated

[PHASE 3] Creative Generation
  [OK] Produced 4 creative concepts

[DONE] Analysis Complete
============================================================

Output Files

reports/analysis_report_[timestamp].md

Executive summary, KPI snapshots

Validated insights & evidence

Creative recommendations and testing plans

reports/insights_[timestamp].json
Contains structured insights, evaluation scores, and evidence.

reports/creatives_[timestamp].json
Creative concepts with audiences, formats, budgets, and expected ROAS.

logs/execution_[timestamp].json
Complete step-by-step execution trace.

Testing
python -m pytest tests/ -v
python -m pytest tests/test_evaluator.py -v
python -m pytest tests/ --cov=src --cov-report=html

How Kasparro Works

Query Interpretation → Planner generates analysis plan

Data Processing → Data Agent loads and computes metrics

Insight Generation → Insight Agent analyzes patterns via Gemini

Validation → Evaluator filters weak insights

Creative Ideation → Creative Agent proposes new ad concepts

Reporting → System produces Markdown + JSON outputs with logs

API Key Setup

Get a Gemini API key from makersuite.google.com/app/apikey

Update .env:

GEMINI_API_KEY=AIza...your_key_here


Validate:

python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:10] + '...')"

Dependencies
google-generativeai>=0.3.0
pandas>=2.0.0
pyyaml>=6.0
python-dotenv>=1.0.0
langfuse>=2.0.0
pytest>=7.4.0
pytest-cov>=4.1.0

Troubleshooting

"API key not valid"
Check .env and ensure a real Gemini API key is present.

"Module not found"
Activate the virtual environment and reinstall dependencies.

.venv\Scripts\activate
pip install -r requirements.txt


Missing output files
Ensure reports/ and logs/ directories exist.

Unicode issues (Windows)
All emoji have been removed; no additional action required.

Development Notes

Tech Stack: Python 3.13, Gemini 1.5 Flash, Pandas, pytest
Design Patterns: Multi-agent orchestration, modular prompts, error-tolerant execution
Quality: Full type hints, docstrings, extensive logging, unit test coverage

System Status

Version: v1.0 — Production Ready
All agents, workflows, tests, and documentation are complete and validated.

License

MIT License — free for educational and commercial use.

Acknowledgments

Developed as part of an AI-driven marketing analytics project using synthetic Facebook ad data.


