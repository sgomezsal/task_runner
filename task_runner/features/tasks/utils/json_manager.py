import json
import os
from datetime import datetime

def read_json_file(file_path):
    """
    Reads a JSON file and returns the data.
    If the file does not exist, returns an empty dictionary.
    
    Parameters:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict: The data from the JSON file.
    """
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {}

def write_json_file(data, file_path):
    """
    Writes data to a JSON file.
    
    Parameters:
        data (dict): The data to write.
        file_path (str): The path to the JSON file.
    """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_json(json_file_path, list_name, task_name, file_path, data, template_data):
    """
    Updates the JSON file with task details, incorporating template data.
    
    Parameters:
        directory (str): The base directory for storing task-related files.
        list_name (str): The list where the task belongs.
        task_name (str): The name of the task.
        file_path (str): The path to the task's file.
        data (dict): Current task data.
        template_data (dict): Data from the applied template.
    """
    task_data = {
        "complete": False,
        "title": task_name,
        "file": file_path,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    task_data.update(template_data)

    if list_name not in data:
        list_name = "Default"
        data[list_name] = {"abbreviation": "df", "tasks": {}}

    next_number = str(len(data[list_name].get('tasks', {})) + 1)
    data[list_name]['tasks'][next_number] = task_data

    write_json_file(data, json_file_path)

    return next_number, list_name, data[list_name]['abbreviation']

def get_list_json(data, input_name):
    """
    Retrieves the list for the task based on the input name or abbreviation. Returns a default list if not found.
    
    Parameters:
        data (dict): Task data loaded from the JSON file.
        input_name (str): The list name or abbreviation input by the user.
    
    Returns:
        str: The list name.
    """
    list_map = {"df": "Default"}
    for list_name, details in data.items():
        if 'abbreviation' in details:
            list_map[details['abbreviation']] = list_name
            list_map[list_name] = list_name

    return list_map.get(input_name, "Default")

def check_list_json(json_file_path, category):
    data = read_json_file(json_file_path)
    return category in data or any(cat.get('abbreviation') == category for cat in data.values())