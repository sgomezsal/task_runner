import json
import os
from datetime import datetime
from colorama import Fore, Style
import re

task_runner_logo = """
|\__/,|   (`\ 
|_ _  |.--.) ) 
( T   )     / 
(((^_(((/(((_/ 𝑡𝑎𝑠𝑘 𝑟𝑢𝑛𝑛𝑒𝑟
_________________________"""

def show_lists(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(Fore.RED + f"Failed to read or parse the JSON file: {e}" + Style.RESET_ALL)
        return

    print(Fore.GREEN + task_runner_logo + Style.RESET_ALL)
    print(Fore.GREEN + "Available lists:" + Style.RESET_ALL)

    for list_name, details in data.items():
        task_count = len(details.get('tasks', {}))  # Obtiene el número de tareas en cada lista
        abbreviation = details.get('abbreviation', 'N/A')
        print(Fore.GREEN + "↬ " + Style.RESET_ALL + f"{list_name} {abbreviation} " + Fore.CYAN + f"[{task_count}]" + Style.RESET_ALL)


def show_list_content(directory, json_file_path, list_abbr):
    data = load_data(json_file_path)
    list_name = get_list_from_abbr(data, list_abbr)
    if not list_name:
        print(Fore.RED + f"No list found with abbreviation '{list_abbr}'." + Style.RESET_ALL)
        return
    print(Style.BRIGHT + f"{list_name} ({data[list_name]['abbreviation']})" + Style.RESET_ALL)
    for task_number, task_info in data[list_name].get('tasks', {}).items():
        file_path = os.path.join(directory, task_info['file'])  # Asegúrate de que la ruta es correcta
        file_filled_symbol = Fore.YELLOW + "Ξ" + Style.RESET_ALL if os.path.exists(file_path) and os.path.getsize(file_path) > 0 else ""
        if 'complete' not in task_info:
            status_symbol = Fore.YELLOW + "△" + Style.RESET_ALL
            file_extension = os.path.splitext(task_info['file'])[1]
            print(f"  {task_number}. {status_symbol} {task_info.get('title', 'No title')} ({file_extension}) {file_filled_symbol}")
        else:
            status_symbol = Fore.RED + "x" + Style.RESET_ALL if not task_info['complete'] else Fore.GREEN + "✓" + Style.RESET_ALL
            print(f"  {task_number}. {status_symbol} {task_info.get('title', 'No title')} {file_filled_symbol}")


def parse_filters(filter_args):
    filters = []
    current_filters = []
    logic_operator = 'and'  # Default logical operator

    for f in filter_args:
        if f.lower() == 'and' or f.lower() == 'or':
            if current_filters:
                filters.append((current_filters, logic_operator))
                current_filters = []
            logic_operator = f.lower()
        else:
            key_value = f.strip('@').split('=', 1)
            if len(key_value) == 2:
                key, value = key_value
                current_filters.append((key.strip(), value.strip('"')))
            else:
                current_filters.append((key_value[0].strip(), None))

    if current_filters:
        filters.append((current_filters, logic_operator))  # Add the last set of filters

    return filters

def apply_filters_to_tasks(tasks, filters):
    filtered_tasks = []
    for task_id, task_details in tasks.items():
        if all(task_details.get(key) == value if value is not None else key in task_details for key, value in filters):
            filtered_tasks.append((task_id, task_details))
    return filtered_tasks

def load_data(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    else:
        print("No tasks file found.")
        return None
    
def get_list_from_abbr(data, abbr):
    for list, details in data.items():
        if 'abbreviation' in details and details['abbreviation'] == abbr:
            return list
    return abbr  # Return the abbreviation as is if no match found

def show_filtered_tasks(directory, json_file_path, list_abbr, filters):
    data = load_data(json_file_path)

    list_name = get_list_from_abbr(data, list_abbr)
    if not list_name:
        print(f"No list found with abbreviation '{list_abbr}'.")
        return

    tasks = data[list_name].get('tasks', {})
    parsed_filters = parse_filters(filters)

    if not parsed_filters:  # Si no se proporcionan filtros específicos, mostrar filtros disponibles
        show_available_filters(json_file_path, list_abbr)
    else:
        filtered_tasks = {num: task for num, task in tasks.items() if check_task_against_filters(task, parsed_filters)}
        if filtered_tasks:
            print(f"\033[4m{list_name} ({list_abbr}):\033[0m")
            for num, task in filtered_tasks.items():
                file_path = os.path.join(directory, task['file'])  # Asegúrate de que la ruta es correcta
                file_filled_symbol = Fore.YELLOW + "Ξ" + Style.RESET_ALL if os.path.exists(file_path) and os.path.getsize(file_path) > 0 else ""
                if 'complete' not in task:
                    status_symbol = Fore.YELLOW + "△" + Style.RESET_ALL
                    file_extension = os.path.splitext(task['file'])[1]
                    print(f"  {num}. {status_symbol} {task['title']} ({file_extension}) - {task_details} {file_filled_symbol}")
                else:
                    status_symbol = Fore.RED + "x" + Style.RESET_ALL if not task['complete'] else Fore.GREEN + "✓" + Style.RESET_ALL
                    task_details = " - ".join(f"{key}={task.get(key, 'N/A')}" for group, _ in parsed_filters for key, _ in group if key in task)
                    print(f"  {num}. {status_symbol} {task['title']} - {task_details} {file_filled_symbol}")
        else:
            print("No tasks match the specified filters.")


def show_available_filters(json_file_path, list_abbr):
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    list_name = get_list_from_abbr(data, list_abbr)
    if not list_name:
        print(f"No list found with abbreviation '{list_abbr}'.")
        return

    # Extraer todos los filtros posibles de las tareas
    tasks = data[list_name].get('tasks', {})
    all_filters = set()
    for task_details in tasks.values():
        for key in task_details.keys():
            if key not in ['complete', 'title', 'file', 'created']:  # Excluir claves que no sean filtros
                all_filters.add(key)

    # Mostrar todos los filtros disponibles
    if all_filters:
        print(f"Available filters for tasks in list '{list_name} ({list_abbr})':")
        for filter_key in sorted(all_filters):
            print(f"  - {filter_key}")
    else:
        print(f"No filters available for tasks in list '{list_name}'.")


def wildcard_to_regex(wildcard):
    """ Convert wildcard pattern to a regex pattern. """
    regex = re.escape(wildcard)  # Escape all special characters except for '*' and '?'
    regex = regex.replace(r'\*', '.*')  # Replace '*' with '.*' (0 or more of any character)
    regex = regex.replace(r'\?', '.')  # Replace '?' with '.' (1 of any character)
    return '^' + regex + '$'  # Ensure the pattern matches the entire string

def check_task_against_filters(task, filters):
    if not filters:
        return True  # No filters provided, all tasks match

    overall_result = True  # Start true for 'and', change if the first operator is 'or'
    for filter_group, logic_operator in filters:
        group_result = (logic_operator == 'and')  # Start true for 'and', false for 'or'
        for key, value in filter_group:
            actual_value = task.get(key)

            if value is not None:
                # Use the wildcard_to_regex function to convert wildcard patterns to regex patterns
                pattern = wildcard_to_regex(value)
                current_match = bool(re.match(pattern, actual_value)) if actual_value is not None else False
            else:
                # If no value is specified, check for the existence of the attribute
                current_match = (actual_value is not None)

            if logic_operator == 'and':
                group_result = group_result and current_match
            else:
                group_result = group_result or current_match

        if logic_operator == 'and':
            overall_result = overall_result and group_result
        else:
            overall_result = overall_result or group_result

    return overall_result

# Function to show tasks for the day
def show_my_day(json_file_path, specific_categories=None):
    data = load_data(json_file_path)
    if not data:
        return

    today = datetime.now().strftime("%Y-%m-%d")
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today_weekday = weekdays[datetime.now().weekday()]

    # Default categories to show if none are specified
    default_categories = ['Calendar', 'Tickler File', 'Checklist']
    # Mapping abbreviations to full list names
    list_map = {details.get('abbreviation', '').lower(): list_name for list_name, details in data.items()}

    for list_name, details in data.items():
        abbreviation = details.get('abbreviation', 'N/A')
        if specific_categories:
            if list_name not in specific_categories and abbreviation.lower() not in specific_categories:
                continue
        else:
            if list_name not in default_categories:
                continue

        print(f"{list_name} ({abbreviation})")
        total_tasks = 0
        completed_tasks = 0
        task_list = details.get('tasks', {})

        for task_number, task_info in task_list.items():
            due_date = task_info.get('dueDate', '')
            routine = task_info.get('routine', [])
            if (due_date == today or today_weekday in routine or any(check_recurring(today, entry) for entry in routine)):
                total_tasks += 1
                if task_info.get('complete', False):
                    completed_tasks += 1
                if specific_categories:
                    print(f"  {task_number}. {task_info.get('title')} - @dueDate={due_date}")
                    continue

        if not specific_categories:
            print(f"  Number of tasks: {total_tasks}")
            print(f"  Number of complete tasks: {completed_tasks}\n")

def check_recurring(current_date, recurring_entry):
    # This is a placeholder for actual recurring date checking logic
    return False



