import os
from features.tasks.utils.json_manager import read_json_file, write_json_file
from features.tasks.attributes.templates import load_template
from colorama import Fore, Style


def delete_tasks(json_file_path, commands):
    """
    Delete tasks specified by the commands dictionary from the JSON file.

    Parameters:
        json_file_path (str): The path to the JSON file.
        commands (dict): Dictionary with list abbreviation as keys and list of task numbers as values.
    """
    data = read_json_file(json_file_path)

    # Process each command
    for list_abbr, task_numbers in commands.items():
        list = None
        for cat, details in data.items():
            if 'abbreviation' in details and details['abbreviation'] == list_abbr:
                list = cat
                break

        if not list:
            print(Fore.RED + f"No list found for abbreviation '{list_abbr}'." + Style.RESET_ALL)
            continue

        if 'tasks' not in data[list]:
            print(Fore.RED + f"No tasks in list '{list}'." + Style.RESET_ALL)
            continue

        to_delete = []
        for task_number in task_numbers:
            if str(task_number) in data[list]['tasks']:
                to_delete.append(str(task_number))
            else:
                print(Fore.YELLOW + f"No task number {task_number} in list '{list}'." + Style.RESET_ALL)

        # Delete task files and update tasks
        tasks_deleted = False
        for task_number in to_delete:
            task_file = data[list]['tasks'][task_number]['file']
            task_name = data[list]['tasks'][task_number]['title']
            if os.path.exists(task_file):
                os.remove(task_file)
                print(Fore.RED + f"✕ Deleted task:" + Style.RESET_ALL + f" '{task_name}' " + Fore.MAGENTA + f"{list_abbr} {task_number}" + Style.RESET_ALL)
                tasks_deleted = True
            del data[list]['tasks'][task_number]
        if tasks_deleted:
            print(Fore.GREEN + f"Tasks in list '{list_abbr}' updated successfully." + Style.RESET_ALL)

        # Renumber tasks
        new_keys = sorted((int(key) for key in data[list]['tasks']), key=int)
        new_data = {str(i+1): data[list]['tasks'][str(key)] for i, key in enumerate(new_keys)}
        data[list]['tasks'] = new_data

    write_json_file(data, json_file_path)

def delete_task_properties(directory, json_file_path, category_abbr, task_number, properties=None, template_name=None):
    data = read_json_file(json_file_path)

    category_found = False
    for category, details in data.items():
        if 'abbreviation' in details and details['abbreviation'] == category_abbr:
            category_found = True
            tasks = details.get('tasks', {})
            task = tasks.get(str(task_number))

            if task is None:
                print(f"Task number {task_number} not found in category {category}.")
                break

            # Process properties removal
            if properties:
                for prop_name, prop_value in properties:
                    if prop_name in task:
                        if prop_value is not None:
                            # Remove only specific value from list or reset property
                            if isinstance(task[prop_name], list) and prop_value in task[prop_name]:
                                task[prop_name].remove(prop_value)
                                print(f"Removed '{prop_value}' from '{prop_name}' in task {task_number} in {category}.")
                            elif task[prop_name] == prop_value:
                                task[prop_name] = None  # Set property to None or empty depending on requirements
                                print(f"Cleared value from '{prop_name}' in task {task_number} in {category}.")
                        else:
                            # Remove property completely
                            del task[prop_name]
                            print(f"Removed property '{prop_name}' from task {task_number} in {category}.")
            
            # Process template removal
            if template_name and directory:
                template_data = load_template(directory, template_name)
                for key in template_data:
                    if key in task:
                        del task[key]
                        print(f"Removed template property '{key}' from task {task_number} in {category}.")

            write_json_file(data, json_file_path)
            break

    if not category_found:
        print(f"Category with abbreviation '{category_abbr}' not found.")

def delete_link(json_file_path, src_category_abbr, src_task_number, dst_category_abbr, dst_task_number):
    data = read_json_file(json_file_path)

    def get_category_from_abbr(data, src_category_abbr):
        for category, details in data.items():
            if 'abbreviation' in details and details['abbreviation'] == src_category_abbr:
                return category
        return None

    src_category = get_category_from_abbr(data, src_category_abbr)

    if src_category is None:
        print("Source category not found.")
        return

    src_tasks = data[src_category].get('tasks', {})
    src_task = src_tasks.get(str(src_task_number))
    
    if not src_task:
        print(f"Source task number {src_task_number} not found in category {src_category_abbr}.")
        return

    link_notation = f"{dst_category_abbr.lower()} {dst_task_number}"
    if 'nodes' in src_task and link_notation in src_task['nodes']:
        src_task['nodes'].remove(link_notation)
        print(f"Link removed between {src_category_abbr} {src_task_number} and {dst_category_abbr} {dst_task_number}.")
    else:
        print(f"Link not found between {src_category_abbr} {src_task_number} and {dst_category_abbr} {dst_task_number}.")

    write_json_file(data, json_file_path)

