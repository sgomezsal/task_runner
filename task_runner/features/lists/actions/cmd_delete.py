import json
import os

def delete_list(json_file_path, category_name):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    else:
        print("No data file found.")
        return

    if category_name not in data:
        print(f"Category '{category_name}' does not exist.")
        return

    print(f"Contents of '{category_name}': {data[category_name]}")
    if input("Are you sure you want to delete this category and all its contents? (yes/no): ").lower() == 'yes':
        del data[category_name]
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Category '{category_name}' has been deleted.")
    else:
        print("Deletion cancelled.")
