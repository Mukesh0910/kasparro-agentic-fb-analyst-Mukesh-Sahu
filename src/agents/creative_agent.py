"""
Creative Agent - Generates new ad creative recommendations

This agent creates new creative concepts based on performance insights.
"""
import json
from typing import Dict, Any, List
import google.generativeai as genai
import os
from dotenv import load_dotenv
from ..utils.prompt_manager import PromptManager
from ..utils import convert_to_serializable

load_dotenv()


class CreativeAgent:
    """Generates creative recommendations"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the creative agent"""
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel(
            model_name=config.get('model', 'gemini-1.5-flash'),
            generation_config={
                'temperature': 0.9,  # Higher temperature for creativity
                'max_output_tokens': config.get('max_tokens', 2000),
            }
        )
        self.prompt_manager = PromptManager()
    
    def generate_creatives(self, insights: List[Dict[str, Any]], 
                          creative_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate new creative concepts
        
        Args:
            insights: Validated insights about performance
            creative_data: Current creative performance data
            
        Returns:
            Dictionary with creative concepts and testing strategy
        """
        # Convert numpy types and load prompt template
        serializable_insights = convert_to_serializable(insights)
        serializable_creative_data = convert_to_serializable(creative_data)
        
        prompt = self.prompt_manager.get_filled_prompt(
            'creative_agent',
            insights=json.dumps(serializable_insights, indent=2),
            creative_data=json.dumps(serializable_creative_data, indent=2)
        )
        
        system_instruction = "You are a creative strategist for Facebook ads. Always return valid JSON."
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
            
            return result
            
        except Exception as e:
            print(f"Error generating creatives: {e}")
            return {
                'creative_concepts': [],
                'testing_strategy': {
                    'duration': '7-14 days',
                    'success_metrics': ['ROAS > 5.0', 'CTR > 1.5%'],
                    'iteration_plan': 'Test and refine based on results'
                },
                'error': str(e)
            }


def generate_creative_recommendations(config: Dict[str, Any], 
                                     insights: List[Dict[str, Any]], 
                                     creative_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to generate creative recommendations
    
    Args:
        config: Configuration dictionary
        insights: Validated insights
        creative_data: Creative performance data
        
    Returns:
        Creative recommendations
    """
    agent = CreativeAgent(config)
    return agent.generate_creatives(insights, creative_data)
