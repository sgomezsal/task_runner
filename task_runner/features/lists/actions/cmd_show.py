import json
import os
from datetime import datetime
from colorama import Fore, Style

def show_lists(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Failed to read or parse the JSON file: {e}")
        return

    print("Available lists:")
    for list_name, details in data.items():
        print(f"{list_name} - Abbreviation: {details.get('abbreviation', 'N/A')}")


def show_list_content(json_file_path, list_abbr):
    data = load_data(json_file_path)
    list_name = get_list_from_abbr(data, list_abbr)
    if not list_name:
        print(Fore.RED + f"No list found with abbreviation '{list_abbr}'." + Style.RESET_ALL)
        return
    print(Style.BRIGHT + f"{list_name} ({data[list_name]['abbreviation']})" + Style.RESET_ALL)
    for task_number, task_info in data[list_name].get('tasks', {}).items():
        if not 'complete' in task_info:
            # This assumes that tasks representing files have a 'file' field
            status_symbol = Fore.YELLOW + "△" + Style.RESET_ALL  # Triangle for file tasks
            file_extension = os.path.splitext(task_info['file'])[1]
            print(f"  {task_number}. {status_symbol} {task_info['title']} ({file_extension})")
        else:
            status_symbol = Fore.RED + "x" + Style.RESET_ALL if not task_info.get('complete', False) else Fore.GREEN + "✓" + Style.RESET_ALL
            print(f"  {task_number}. {status_symbol} {task_info.get('title', 'No title')}")


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

def show_filtered_tasks(json_file_path, list_abbr, filters):
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
            print(f"\033[4m{list_name} ({list_abbr}) with applied filters:\033[0m")
            for num, task in filtered_tasks.items():
                if not 'complete' in task:
                    task_details = " - ".join(f"{key}={task.get(key, 'N/A')}" for group, _ in parsed_filters for key, _ in group if key in task)
                    status_symbol = Fore.YELLOW + "△" + Style.RESET_ALL 
                    file_extension = os.path.splitext(task['file'])[1]
                    print(f"  {num}. {status_symbol} {task['title']} ({file_extension}) - {task_details}")
                else:
                    status_symbol = Fore.RED + "x" + Style.RESET_ALL if not task['complete'] else Fore.GREEN + "✓" + Style.RESET_ALL
                    task_details = " - ".join(f"{key}={task.get(key, 'N/A')}" for group, _ in parsed_filters for key, _ in group if key in task)
                    print(f"  {num}. {status_symbol} {task['title']} - {task_details}")
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


def check_task_against_filters(task, filters):
    if not filters:
        return True  # Si no se proporcionan filtros, todas las tareas deben coincidir

    overall_result = True  # Comienza con True para 'and', cambia si el primer operador es 'or'
    for filter_group, logic_operator in filters:
        group_result = (logic_operator == 'and')  # Comienza verdadero para 'and', falso para 'or'
        for key, value in filter_group:
            actual_value = task.get(key)

            # Verifica si el valor coincide o si solo se supone que el atributo debe existir
            if value is not None:
                current_match = (actual_value == value)
            else:
                # Si no se especifica un valor, verifique la existencia del atributo
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



