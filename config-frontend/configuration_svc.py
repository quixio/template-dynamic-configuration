import requests
import os
from datetime import datetime
from typing import List, Dict, Optional

# Get base URL from environment variable
BASE_URL = os.environ["CONFIG_API_BASE_URL"]


def fetch_existing_configs() -> List[Dict]:
    """Fetch existing experiment configurations from API"""
    try:
        url = f"{BASE_URL}/configurations"
        params = {
            "type": "printer-config",
            "type__operator": "$match",
            "sort": "created_at",
            "sort_direction": "desc",
            "limit": 30,
            "offset": 0
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            configs = data.get('data', data.get('results', [])) if isinstance(data, dict) else data
            return configs
        else:
            raise Exception(f"Failed to fetch configurations. Status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching configurations: {str(e)}")


def fetch_full_configuration(config_id: str) -> Optional[Dict]:
    """Fetch full configuration details by ID"""
    try:
        url = f"{BASE_URL}/configurations/{config_id}/content"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch configuration {config_id}. Status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error fetching configuration {config_id}: {str(e)}")


def create_machine_configuration(
    machine_id: str, editor_name: str, scalar: float, mapping: Dict[str, str],
) -> bool:
    """Create a new machine configuration"""
    payload = {
        "metadata": {
            "type": "printer-config",
            "target_key": machine_id,
            "valid_from": datetime.now().isoformat() + "Z",
            "category": "Printer Settings"
        },
        "content": {
            "machine_id": machine_id,
            "editor_name": editor_name,
            "field_scalar": scalar,
            "mapping": mapping,
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/configurations",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            return True
        else:
            raise Exception(f"Failed to create configuration. Status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error creating configuration: {str(e)}")


def update_machine_configuration(
    config_id: str, machine_id: str, editor_name: str, scalar: float, mapping: Dict[str, str]
) -> bool:
    """Update an existing experiment configuration"""
    payload = {
        "content": {
            "machine_id": machine_id,
            "editor_name": editor_name,
            "field_scalar": scalar,
            "mapping": mapping,
        }
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/configurations/{config_id}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            return True
        else:
            raise Exception(f"Failed to update configuration. Status code: {response.status_code}")
    except Exception as e:
        raise Exception(f"Error updating configuration: {str(e)}")


def get_existing_target_keys(configs: List[Dict]) -> List[str]:
    """Extract target keys from configurations list"""
    return [
        config['metadata']['target_key'] 
        for config in configs 
        if 'metadata' in config and 'target_key' in config['metadata']
    ]