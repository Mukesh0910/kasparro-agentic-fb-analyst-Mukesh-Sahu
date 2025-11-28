"""
Planner Agent - Creates analysis plans from user queries

This agent decomposes user queries into structured analysis plans.
"""
import json
from pathlib import Path
from typing import Dict, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()


class PlannerAgent:
    def __init__(self, config: Dict[str, Any]):
        """Initialize the planner agent"""
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel(
            model_name=config.get('model', 'gemini-1.5-flash'),
            generation_config={
                'temperature': config.get('temperature', 0.7),
                'max_output_tokens': config.get('max_tokens', 2000),
            }
        )
        
        # Load prompt template
        prompt_path = Path('prompts/planner_agent.md')
        with open(prompt_path, 'r') as f:
            self.prompt_template = f.read()
    
    def create_plan(self, user_query: str) -> Dict[str, Any]:
        """
        Create an analysis plan from user query
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Dictionary containing the analysis plan
        """
        # Fill in the prompt template
        prompt = self.prompt_template.replace('{query}', user_query)
        system_instruction = "You are a strategic planner for marketing analytics. Always return valid JSON."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        try:
            response = self.model.generate_content(full_prompt)
            
            # Extract JSON from response (Gemini may include markdown code blocks)
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]  # Remove ```json
            if response_text.startswith('```'):
                response_text = response_text[3:]  # Remove ```
            if response_text.endswith('```'):
                response_text = response_text[:-3]  # Remove trailing ```
            response_text = response_text.strip()
            
            plan = json.loads(response_text)
            
            # Add metadata
            plan['user_query'] = user_query
            plan['model_used'] = self.model.model_name
            
            return plan
            
        except Exception as e:
            print(f"Error creating plan: {e}")
            # Return a basic fallback plan
            return {
                'user_query': user_query,
                'objective': 'Analyze Facebook ads performance',
                'steps': [
                    {
                        'step_number': 1,
                        'action': 'Load and examine recent data',
                        'data_needed': 'Last 7-14 days of ad performance',
                        'expected_output': 'Data summary with key metrics'
                    },
                    {
                        'step_number': 2,
                        'action': 'Identify performance trends and anomalies',
                        'data_needed': 'ROAS, CTR, spend, revenue by segments',
                        'expected_output': 'List of insights with evidence'
                    },
                    {
                        'step_number': 3,
                        'action': 'Generate recommendations',
                        'data_needed': 'Best and worst performers',
                        'expected_output': 'Actionable improvements'
                    }
                ],
                'success_criteria': 'Clear insights with data-backed recommendations',
                'error': str(e)
            }


def create_analysis_plan(config: Dict[str, Any], user_query: str) -> Dict[str, Any]:
    """
    Convenience function to create an analysis plan
    
    Args:
        config: Configuration dictionary
        user_query: User's query string
        
    Returns:
        Analysis plan dictionary
    """
    planner = PlannerAgent(config)
    return planner.create_plan(user_query)
