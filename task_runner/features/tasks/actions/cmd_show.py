import os
import json
import subprocess

def show_tasks(json_file_path, category_abbr, task_number, preview=False):
    if not os.path.exists(json_file_path):
        print("No tasks file found.")
        return

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    def get_category_from_abbr(data, abbr):
        for category, details in data.items():
            if 'abbreviation' in details and details['abbreviation'] == abbr:
                return category
        return None

    category = get_category_from_abbr(data, category_abbr)

    if category and str(task_number) in data[category]['tasks']:
        task_info = data[category]['tasks'][str(task_number)]
        task_path = task_info["file"]

        if os.path.exists(task_path):
            if preview:
                subprocess.run(['typst-preview', task_path])
            else:
                subprocess.run(['cat', task_path])
        else:
            print(f"Task file not found: {task_path}")
    else:
        print(f"Task number {task_number} in category '{category}' does not exist.")

def show_linked_tasks(directory, json_file_path, category_abbr, task_number):
    if not os.path.exists(json_file_path):
        print("No tasks file found.")
        return

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Normalize the input abbreviation
    category_abbr = category_abbr.lower()
    task_number = str(task_number)

    # Check if the abbreviation corresponds to an existing category
    if category_abbr not in (details.get('abbreviation', '').lower() for details in data.values()):
        print(f"No category found for abbreviation '{category_abbr}'.")
        return

    # Locate the source task in its category
    src_category = next((category for category, details in data.items() if details.get('abbreviation', '').lower() == category_abbr), None)
    if not src_category:
        print("Category not found in the data.")
        return
    
    src_task = data[src_category]['tasks'].get(task_number)
    if not src_task:
        print(f"Task {task_number} not found in category '{src_category}'.")
        return

    # Print links if nodes exist
    if 'nodes' in src_task:
        print(f"Links for {category_abbr.upper()} {task_number}:")
        for node in src_task['nodes']:
            dst_category_abbr, dst_task_number = node.lower().split()
            dst_category = next((category for category, details in data.items() if details.get('abbreviation', '').lower() == dst_category_abbr), None)
            if dst_category and dst_task_number in data[dst_category]['tasks']:
                dst_task_info = data[dst_category]['tasks'][dst_task_number]
                print(f"  - {dst_category.upper()} {dst_task_number}: {dst_task_info.get('title', 'No title available')}")
    else:
        print(f"No links found for task {task_number} in category '{src_category}'.")
