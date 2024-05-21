import os
import json
import subprocess
from colorama import Fore, Style

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

def load_data(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    else:
        print("No tasks file found.")
        return None

def get_list_from_abbr(data, abbr):
    for category, details in data.items():
        if details.get('abbreviation', '').lower() == abbr.lower():
            return category
    return None

def show_linked_tasks(directory, json_file_path, category_abbr, task_number):
    if not os.path.exists(json_file_path):
        print(Fore.RED + "No tasks file found." + Style.RESET_ALL)
        return

    data = load_data(json_file_path)
    category_abbr = category_abbr.lower()
    task_number = str(task_number)

    src_category = get_list_from_abbr(data, category_abbr)
    if not src_category:
        print(Fore.RED + f"No category found for abbreviation '{category_abbr}'." + Style.RESET_ALL)
        return

    src_task = data[src_category]['tasks'].get(task_number)
    if not src_task:
        print(Fore.RED + f"Task {task_number} not found in category '{src_category}'." + Style.RESET_ALL)
        return

    if 'nodes' in src_task:
        linked_categories = {}
        for node in src_task['nodes']:
            dst_category_abbr, dst_task_number = node.lower().split()
            dst_category = get_list_from_abbr(data, dst_category_abbr)
            if dst_category and dst_task_number in data[dst_category]['tasks']:
                dst_task_info = data[dst_category]['tasks'][dst_task_number]
                if dst_category not in linked_categories:
                    linked_categories[dst_category] = []
                linked_categories[dst_category].append((dst_task_number, dst_task_info))

        # Contar solo tareas con el atributo 'complete' para total y completadas
        total_linked_tasks = sum(1 for tasks in linked_categories.values() for _, task in tasks if 'complete' in task)
        completed_linked_tasks = sum(1 for tasks in linked_categories.values() for _, task in tasks if task.get('complete', False))

        print(f"\033[4m{src_category} {task_number}\033[0m" + Fore.CYAN + Style.BRIGHT + f" [{completed_linked_tasks}/{total_linked_tasks}]" + Style.RESET_ALL)

        for category, tasks in linked_categories.items():
            print(Style.BRIGHT + Fore.WHITE + f"{category.capitalize()} ⇗" + Style.RESET_ALL)
            for dst_task_number, dst_task_info in tasks:
                dst_category_abbr = data[category]['abbreviation'].lower()
                if 'complete' not in dst_task_info:
                    status_symbol = Fore.YELLOW + "△" + Style.RESET_ALL  # Triangle for file tasks
                    print(f"  {status_symbol} {dst_task_info.get('title', 'No title available')}" + Fore.MAGENTA + f" {dst_category_abbr} {dst_task_number}" + Style.RESET_ALL)
                else:
                    status_symbol = Fore.RED + "x" + Style.RESET_ALL if not dst_task_info['complete'] else Fore.GREEN + "✓" + Style.RESET_ALL
                    print(f"  {status_symbol} {dst_task_info.get('title', 'No title available')}" + Fore.MAGENTA + f" {dst_category_abbr} {dst_task_number}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + f"No links found for task {task_number} in category '{src_category}'." + Style.RESET_ALL)