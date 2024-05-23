import os
from features.tasks.utils.json_manager import read_json_file, write_json_file
from features.tasks.attributes.templates import load_template
from colorama import Fore, Style


def remove_task_links(data, list_abbr, task_number):
    link_notation = f"{list_abbr.lower()} {task_number}"
    for category_name, details in data.items():
        if 'tasks' in details:
            for task_id, task_info in details['tasks'].items():
                if 'nodes' in task_info and link_notation in task_info['nodes']:
                    task_info['nodes'].remove(link_notation)
                    print(f"Removed link {link_notation} from task {task_id} in category {category_name}.")

def update_task_links(data, list_abbr, old_number, new_number):
    old_link_notation = f"{list_abbr.lower()} {old_number}"
    new_link_notation = f"{list_abbr.lower()} {new_number}"
    for category_name, details in data.items():
        if 'tasks' in details:
            for task_id, task_info in details['tasks'].items():
                if 'nodes' in task_info and old_link_notation in task_info['nodes']:
                    task_info['nodes'].remove(old_link_notation)
                    task_info['nodes'].append(new_link_notation)
                    print(f"Updated link from {old_link_notation} to {new_link_notation} in task {task_id} in category {category_name}.")

def delete_tasks(json_file_path, commands):
    data = read_json_file(json_file_path)

    for list_abbr, task_numbers in commands.items():
        list_name = None
        for cat, details in data.items():
            if 'abbreviation' in details and details['abbreviation'] == list_abbr:
                list_name = cat
                break

        if not list_name:
            print(Fore.RED + f"No list found for abbreviation '{list_abbr}'." + Style.RESET_ALL)
            continue

        if 'tasks' not in data[list_name]:
            print(Fore.RED + f"No tasks in list '{list_name}'." + Style.RESET_ALL)
            continue

        to_delete = []
        for task_number in task_numbers:
            if str(task_number) in data[list_name]['tasks']:
                to_delete.append(str(task_number))
            else:
                print(Fore.YELLOW + f"No task number {task_number} in list '{list_name}'." + Style.RESET_ALL)

        for task_number in to_delete:
            remove_task_links(data, list_abbr, task_number)
            task_info = data[list_name]['tasks'][task_number]
            task_file = os.path.expanduser(task_info['file'])

            try:
                if os.path.exists(task_file):
                    os.remove(task_file)
                    print(Fore.RED + f"Deleted task file: '{task_file}'" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Error deleting file {task_file}: {e}" + Style.RESET_ALL)

            del data[list_name]['tasks'][task_number]

        old_keys = sorted((int(key) for key in data[list_name]['tasks']), key=int)
        new_data = {str(i+1): data[list_name]['tasks'][str(key)] for i, key in enumerate(old_keys)}
        for old_key, new_key in zip(old_keys, new_data.keys()):
            if str(old_key) != new_key:
                update_task_links(data, list_abbr, str(old_key), new_key)
        data[list_name]['tasks'] = new_data

        print(Fore.GREEN + f"Tasks in list '{list_abbr}' updated successfully." + Style.RESET_ALL)

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

    def get_category_from_abbr(data, category_abbr):
        for category, details in data.items():
            if 'abbreviation' in details and details['abbreviation'] == category_abbr:
                return category
        return None

    src_category = get_category_from_abbr(data, src_category_abbr)
    dst_category = get_category_from_abbr(data, dst_category_abbr)

    if not src_category or not dst_category:
        print("One or both categories not found.")
        return

    src_tasks = data[src_category].get('tasks', {})
    dst_tasks = data[dst_category].get('tasks', {})
    
    src_task = src_tasks.get(str(src_task_number))
    dst_task = dst_tasks.get(str(dst_task_number))
    
    if not src_task or not dst_task:
        print(f"One or both tasks not found in specified categories.")
        return

    link_notation = f"{dst_category_abbr.lower()} {dst_task_number}"
    reverse_link_notation = f"{src_category_abbr.lower()} {src_task_number}"

    link_removed = False
    if 'nodes' in src_task and link_notation in src_task['nodes']:
        src_task['nodes'].remove(link_notation)
        print(f"Link removed from {src_category_abbr} {src_task_number} to {dst_category_abbr} {dst_task_number}.")
        link_removed = True

    if 'nodes' in dst_task and reverse_link_notation in dst_task['nodes']:
        dst_task['nodes'].remove(reverse_link_notation)
        print(f"Link removed from {dst_category_abbr} {dst_task_number} to {src_category_abbr} {src_task_number}.")
        link_removed = True

    if link_removed:
        write_json_file(data, json_file_path)
    else:
        print("No links were found to remove.")