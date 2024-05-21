import os
from features.tasks.utils.json_manager import read_json_file, write_json_file

def rename_task_name(json_file_path, extension_file, category_abbr, task_number, new_name):
    data = read_json_file(json_file_path)

    category_found = False
    for category, details in data.items():
        if 'abbreviation' in details and details['abbreviation'] == category_abbr:
            category_found = True
            tasks = details.get('tasks', {})
            task = tasks.get(str(task_number))
            
            if task is None:
                print(f"Task number {task_number} not found in category {category}.")
                return
            
            old_file_path = task['file']
            new_file_path = os.path.join(os.path.dirname(old_file_path), f"{new_name.replace(' ', '_')}.{extension_file}")
            
            # Rename the file on the filesystem
            if os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)
                print(f"Renamed file from {old_file_path} to {new_file_path}")
            
            # Update the JSON data
            task['title'] = new_name
            task['file'] = new_file_path
            write_json_file(data, json_file_path)
            print(f"Updated task name to {new_name} in category {category}")
            break

    if not category_found:
        print(f"Category with abbreviation '{category_abbr}' not found.")

def rename_task_property_name(json_file_path, category_abbr, task_number, old_prop_name, new_prop_name):
    data = read_json_file(json_file_path)

    category_found = False
    for category, details in data.items():
        if 'abbreviation' in details and details['abbreviation'] == category_abbr:
            category_found = True
            tasks = details.get('tasks', {})
            task = tasks.get(str(task_number))
            
            if task is None:
                print(f"Task number {task_number} not found in category {category}.")
                return
            
            if old_prop_name in task:
                task[new_prop_name] = task.pop(old_prop_name)
                write_json_file(data, json_file_path)
                print(f"Renamed property '{old_prop_name}' to '{new_prop_name}' in task {task_number} in category {category}")
            else:
                print(f"Property '{old_prop_name}' not found in task {task_number} in category {category}")
            break

    if not category_found:
        print(f"Category with abbreviation '{category_abbr}' not found.")
