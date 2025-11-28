# Kasparro — Agentic Facebook Performance Analyst

An AI-powered multi-agent system for analyzing Facebook ads performance data and generating actionable insights. Built with Google Gemini AI, this system uses five specialized agents to analyze ad performance, validate insights, and generate creative recommendations.

## Overview

Kasparro is a production-ready agentic system that automates Facebook ads analysis through a sophisticated multi-agent architecture. It processes historical ad data, identifies performance patterns, validates insights with statistical rigor, and generates data-driven creative recommendations.

### Key Features

- **Multi-Agent Architecture**: 5 specialized AI agents working in coordinated phases
- **Automated Analysis**: Converts natural language queries into comprehensive reports
- **Statistical Validation**: Built-in evaluator ensures insight quality and confidence
- **Creative Generation**: AI-generated ad concepts based on validated insights
- **Full Observability**: Detailed execution logs and performance traces
- **Production Ready**: Error handling, fallback responses, and robust data processing

## Quick Start

```bash
# 1. Check Python version
python -V  # should be >= 3.10

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
copy .env.example .env
# Edit .env and add: GEMINI_API_KEY=your_actual_key_here

# 5. Run analysis
python run.py "Analyze ROAS trends in last 7 days"

# Note: If you get ModuleNotFoundError, activate the virtual environment first:
# .venv\Scripts\activate
# python run.py "Your query here"

# Run analysis with different queries
python run.py "Compare Image vs Video ad performance"
```

## Project Structure

```
kaspora/
├── src/
│   ├── agents/
│   │   ├── planner_agent.py      # Breaks queries into analysis plans
│   │   ├── data_agent.py         # Queries and filters CSV data
│   │   ├── insight_agent.py      # Generates insights using Gemini AI
│   │   ├── evaluator_agent.py    # Validates insights for quality
│   │   └── creative_agent.py     # Generates ad creative concepts
│   ├── orchestrator/
│   │   └── agent_graph.py        # Coordinates agent workflow
│   └── utils/
│       ├── data_loader.py        # CSV data loading and parsing
│       ├── prompt_manager.py     # Prompt template management
│       └── logger.py             # Execution logging and traces
├── config/
│   └── config.yaml               # Model and system configuration
├── prompts/
│   ├── planner_agent.md          # Planner agent system prompt
│   ├── data_agent.md             # Data agent instructions
│   ├── insight_agent.md          # Insight generation prompt
│   ├── evaluator_agent.md        # Validation criteria
│   └── creative_agent.md         # Creative generation prompt
├── data/
│   └── synthetic_fb_ads_undergarments.csv  # 4500 rows of ad data
├── tests/
│   ├── test_agents.py            # Agent unit tests
│   └── test_evaluator.py         # Evaluator validation tests
├── reports/                      # Generated analysis outputs
├── logs/                         # Execution traces
├── run.py                        # Main entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Agent Architecture

![Data Flow Diagram](data/data_flow_diagram.png)

### Phase 1: Planning & Data Loading

**1. Planner Agent** (`planner_agent.py`)
- Converts natural language queries into structured analysis plans
- Defines objectives, steps, and data requirements
- Provides fallback plans if API unavailable

**2. Data Agent** (`data_agent.py`)
- Loads and processes CSV data (no LLM required)
- Performs filtering, aggregation, and comparisons
- Calculates metrics: ROAS, CTR, CPC, CPA
- Handles date ranges and period comparisons

### Phase 2: Insight Generation & Validation

**3. Insight Agent** (`insight_agent.py`)
- Analyzes data patterns using Gemini AI
- Generates hypotheses about performance
- Provides evidence and confidence scores
- Identifies trends, anomalies, and opportunities

**4. Evaluator Agent** (`evaluator_agent.py`)
- Validates each insight across 4 dimensions:
  - Evidence Quality (data completeness)
  - Statistical Validity (sample size, significance)
  - Actionability (can it drive decisions?)
  - Business Relevance (impact on KPIs)
- Filters out low-confidence insights
- Only passes insights with >60% overall score

### Phase 3: Creative Generation

**5. Creative Agent** (`creative_agent.py`)
- Generates new ad concepts based on validated insights
- Specifies format, platform, audience, and messaging
- Includes test budgets and success metrics
- Provides A/B testing strategies

## Configuration

Edit `config/config.yaml`:

```yaml
# Model Configuration
model: "gemini-1.5-flash"         # Gemini model to use
temperature: 0.7                   # Creativity (0.0-1.0)
max_tokens: 2000                   # Max response length

# Analysis Parameters
confidence_min: 0.6                # Minimum insight confidence
data_path: "data/synthetic_fb_ads_undergarments.csv"

# Observability (optional)
langfuse:
  enabled: false
  public_key: ""
  secret_key: ""
```

## Example Queries

```bash
# Performance Analysis
python run.py "Analyze ROAS trends in last 7 days"
python run.py "Which creative types have highest ROAS?"

# Comparative Analysis
python run.py "Compare Image vs Video ad performance"
python run.py "Facebook vs Instagram performance comparison"

# Trend Analysis
python run.py "Why is CTR declining on Instagram?"
python run.py "Identify top performing audience segments"

# Optimization
python run.py "Which campaigns need budget reallocation?"
python run.py "Find high-spend low-ROAS campaigns"

# Creative Insights
python run.py "What messaging resonates best with our audience?"
python run.py "Suggest improvements for underperforming ads"
```

## Sample Output

### Console Output
```
============================================================
Kasparro - Agentic Facebook Ads Analyst
============================================================

Query: Analyze ROAS trends in last 7 days

[PHASE 1] Planning & Data Loading
------------------------------------------------------------
  [1] Creating analysis plan...
      [OK] Plan created (0.5s)
      Objective: Analyze ROAS performance trends...

  [2] Loading and analyzing data...
      [OK] Data loaded (0.02s)
      Rows: 4500, ROAS: 5.83

[PHASE 2] Insight Generation & Validation
------------------------------------------------------------
  [3] Generating insights...
      [OK] Generated 5 insights (1.2s)

  [4] Evaluating insights...
      [OK] Validated 3/5 insights (0.8s)

[PHASE 3] Creative Generation
------------------------------------------------------------
  [5] Generating creative concepts...
      [OK] Generated 4 creative concepts (1.1s)

[DONE] Analysis Complete!
============================================================
```

### Generated Files

**reports/analysis_report_[timestamp].md**
- Executive summary with key metrics
- Period-over-period comparisons
- Validated insights with evidence
- Quality scores for each insight
- Creative recommendations with test budgets
- A/B testing strategies

**reports/insights_[timestamp].json**
```json
{
  "query": "Analyze ROAS trends",
  "timestamp": "2025-11-27T23:00:00",
  "insights": [
    {
      "insight": {
        "title": "Video ads outperform Images by 200%",
        "description": "Video creative achieved 8.5 ROAS...",
        "confidence": 0.89,
        "evidence": { ... }
      },
      "evaluation": {
        "overall_score": 0.87,
        "passed": true,
        "scores": {
          "evidence_quality": 0.92,
          "statistical_validity": 0.85,
          "actionability": 0.88,
          "business_relevance": 0.83
        }
      }
    }
  ]
}
```

**reports/creatives_[timestamp].json**
```json
{
  "creative_concepts": [
    {
      "headline": "New Year Sale: 50% Off",
      "format": "Video",
      "platform": "Facebook",
      "target_audience": "Women 25-45",
      "test_budget": 500,
      "expected_roas": 6.5
    }
  ]
}
```

**logs/execution_[timestamp].json**
- Complete execution trace
- Agent inputs/outputs
- Timing for each step
- Error logs (if any)

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_evaluator.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## How It Works

### 1. User Query Processing
User submits a natural language query → Planner creates structured analysis plan

### 2. Data Collection
Data Agent loads CSV → Filters by date ranges → Aggregates by dimensions → Calculates metrics

### 3. Insight Generation
Insight Agent receives data → Analyzes patterns → Generates hypotheses → Provides evidence

### 4. Quality Validation
Evaluator scores each insight → Checks statistical validity → Filters low-confidence insights

### 5. Creative Generation
Creative Agent takes validated insights → Generates ad concepts → Specifies test parameters

### 6. Report Generation
System compiles markdown report → Saves JSON outputs → Logs execution trace

## API Key Setup

1. Get your free Gemini API key:
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Create new API key

2. Add to `.env` file:
```env
GEMINI_API_KEY=AIza...your_actual_key_here
```

3. Verify setup:
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('GEMINI_API_KEY')[:10] + '...')"
```

## Dependencies

```
google-generativeai>=0.3.0  # Gemini AI SDK
pandas>=2.0.0               # Data processing
pyyaml>=6.0                 # Configuration
python-dotenv>=1.0.0        # Environment variables
langfuse>=2.0.0             # Observability (optional)
pytest>=7.4.0               # Testing
pytest-cov>=4.1.0           # Coverage reporting
```

## Troubleshooting

### Issue: "API key not valid"
**Solution**: Check that your `.env` file has a real Gemini API key (not the placeholder)

### Issue: "Module not found"
**Solution**: Activate virtual environment and reinstall dependencies
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: "No output files"
**Solution**: Check that `reports/` and `logs/` directories exist
```bash
mkdir reports logs
```

### Issue: Unicode encoding errors
**Solution**: Already fixed! All emojis replaced with ASCII characters for Windows compatibility

## Assignment Completion

### Implemented Features

- [DONE] Multi-agent architecture (5 agents)
- [DONE] Agent orchestration with AgentGraph
- [DONE] Google Gemini AI integration
- [DONE] Data loading and processing (Pandas)
- [DONE] Prompt template management
- [DONE] Insight generation and validation
- [DONE] Creative concept generation
- [DONE] Comprehensive reporting (Markdown + JSON)
- [DONE] Execution logging and observability
- [DONE] Error handling and fallback responses
- [DONE] Unit tests for agents
- [DONE] Configuration management (YAML)
- [DONE] Documentation (README, docstrings)

### Data Analysis Capabilities

- Period-over-period comparisons (7 vs 7 days, custom ranges)
- Metric aggregation (ROAS, CTR, CPC, CPA, Revenue, Spend)
- Dimensional analysis (Creative Type, Platform, Country, Audience)
- Top/bottom performer identification
- Trend detection and anomaly identification
- Statistical validation of insights

### Creative Generation Features

- Data-driven concept generation
- Platform-specific recommendations (Facebook, Instagram)
- Format optimization (Image, Video, Carousel, UGC)
- Audience targeting suggestions
- Test budget allocation
- Success metrics and KPIs

## Development Notes

**Technology Stack:**
- Language: Python 3.13
- AI Model: Google Gemini 1.5 Flash
- Data: Pandas + CSV
- Testing: pytest
- Environment: Virtual environment (.venv)

**Design Patterns:**
- Multi-agent system architecture
- Orchestrator pattern (AgentGraph)
- Prompt template management
- Fallback and error handling
- Modular utilities

**Code Quality:**
- Type hints throughout
- Comprehensive docstrings
- Error handling at all levels
- Logging and observability
- Unit test coverage

## System Status

**Current Version:** Production Ready (v1.0)

[COMPLETE] All agents implemented and tested  
[COMPLETE] Full workflow orchestration  
[COMPLETE] Comprehensive error handling  
[COMPLETE] Report generation working  
[COMPLETE] Windows compatibility verified  
[COMPLETE] Unit tests passing  
[COMPLETE] Documentation complete  

**Ready for:** Production use, assignment submission, further development

## License

MIT License - Free to use for educational and commercial purposes

## Acknowledgments

Built as part of AI-powered marketing analytics assignment. Uses synthetic Facebook ads data for demonstration purposes.

---

**Contact:** For questions or issues, please refer to the documentation or submit an issue.

**Last Updated:** November 27, 2025
#   k a s p a r r o - a g e n t i c - f b - a n a l y s t - M u k e s h - S a h u 
 
 
