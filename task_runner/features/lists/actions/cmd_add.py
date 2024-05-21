import json
import os

def add_list(json_file_path, category_name, abbreviation):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    else:
        data = {}

    if category_name in data:
        print(f"Category '{category_name}' already exists.")
        return

    # Create the category structure
    data[category_name] = {
        "abbreviation": abbreviation,
        "tasks": {} if input("Include tasks? (yes/no): ").lower() == 'yes' else {},
        "files": {} if input("Include files? (yes/no): ").lower() == 'yes' else {}
    }

    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Category '{category_name}' added successfully with abbreviation '{abbreviation}'.")
