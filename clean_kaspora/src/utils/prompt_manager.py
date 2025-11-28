"""
Prompt Manager Utility
Handles loading and filling prompt templates
"""
from pathlib import Path
from typing import Dict, Any


class PromptManager:
    """Manages loading and formatting of prompt templates"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
    
    def load_prompt(self, agent_name: str) -> str:
        """
        Load a prompt template for a specific agent
        
        Args:
            agent_name: Name of the agent (e.g., 'planner_agent', 'data_agent')
            
        Returns:
            Prompt template as string
        """
        prompt_file = self.prompts_dir / f"{agent_name}.md"
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def fill_prompt(self, template: str, **kwargs) -> str:
        """
        Fill a prompt template with provided values
        
        Args:
            template: Prompt template string
            **kwargs: Key-value pairs to fill in the template
            
        Returns:
            Filled prompt string
        """
        filled = template
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            filled = filled.replace(placeholder, str(value))
        
        return filled
    
    def get_filled_prompt(self, agent_name: str, **kwargs) -> str:
        """
        Load and fill a prompt in one step
        
        Args:
            agent_name: Name of the agent
            **kwargs: Values to fill in the template
            
        Returns:
            Filled prompt string
        """
        template = self.load_prompt(agent_name)
        return self.fill_prompt(template, **kwargs)
