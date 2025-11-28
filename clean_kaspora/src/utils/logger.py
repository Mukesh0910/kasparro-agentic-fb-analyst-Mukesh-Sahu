"""
Logger Utility
Handles logging of agent interactions and results
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


class ExecutionLogger:
    """Logs execution traces for observability"""
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.steps: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {}
    
    def set_metadata(self, **kwargs):
        """Set metadata for this execution"""
        self.metadata.update(kwargs)
    
    def log_step(self, step_name: str, input_data: Any, output_data: Any, 
                 agent: str = None, duration: float = None, **extras):
        """
        Log a single execution step
        
        Args:
            step_name: Name of the step
            input_data: Input to this step
            output_data: Output from this step
            agent: Name of the agent that executed this step
            duration: Execution time in seconds
            **extras: Additional metadata
        """
        step = {
            'step_name': step_name,
            'agent': agent,
            'timestamp': datetime.now().isoformat(),
            'input': self._sanitize(input_data),
            'output': self._sanitize(output_data),
            'duration_seconds': duration
        }
        step.update(extras)
        self.steps.append(step)
    
    def _sanitize(self, data: Any) -> Any:
        """Convert data to JSON-serializable format"""
        if isinstance(data, (str, int, float, bool, type(None))):
            return data
        elif isinstance(data, dict):
            return {k: self._sanitize(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._sanitize(item) for item in data]
        else:
            return str(data)
    
    def save(self, filename: str = None) -> Path:
        """
        Save execution log to file
        
        Args:
            filename: Optional filename, auto-generated if not provided
            
        Returns:
            Path to saved log file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"trace_{timestamp}.json"
        
        log_path = self.log_dir / filename
        
        log_data = {
            'metadata': self.metadata,
            'execution_start': self.steps[0]['timestamp'] if self.steps else None,
            'execution_end': self.steps[-1]['timestamp'] if self.steps else None,
            'total_steps': len(self.steps),
            'steps': self.steps
        }
        
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)
        
        return log_path
    
    def get_summary(self) -> str:
        """Get a human-readable summary of the execution"""
        if not self.steps:
            return "No steps logged"
        
        summary = [
            f"Execution Summary",
            f"=" * 50,
            f"Total Steps: {len(self.steps)}",
            f"Query: {self.metadata.get('query', 'N/A')}",
            f"",
            f"Steps:"
        ]
        
        for i, step in enumerate(self.steps, 1):
            summary.append(f"  {i}. {step['step_name']} ({step.get('agent', 'unknown')})")
            if step.get('duration_seconds'):
                summary.append(f"     Duration: {step['duration_seconds']:.2f}s")
        
        return "\n".join(summary)
