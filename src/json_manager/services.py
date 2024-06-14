import uuid
from datetime import datetime
from colorama import Fore, Style
from json_manager.data_json import ensure_json_data_file_exists
from json_manager.utils import load_json, save_json

def add_item_to_json(title, file_path, config, category, item_type):
    json_path = config['data_file_path']
    ensure_json_data_file_exists(config)
    data = load_json(json_path)

    # Crear el ítem basado en el tipo especificado
    if item_type == 'task':
        new_item = {
            "complete": False,
            "title": title,
            "file": file_path,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "uuid": str(uuid.uuid4())
        }
    elif item_type == 'file':
        new_item = {
            "title": title,
            "file": file_path,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "uuid": str(uuid.uuid4())
        }
    else:
        raise ValueError(f"Unsupported item type: {item_type}")

    # Agregar el ítem a la categoría adecuada
    if category not in data:
        data[category] = {"abbreviation": config.get('abbreviation', 'Default'), "items": []}
    data[category]['items'].append(new_item)

    save_json(data, json_path, mode='r+')

def add_category_to_json(config, category_name, abbreviation):
    json_path = config['data_file_path']
    ensure_json_data_file_exists(config)
    data = load_json(json_path)

    if category_name in data:
        return f"{Fore.RED}✗ Error:{Style.RESET_ALL} A category with the name '{category_name}' already exists."

    data[category_name] = {"abbreviation": abbreviation, "items": []}

    save_json(data, json_path)
    return f"{Fore.GREEN}✓{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}New category:{Style.RESET_ALL} {category_name} {Fore.MAGENTA}{abbreviation}{Style.RESET_ALL}"

