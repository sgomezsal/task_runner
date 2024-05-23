import os
import json

def read_json_file(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    else:
        print("No data file found.")
        return None

def write_json_file(data, json_file_path):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_all_references(data, old_abbr, new_abbr):
    """
    Update all references from old abbreviation to new abbreviation across all tasks.
    """
    for category in data.values():
        for task in category.get('tasks', {}).values():
            if 'nodes' in task:
                task['nodes'] = [node.replace(old_abbr, new_abbr) for node in task['nodes']]

def rename_list(json_file_path, old_name, new_name, new_abbreviation):
    data = read_json_file(json_file_path)
    if data is None:
        return

    if old_name not in data:
        print(f"Category '{old_name}' does not exist.")
        return

    # Capture old abbreviation before changing
    old_abbreviation = data[old_name].get('abbreviation', '')

    # Rename the category and update abbreviation
    data[new_name] = data.pop(old_name)
    data[new_name]['abbreviation'] = new_abbreviation

    # Update references to use the new abbreviation
    update_all_references(data, old_abbreviation, new_abbreviation)

    write_json_file(data, json_file_path)
    print(f"Category renamed from '{old_name}' to '{new_name}' with new abbreviation '{new_abbreviation}'.")

# Example of how to call the function
# rename_list('path_to_your_json_file.json', 'Next Actions', 'Next Info', 'ni')
