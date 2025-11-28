"""
Agent Graph Orchestrator
Coordinates the flow of data between agents following the assignment spec
"""
import time
from typing import Dict, Any, List
from pathlib import Path

from ..agents.planner_agent import PlannerAgent
from ..agents.data_agent import DataAgent
from ..agents.insight_agent import InsightAgent
from ..agents.evaluator_agent import EvaluatorAgent
from ..agents.creative_agent import CreativeAgent
from ..utils.logger import ExecutionLogger
from ..utils.data_loader import load_facebook_ads_data


class AgentGraph:
    """
    Orchestrates the multi-agent workflow:
    User Query → Planner → Data → Insight → Evaluator → Creative → Report
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the agent graph with configuration"""
        self.config = config
        self.logger = ExecutionLogger()
        
        # Initialize agents
        self.planner = PlannerAgent(config)
        self.data_agent = DataAgent(config['data_path'])
        self.insight_agent = InsightAgent(config)
        self.evaluator = EvaluatorAgent(config)
        self.creative_agent = CreativeAgent(config)
    
    def execute(self, user_query: str) -> Dict[str, Any]:
        """
        Execute the full agent workflow
        
        Args:
            user_query: User's analysis query
            
        Returns:
            Dictionary with all results
        """
        print(f"\n{'='*60}")
        print(f"Kasparro - Agentic Facebook Ads Analyst")
        print(f"{'='*60}\n")
        print(f"Query: {user_query}\n")
        
        # Set up logging
        self.logger.set_metadata(
            query=user_query,
            config=self.config
        )
        
        results = {}
        
        # PHASE 1: Planning & Data Loading
        print("[PHASE 1] Planning & Data Loading")
        print("-" * 60)
        
        # Step 1: Create Plan
        print("  [1] Creating analysis plan...")
        start_time = time.time()
        plan = self.planner.create_plan(user_query)
        duration = time.time() - start_time
        
        self.logger.log_step(
            step_name="create_plan",
            agent="planner_agent",
            input_data=user_query,
            output_data=plan,
            duration=duration
        )
        
        results['plan'] = plan
        print(f"      [OK] Plan created ({duration:.2f}s)")
        print(f"      Objective: {plan.get('objective', 'N/A')[:70]}...")
        
        # Step 2: Load and Analyze Data
        print("\n  [2] Loading and analyzing data...")
        start_time = time.time()
        
        # Multi-level analysis as per assignment requirements
        data_summary = self.data_agent.get_data_summary()
        comparison = self.data_agent.compare_periods(current_days=7, previous_days=7)
        
        # Detailed level analysis
        campaign_analysis = self.data_agent.get_campaign_level_analysis()
        adset_analysis = self.data_agent.get_adset_level_analysis()
        audience_analysis = self.data_agent.get_audience_level_analysis()
        creative_analysis = self.data_agent.get_creative_level_analysis()
        geo_analysis = self.data_agent.get_geo_level_analysis()
        rolling_trends = self.data_agent.get_rolling_trends(window=7)
        
        data_results = {
            'summary': data_summary,
            'recent_trends': comparison,
            'campaign_level': campaign_analysis,
            'adset_level': adset_analysis,
            'audience_level': audience_analysis,
            'creative_level': creative_analysis,
            'geo_level': geo_analysis,
            'rolling_trends': rolling_trends,
            'top_performers': self.data_agent.get_top_performers(metric='roas', group_by='creative_type').to_dict('records')
        }
        duration = time.time() - start_time
        
        self.logger.log_step(
            step_name="analyze_data",
            agent="data_agent",
            input_data=f"Query data for: {user_query}",
            output_data=data_summary,
            duration=duration
        )
        
        results['data'] = data_results
        print(f"      [OK] Data loaded ({duration:.2f}s)")
        print(f"      Rows: {data_summary['total_rows']}, ROAS: {data_summary['overall_roas']:.2f}")
        
        # PHASE 2: Insight Generation & Validation
        print("\n[PHASE 2] Insight Generation & Validation")
        print("-" * 60)
        
        # Step 3: Generate Insights
        print("  [3] Generating insights...")
        start_time = time.time()
        
        context = f"Analysis focus: {plan.get('objective', user_query)}"
        insights = self.insight_agent.generate_insights(data_results, context)
        duration = time.time() - start_time
        
        self.logger.log_step(
            step_name="generate_insights",
            agent="insight_agent",
            input_data=data_results,
            output_data=insights,
            duration=duration
        )
        
        print(f"      [OK] Generated {len(insights)} insights ({duration:.2f}s)")
        
        # Step 4: Evaluate Insights
        print("\n  [4] Evaluating insights...")
        start_time = time.time()
        
        evaluated_insights = []
        for insight in insights:
            evaluation = self.evaluator.evaluate_insight(insight, data_results)
            evaluated_insights.append({
                'insight': insight,
                'evaluation': evaluation,
                'passed': evaluation['passed']
            })
        
        duration = time.time() - start_time
        
        self.logger.log_step(
            step_name="evaluate_insights",
            agent="evaluator_agent",
            input_data=insights,
            output_data=evaluated_insights,
            duration=duration
        )
        
        validated_count = sum(1 for ei in evaluated_insights if ei['passed'])
        results['insights'] = evaluated_insights
        print(f"      [OK] Validated {validated_count}/{len(insights)} insights ({duration:.2f}s)")
        
        # PHASE 3: Creative Generation
        print(f"\n[PHASE 3] Creative Generation")
        print("-" * 60)
        
        # Step 5: Generate Creative Recommendations
        print("  [5] Generating creative recommendations...")
        start_time = time.time()
        
        validated_insights = [ei['insight'] for ei in evaluated_insights if ei['passed']]
        creative_data = {
            'top_performers': data_results['top_performers'],
            'performance_summary': data_results['recent_trends']
        }
        
        creatives = self.creative_agent.generate_creatives(validated_insights, creative_data)
        duration = time.time() - start_time
        
        self.logger.log_step(
            step_name="generate_creatives",
            agent="creative_agent",
            input_data=validated_insights,
            output_data=creatives,
            duration=duration
        )
        
        results['creatives'] = creatives
        creative_count = len(creatives.get('creative_concepts', []))
        print(f"      [OK] Generated {creative_count} creative concepts ({duration:.2f}s)")
        
        # Save execution log
        log_path = self.logger.save()
        print(f"\n[LOG] Execution log saved: {log_path}")
        
        print(f"\n{'='*60}")
        print("[DONE] Analysis Complete!")
        print(f"{'='*60}\n")
        
        return results
