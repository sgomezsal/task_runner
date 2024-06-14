from json_manager.utils import read_json_file
import os

def read_json_config():
    """Lee la configuración desde 'config.json' y ajusta las rutas necesarias."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, 'config', 'config.json')
    config = read_json_file(config_path)
    if 'task_directory' in config:
        config['task_directory'] = os.path.expanduser(config['task_directory'])
    if 'data_file_path' in config:
        config['data_file_path'] = os.path.expanduser(config['data_file_path'])
    return config