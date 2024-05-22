import os
import json
import shutil
from datetime import datetime
from features.tasks.utils.json_manager import read_json_file, update_json, get_list_json, write_json_file
from features.tasks.attributes.templates import load_template
from features.tasks.utils.file_utils import ensure_directory_exists
from colorama import Fore, Style

def add_task(directory, json_file_path, extension_file, task_names, list_input, template=None):
    json_file_path = os.path.expanduser(json_file_path)
    data = read_json_file(json_file_path)
    template_data = {}
    created_files = []

    if template:
        template_data = load_template(directory, template)
        for key, value in template_data.items():
            input_message = "Please enter a value: " if not isinstance(value, list) else "Please enter a value (for multiple values, separate by commas): "
            print(Fore.CYAN + f"The template field '{key}' is empty." + Style.RESET_ALL)
            user_input = input(Fore.GREEN + input_message + Style.RESET_ALL)
            if isinstance(value, list):
                template_data[key] = [item.strip() for item in user_input.split(',')]
            else:
                template_data[key] = user_input

    for task_name in task_names:
        file_name = f"{task_name.replace(' ', '_')}.{extension_file}"
        file_path = os.path.join(directory, file_name)
        ensure_directory_exists(directory)

        if os.path.exists(file_path):
            print(Fore.RED + f"Task '{task_name}' already exists." + Style.RESET_ALL)
            continue

        # Crea el archivo sin escribir nada en él
        open(file_path, 'w').close()

        relative_path = os.path.join('~', os.path.relpath(file_path, start=os.path.expanduser("~")))
        next_number, list_name, abbreviation = update_json(json_file_path, get_list_json(data, list_input), task_name, relative_path, data, template_data)
        print(Fore.GREEN + f"✔  Added task:" + Style.RESET_ALL + f" '{task_name}' " + Fore.MAGENTA + f"{abbreviation} {next_number}" + Style.RESET_ALL)
        created_files.append(relative_path)

    return created_files

def add_task_properties(directory, json_file_path, list_abbr, task_number, properties, template_name=None):
    data = read_json_file(json_file_path)

    list_found = False
    for list, details in data.items():
        if 'abbreviation' in details and details['abbreviation'] == list_abbr:
            list_found = True
            tasks = details.get('tasks', {})
            task = tasks.get(str(task_number))
            
            if task is None:
                print(f"Task number {task_number} not found in list {list}.")
                break

            # Apply template if specified
            if template_name:
                template_data = load_template(directory, template_name)

                for key, value in template_data.items():
                    if value == "":
                        new_value = input(f"The template field '{key}' is empty. Please enter a value: ")
                        template_data[key] = new_value

                task.update(template_data)
                print(f"Applied template '{template_name}' to task {task_number} in list {list}.")

            # Apply specified properties
            for prop_name, prop_value in properties:
                task[prop_name] = prop_value
                print(f"Added/Updated property '{prop_name}' with value '{prop_value}' in task {task_number} in list {list}.")

            write_json_file(data, json_file_path)
            break

    if not list_found:
        print(f"List with abbreviation '{list_abbr}' not found.")


def add_links(json_file_path, src_category_abbr, src_task_number, links):
    def find_category_by_abbreviation(data, abbr):
        for category_name, details in data.items():
            if details.get('abbreviation', '').lower() == abbr.lower():
                return category_name
        return None

    data = read_json_file(json_file_path)
    src_category = find_category_by_abbreviation(data, src_category_abbr)

    if src_category is None:
        print("Source category not found.")
        return

    src_tasks = data[src_category].get('tasks', {})
    src_task = src_tasks.get(str(src_task_number))
    
    if not src_task:
        print(f"Source task number {src_task_number} not found in category {src_category_abbr}.")
        return

    if 'nodes' not in src_task:
        src_task['nodes'] = []

    success_count = 0
    i = 0
    while i < len(links):
        dst_category_abbr = links[i]
        dst_task_number = links[i + 1]
        dst_category = find_category_by_abbreviation(data, dst_category_abbr)
        if dst_category and str(dst_task_number) in data[dst_category]['tasks']:
            link_notation = f"{dst_category_abbr.lower()} {dst_task_number}"
            if link_notation not in src_task['nodes']:
                src_task['nodes'].append(link_notation)
                print(f"Link added between {src_category_abbr} {src_task_number} and {dst_category_abbr} {dst_task_number}.")
                success_count += 1
            else:
                print(f"Link already exists between {src_category_abbr} {src_task_number} and {dst_category_abbr} {dst_task_number}.")
        else:
            print(f"Destination task or category for link '{dst_category_abbr} {dst_task_number}' not found.")
        i += 2

    write_json_file(data, json_file_path)
    print(f"Added {success_count} new link(s) from task {src_task_number} in category {src_category_abbr}.")

def load_json_file(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

def write_json_file(data, json_file_path):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def add_files(directory, json_file_path, file_paths, category_abbr, template_path=None):
    data = load_json_file(json_file_path)
    category = next((cat for cat, details in data.items() if details.get('abbreviation') == category_abbr), None)
    if not category:
        print(f"No category found for abbreviation '{category_abbr}'.")
        return

    if 'tasks' not in data[category]:
        data[category]['tasks'] = {}

    template_data = {}
    if template_path:
        template_data = load_template(directory, template_path)
        # Interact with the user to fill empty fields in the template
        for key, value in template_data.items():
            if value == "":
                new_value = input(f"The template field '{key}' is empty. Please enter a value: ")
                template_data[key] = new_value

    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"No file found at {file_path}.")
            continue

        file_name = os.path.basename(file_path)
        new_path = os.path.join(directory, file_name)
        if os.path.exists(new_path):
            print(f"Task or file {new_path} already exists.")
            continue

        shutil.move(file_path, new_path)
        print(f"Moved file to {new_path}")

        task_info = {
            "title": os.path.splitext(file_name)[0],
            "file": new_path,
            "extension": os.path.splitext(file_name)[1].strip('.'),
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **template_data
        }

        next_number = str(len(data[category]['tasks']) + 1)
        data[category]['tasks'][next_number] = task_info

    write_json_file(data, json_file_path)
    print(f"Added to category '{category}' under entry number {next_number}.")