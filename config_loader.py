import yaml
import json
from typing import Dict, Any

def load_config(config_path: str) -> Dict[str, Any]:
    if config_path.endswith('.yaml'):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    elif config_path.endswith('.json'):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported config format. Use .yaml or .json")