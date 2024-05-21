from features.tasks.utils.json_manager import read_json_file, write_json_file

def move_task(json_file_path, src_category_abbr, task_numbers, dst_category_abbr):
    """
    Move multiple tasks from one category to another and renumber tasks in the source category.
    """   
    data = read_json_file(json_file_path)

    src_category_name = next((name for name, details in data.items() if details.get('abbreviation') == src_category_abbr), None)
    dst_category_name = next((name for name, details in data.items() if details.get('abbreviation') == dst_category_abbr), None)

    if not src_category_name or not dst_category_name:
        print("One of the categories was not found.")
        return

    src_tasks = data[src_category_name].get('tasks', {})
    dst_tasks = data[dst_category_name].get('tasks', {})

    moved_tasks = []
    for task_number in sorted(task_numbers, reverse=True):  # Sort and reverse to maintain order when popping
        task_number_str = str(task_number)
        task = src_tasks.pop(task_number_str, None)
        if task:
            new_task_number = str(max([int(num) for num in dst_tasks.keys()], default=0) + 1)
            dst_tasks[new_task_number] = task
            moved_tasks.append((task_number_str, new_task_number))

    # Renumber the remaining tasks in the source category
    new_src_tasks = {}
    for i, (task_num, task) in enumerate(src_tasks.items(), start=1):
        new_src_tasks[str(i)] = task

    data[src_category_name]['tasks'] = new_src_tasks

    write_json_file(data, json_file_path)

    for src_num, dst_num in moved_tasks:
        print(f"\033[90m⫸\033[0m Task '{src_num}' moved from \033[95m{src_category_abbr}\033[0m to \033[95m{dst_category_abbr}\033[0m as new task number \033[92m{dst_num}\033[0m")
