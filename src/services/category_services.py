from json_manager.config_json import read_json_config
from json_manager.services import add_category_to_json
    
def add_category(args):
    category_name = args.category_name
    abbreviation = args.abbreviation

    config = read_json_config()
    message = add_category_to_json(config, category_name, abbreviation)
    print(message)

def validate_category(data, category_abbreviation, default_category):
    category = next
    ((cat for cat, details in data.items() if details.get('abbreviation') == category_abbreviation), None)
    
    if category_abbreviation is None or category_abbreviation == "":
        if default_category not in data:
            raise ValueError(f"Default category '{default_category}' does not exist.")
        return default_category
    
    if not category:
        raise ValueError(f"The category abbreviation '{category_abbreviation}' does not exist.")

    return category