"""
Utility modules for Kasparro
"""
import yaml
import json
import numpy as np
from pathlib import Path
from typing import Dict, Any


def convert_to_serializable(obj):
    """Convert numpy/pandas types to Python native types for JSON serialization"""
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'isoformat'):  # Handle datetime/Timestamp objects
        return obj.isoformat()
    elif str(type(obj)).startswith("<class 'pandas._libs.tslibs"):  # Handle all pandas timestamp types
        return str(obj)
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    return obj


def load_config(config_path: str = 'config/config.yaml') -> Dict[str, Any]:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def save_json(data: Dict[str, Any], filepath: str):
    """Save data as JSON file"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    # Convert numpy types before saving
    serializable_data = convert_to_serializable(data)
    with open(filepath, 'w') as f:
        json.dump(serializable_data, f, indent=2)
