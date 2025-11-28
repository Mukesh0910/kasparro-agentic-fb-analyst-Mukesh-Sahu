"""
Insight Agent - Generates hypotheses and insights from data

This agent analyzes data patterns and generates actionable insights.
"""
import json
from typing import Dict, Any, List
import google.generativeai as genai
import os
from dotenv import load_dotenv
from ..utils.prompt_manager import PromptManager
from ..utils import convert_to_serializable

load_dotenv()


class InsightAgent:
    """Generates insights and hypotheses from analyzed data"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the insight agent"""
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel(
            model_name=config.get('model', 'gemini-1.5-flash'),
            generation_config={
                'temperature': config.get('temperature', 0.7),
                'max_output_tokens': config.get('max_tokens', 2000),
            }
        )
        self.prompt_manager = PromptManager()
    
    def generate_insights(self, data: Dict[str, Any], context: str = "") -> List[Dict[str, Any]]:
        """
        Generate insights from data
        
        Args:
            data: Data summary and metrics
            context: Additional context about what to analyze
            
        Returns:
            List of insight dictionaries
        """
        # Convert numpy types to JSON-serializable types
        serializable_data = convert_to_serializable(data)
        
        # Load and fill prompt template
        prompt = self.prompt_manager.get_filled_prompt(
            'insight_agent',
            data=json.dumps(serializable_data, indent=2),
            context=context
        )
        
        system_instruction = "You are an expert marketing analyst. Always return valid JSON."
        full_prompt = f"{system_instruction}\n\n{prompt}"
        
        try:
            response = self.model.generate_content(full_prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.startswith('```'):
                response_text = response_text[3:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            result = json.loads(response_text)
            
            return result.get('insights', [])
            
        except Exception as e:
            print(f"Error generating insights: {e}")
            return [{
                'title': 'Error generating insights',
                'description': str(e),
                'severity': 'low',
                'confidence': 0.0,
                'evidence': {},
                'error': True
            }]


def generate_insights(config: Dict[str, Any], data: Dict[str, Any], context: str = "") -> List[Dict[str, Any]]:
    """
    Convenience function to generate insights
    
    Args:
        config: Configuration dictionary
        data: Data to analyze
        context: Analysis context
        
    Returns:
        List of insights
    """
    agent = InsightAgent(config)
    return agent.generate_insights(data, context)
