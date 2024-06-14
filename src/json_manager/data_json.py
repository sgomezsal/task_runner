import json
import os
import logging
from json_manager.utils import read_json_file

def read_json_data(config):
    """Lee los datos desde el archivo especificado en la configuración."""
    data_file_path = config['data_file_path']
    return read_json_file(data_file_path)
    
def ensure_json_data_file_exists(config):
    """
    Ensures that the JSON file specified in the configuration exists at the given path.
    """
    json_path = os.path.expanduser(config['data_file_path'])
    if not os.path.exists(json_path):
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        with open(json_path, 'w') as file:
            json.dump({config['default_category']: {"abbreviation": config['abbreviation'], "items": []}}, file, indent=4)
        logging.info(f"New JSON file created at: {json_path}")
    else:
        logging.info(f"JSON file already exists at: {json_path}")