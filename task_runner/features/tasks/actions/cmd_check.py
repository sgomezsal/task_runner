from features.tasks.utils.json_manager import read_json_file, write_json_file

def check_task(json_file_path, category_abbr, task_numbers, mark_complete):
    data = read_json_file(json_file_path)
    category = next((cat for cat, details in data.items() if details.get('abbreviation') == category_abbr), None)

    if not category:
        print(f"No category found for abbreviation '{category_abbr}'.")
        return

    tasks = data[category].get('tasks', {})
    for task_number in task_numbers:
        task_str = str(task_number)
        if task_str in tasks:
            tasks[task_str]['complete'] = mark_complete
        else:
            print(f"No task number {task_number} in category '{category}'.")
    
    write_json_file(data, json_file_path)
    
    status = "completed" if mark_complete else "incomplete"
    print(f"Tasks {task_numbers} in category '{category}' marked as {status}.")
