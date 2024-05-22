import os
import subprocess
import argparse
from features.tasks.actions.cmd_add import add_task, add_task_properties, add_links, add_files
from features.tasks.actions.cmd_delete import delete_tasks, delete_task_properties, delete_link
from features.tasks.actions.cmd_move import move_task
from features.tasks.actions.cmd_check import check_task
from features.tasks.actions.cmd_edit import edit_task
from features.tasks.actions.cmd_rename import rename_task_name, rename_task_property_name
from features.tasks.actions.cmd_show import show_tasks, show_linked_tasks

from features.tasks.attributes.templates import check_template
from features.tasks.attributes.properties import parse_properties

from features.tasks.utils.json_manager import check_list_json

from features.lists.actions.cmd_add import add_list
from features.lists.actions.cmd_delete import delete_list
from features.lists.actions.cmd_rename import rename_list
from features.lists.actions.cmd_show import show_list_content, show_lists, show_filtered_tasks, show_my_day

# Obtiene el directorio donde se encuentra el script en ejecución
base_directory = os.path.dirname(os.path.abspath(__file__))
subdirectory = 'task_runner/.app_data'
directory = os.path.join(base_directory, subdirectory)
json_file_path = os.path.join(directory, 'app_data.json')

# Definiciones adicionales
extension_file = "typ"
default_list = "ib"

def main():
    parser = argparse.ArgumentParser(description="Task management script")
    subparsers = parser.add_subparsers(dest='command', required=True)



    list_parser = subparsers.add_parser('list', help="Manage lists")
    list_parser.add_argument('-a', '--add', nargs=2, metavar=('CATEGORY_NAME', 'ABBREVIATION'), help="Add a new list with tasks and files sections.")
    list_parser.add_argument('-d', '--delete', nargs=1, help="Delete a list with all its contents.")
    list_parser.add_argument('-r', '--rename', nargs=3, metavar=('OLD_NAME', 'NEW_NAME', 'NEW_ABBREVIATION'), help="Rename a list.")
    list_parser.add_argument('-s', '--show', nargs='?', const='', help="Show lists or tasks within a specific list.")
    list_parser.add_argument('-sf', '--show-filters', nargs='+', help="Show available filters for tasks within a specific list or apply filters. Usage: -sf LIST_ABBR [@filter='value' ...]")
    list_parser.add_argument('-sd', '--show-day', nargs='?', const='', help="Show tasks for the day, optionally specify a category")


    tasks_parser = subparsers.add_parser('tasks', help="Manage tasks")
    tasks_parser.add_argument('-a', '--add', nargs='+', help="Name(s) of the task(s) to add")
    tasks_parser.add_argument('-al', '--add-link', nargs='+', help="Add links to a task. Format: SRC_CATEGORY_ABBR SRC_TASK_NUMBER [DST_CATEGORY_ABBR DST_TASK_NUMBER ...]")
    tasks_parser.add_argument('-af', '--add-file', nargs='+', help="Path(s) of the file(s) to add")
    tasks_parser.add_argument('-ap', '--add-property', nargs='+', help="Add or update properties for a task. Format: CATEGORY_ABBR TASK_NUMBER @PROP='VALUE' [@PROP2='VALUE2' ...]")
    tasks_parser.add_argument('-ae', '--add-edit', nargs='+', help="Add a task and then edit it. Format: NAME [@PROP='VALUE' ...]")
    tasks_parser.add_argument('-d', '--delete', nargs='+', help="Name(s) of the task(s) to delete")
    tasks_parser.add_argument('-dl', '--delete-link', nargs=4, metavar=('SRC_CATEGORY_ABBR', 'SRC_TASK_NUMBER', 'DST_CATEGORY_ABBR', 'DST_TASK_NUMBER'), help="Delete a specific link from a task. Format: SRC_CATEGORY_ABBR SRC_TASK_NUMBER DST_CATEGORY_ABBR DST_TASK_NUMBER")
    tasks_parser.add_argument('-dp', '--delete-property', nargs='+', help="Delete properties from a task. Format: CATEGORY_ABBR TASK_NUMBER @PROP='VALUE' [@PROP2='VALUE2' ...]")
    tasks_parser.add_argument('-m', '--move', nargs='+', help="Move tasks from one list to another")
    tasks_parser.add_argument('-rn', '--rename-name', nargs=3, metavar=('CATEGORY_ABBR', 'TASK_NUMBER', 'NEW_NAME'), help="Modify the name of a task")
    tasks_parser.add_argument('-rp', '--rename-property', nargs=4, metavar=('CATEGORY_ABBR', 'TASK_NUMBER', 'OLD_PROP_NAME', 'NEW_PROP_NAME'), help="Modify the name of a property in a task")
    tasks_parser.add_argument('-s', '--show', nargs='+', help="Show the task file using specified viewer. Format: CATEGORY_ABBR TASK_NUMBER [--typst]")
    tasks_parser.add_argument('--typst', action='store_true', help="Use typst-preview to view the task")
    tasks_parser.add_argument('-sl', '--show-links', nargs=2, metavar=('CATEGORY_ABBR', 'TASK_NUMBER'), help="Show linked tasks. Format: CATEGORY_ABBR TASK_NUMBER")
    tasks_parser.add_argument('-c', '--check', nargs='+', help="Check tasks as completed. Format: CATEGORY TASK_NUMBERS...")
    tasks_parser.add_argument('-e', '--edit', nargs=2, metavar=('CATEGORY_ABBR', 'TASK_NUMBER'), help="Edit the specified task file")
    tasks_parser.add_argument('-u', '--uncheck', nargs='+', help="Uncheck tasks as incomplete. Format: CATEGORY TASK_NUMBERS...")
    tasks_parser.add_argument('-l', '--list', default=default_list, help="List abbreviation or full name to manage tasks")
    tasks_parser.add_argument('--template', help="Path to the template file to use for the task")

    args = parser.parse_args()

    if args.command == 'list':
        if args.add:
            category_name, abbreviation = args.add
            add_list(json_file_path, category_name, abbreviation)
        elif args.delete:
            category_name = args.delete[0]
            delete_list(json_file_path, category_name)
        elif args.rename:
            old_name, new_name, new_abbreviation = args.rename
            rename_list(json_file_path, old_name, new_name, new_abbreviation)
        elif args.show is not None:
            if args.show == '':
                show_lists(json_file_path)
            else:
                show_list_content(directory, json_file_path, args.show)
        elif args.show_filters is not None:
            if args.show_filters:
                list_abbr = args.show_filters[0]
                filters = args.show_filters[1:]
                show_filtered_tasks(directory, json_file_path, list_abbr, filters)
            else:
                print("Specify a list abbreviation to filter.")
        elif args.show_day == '':
            show_my_day(json_file_path)
        else:
            show_my_day(json_file_path, specific_categories=[args.show_day])

    elif args.command == 'tasks':
        if args.list and args.list != default_list and not check_list_json(json_file_path, args.list):
            print(f"\033[91mError: The list '{args.list}' does not exist.\033[0m")
            return

        if args.template and not check_template(directory, args.template):
            print(f"\033[91mError: The template '{args.template}' does not exist.\033[0m")
            return

        # Handling deletion of tasks
        if args.delete:
            commands = {}
            for command_str in args.delete:
                parts = command_str.split()
                list_abbr = parts[0]
                task_numbers = list(map(int, parts[1:]))
                commands.setdefault(list_abbr, []).extend(task_numbers)
            delete_tasks(json_file_path, commands)

        # Handling delete task property
        elif args.delete_property:
            category_abbr = args.delete_property[0]
            task_number = args.delete_property[1]
            properties = parse_properties(args.delete_property[2:]) if len(args.delete_property) > 2 else []
            delete_task_properties(directory, json_file_path, category_abbr, int(task_number), properties, args.template)

        elif args.delete_link:
            src_category_abbr, src_task_number, dst_category_abbr, dst_task_number = args.delete_link
            delete_link(json_file_path, src_category_abbr, src_task_number, dst_category_abbr, dst_task_number)


        # Handling adding tasks
        elif args.add:
            add_task(directory, json_file_path, extension_file, args.add, args.list, args.template)

        elif args.add_file:
            add_files(directory, json_file_path, args.add_file, args.list, args.template)

        elif args.add_edit:
            task_names = args.add_edit
            created_files = add_task(directory, json_file_path, extension_file, task_names, default_list, args.template)
            for file_path in created_files:
                if os.path.exists(file_path):
                    subprocess.run(['nvim', file_path])
                    print(f"Editing task file: {file_path}")

        elif args.add_link:
            src_category_abbr = args.add_link[0]
            src_task_number = args.add_link[1]
            links = args.add_link[2:]
            add_links(json_file_path, src_category_abbr, src_task_number, links)

        # Handling task property
        elif args.add_property:
            category_abbr = args.add_property[0]
            task_number = args.add_property[1]
            properties = parse_properties(args.add_property[2:]) if len(args.add_property) > 2 else []
            add_task_properties(directory, json_file_path, category_abbr, int(task_number), properties, args.template)

        # Handling moving tasks
        elif args.move:
            if len(args.move) < 3:
                print("Error: Move operation requires at least 3 arguments.")
                return
            src_category = args.move[0]
            dst_category = args.move[-1]
            task_numbers = list(map(int, args.move[1:-1]))
            move_task(json_file_path, src_category, task_numbers, dst_category)

        # Handling checking tasks
        elif args.check:
            category = args.check[0]
            task_numbers = list(map(int, args.check[1:]))
            check_task(json_file_path, category, task_numbers, True)

        # Handling unchecking tasks
        elif args.uncheck:
            category = args.uncheck[0]
            task_numbers = list(map(int, args.uncheck[1:]))
            check_task(json_file_path, category, task_numbers, False)

        # Handling task editing
        elif args.edit:
            category_abbr, task_number = args.edit
            task_number = int(task_number)
            edit_task(json_file_path, category_abbr, task_number)

        elif args.rename_name:
            category_abbr, task_number, new_name = args.rename_name
            rename_task_name(json_file_path, extension_file, category_abbr, int(task_number), new_name)

        elif args.rename_property:
            category_abbr, task_number, old_prop_name, new_prop_name = args.rename_property
            rename_task_property_name(json_file_path, category_abbr, int(task_number), old_prop_name, new_prop_name)
        
        elif args.show:
            category_abbr = args.show[0]
            task_number = args.show[1]
            preview = args.typst  # Directly use the flag set by argparse
            show_tasks(json_file_path, category_abbr, int(task_number), preview)
        
        elif args.show_links:
            category_abbr, task_number = args.show_links
            show_linked_tasks(directory, json_file_path, category_abbr, task_number)

if __name__ == "__main__":
    main()
