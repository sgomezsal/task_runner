import json

def read_json_file(json_file_path):
    with open(json_file_path, 'r') as file:
        return json.load(file)

def write_json_file(data, json_file_path):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_task_references(data, old_id, new_id, new_abbr):
    """
    Update all task references across the entire dataset.
    """
    old_ref = f"{old_id}"
    new_ref = f"{new_abbr} {new_id}"
    for category in data.values():
        for task_id, task in category.get('tasks', {}).items():
            if 'nodes' in task:
                task['nodes'] = [new_ref if node == old_ref else node for node in task['nodes']]

def move_task(json_file_path, src_category_abbr, task_numbers, dst_category_abbr):
    """
    Move multiple tasks from one category to another and renumber tasks in the source category.
    Update all references to the moved tasks in other tasks' nodes.
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
    for task_number in sorted(task_numbers, reverse=True):
        task_number_str = str(task_number)
        task = src_tasks.pop(task_number_str, None)
        if task:
            new_task_number = str(max([int(num) for num in dst_tasks.keys()], default=0) + 1)
            dst_tasks[new_task_number] = task
            moved_tasks.append((task_number_str, new_task_number))
            update_task_references(data, f"{src_category_abbr} {task_number_str}", new_task_number, dst_category_abbr)

    # Renumber the remaining tasks in the source category
    new_src_tasks = {}
    for i, (task_num, task) in enumerate(sorted(src_tasks.items(), key=lambda x: int(x[0])), start=1):
        new_src_tasks[str(i)] = task
        update_task_references(data, f"{src_category_abbr} {task_num}", str(i), src_category_abbr)

    data[src_category_name]['tasks'] = new_src_tasks

    write_json_file(data, json_file_path)

    for src_num, dst_num in moved_tasks:
        print(f"Task '{src_num}' moved from {src_category_abbr} to {dst_category_abbr} as new task number {dst_num}")
