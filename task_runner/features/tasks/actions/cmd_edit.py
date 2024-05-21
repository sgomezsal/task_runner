import os
from features.tasks.utils.json_manager import read_json_file
import subprocess

def edit_task(json_file_path, list_abbr, task_number):
    data = read_json_file(json_file_path)

    category = None
    for cat, details in data.items():
        if 'abbreviation' in details and details['abbreviation'] == list_abbr:
            category = cat
            break

    if not category:
        print(f"No category found for abbreviation '{list_abbr}'.")
        return

    # Check if the task exists within the 'tasks' dictionary of the category
    if str(task_number) not in data[category]['tasks']:
        print(f"No task number {task_number} in category '{category}'.")
        return

    # Access the task file from the 'tasks' sub-dictionary
    task_file = data[category]['tasks'][str(task_number)]['file']
    if not os.path.exists(task_file):
        print(f"Task file not found: {task_file}")
        return

    # Launch nvim to edit the task file
    subprocess.run(['nvim', task_file])
    print(f"Editing task number {task_number} in category '{category}' with file: {task_file}")
