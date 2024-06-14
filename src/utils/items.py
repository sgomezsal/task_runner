from json_manager.services import add_item_to_json
from utils.files import create_task_file
from utils.collection import find_item_index
from json_manager.data_json import read_json_data

def check_item_existence(data, titles):
    existing_titles = {item['title'].lower(): cat_name for cat_name, cat_details in data.items() for item in cat_details.get('items', [])}
    existing_item = {}
    for title in titles:
        if title.lower() in existing_titles:
            existing_item[title] = existing_titles[title.lower()]
    return existing_item

def add_item_to_category(title, category, config, data, item_type):
    file_path = create_task_file(title, config)
    add_item_to_json(title, file_path, config, category, item_type)
    data = read_json_data(config)  # Reload data to reflect changes
    index = find_item_index(data, category, title)
    if index is None:
        raise Exception("Task not found in JSON data after addition.")
    return file_path, index