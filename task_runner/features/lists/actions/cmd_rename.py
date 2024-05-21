import os
import json

def rename_list(json_file_path, old_name, new_name, new_abbreviation):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    else:
        print("No data file found.")
        return

    if old_name not in data:
        print(f"Category '{old_name}' does not exist.")
        return

    data[new_name] = data.pop(old_name)
    data[new_name]['abbreviation'] = new_abbreviation

    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Category renamed from '{old_name}' to '{new_name}' with new abbreviation '{new_abbreviation}'.")
