import logging
import os
from colorama import Fore, Style
from json_manager.config_json import read_json_config
from json_manager.utils import save_json
from json_manager.data_json import read_json_data, ensure_json_data_file_exists
from utils.items import add_item_to_category, check_item_existence
from services.category_services import validate_category

def add_task(args):
    config = read_json_config()
    titles = args.title
    category_abbreviation = args.category if hasattr(args, 'category') and args.category else None

    try:
        ensure_json_data_file_exists(config)
        data = read_json_data(config)

        try:
            category = validate_category(data, category_abbreviation, config.get('default_category'))
        except ValueError as e:
            print(f"{Fore.RED}✗ Error:{Style.RESET_ALL} {e}")
            return         
        
        existing_tasks = check_item_existence(data, titles)

        for title in titles:
            if title in existing_tasks:
                print(f"{Fore.RED}✗ Error:{Style.RESET_ALL} A task with the name '{title}' already exists in '{existing_tasks[title]}'.")
                continue

            file_path, index = add_item_to_category(title, category, config, data, "task")
            print(f"{Fore.GREEN}✓{Style.RESET_ALL} {Fore.LIGHTBLACK_EX}Added task:{Style.RESET_ALL} {title} {Fore.MAGENTA}{data[category]['abbreviation']} {index}{Style.RESET_ALL}")
            logging.info(f"Task added: {title} - Category: {category} {data[category]['abbreviation']} - Index: {index}")
            logging.info(f"Task file created at: {file_path}")

    except Exception as e:
        logging.error(f"An error occurred while adding tasks: {e}")
        print(f"{Fore.RED}✗ Error:{Style.RESET_ALL} {e}")

def delete_item(args):
    config = read_json_config()
    category_abbreviation = args.category
    item_index = int(args.index) - 1  # Explicit conversion to int, then adjust to 0-based index

    data = read_json_data(config['data_file_path'])

    if category_abbreviation not in data:
        print(f"{Fore.RED}✗ Error:{Style.RESET_ALL} Category '{category_abbreviation}' does not exist.")
        return

    if item_index >= len(data[category_abbreviation]['items']):
        print(f"{Fore.RED}✗ Error:{Style.RESET_ALL} Item index {item_index} does not exist in category '{category_abbreviation}'.")
        return

    # Retrieve item details for confirmation and deletion
    item = data[category_abbreviation]['items'].pop(item_index)
    file_path = item['file']

    # Save the updated JSON data
    save_json(data, config['data_file_path'])

    # Attempt to delete the file associated with the item
    try:
        os.remove(file_path)
        confirmation_message = f"{Fore.GREEN}✓{Style.RESET_ALL} Successfully deleted '{item['title']}' from '{category_abbreviation}'."
        logging.info(f"Deleted item: {item['title']} - File: {file_path}")
        return confirmation_message
    except Exception as e:
        logging.error(f"Failed to delete file {file_path}: {e}")
        return f"{Fore.RED}✗ Error:{Style.RESET_ALL} Failed to delete file {file_path}: {e}"
