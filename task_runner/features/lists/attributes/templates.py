import os
from features.tasks.utils.json_manager import read_json_file

def check_template(directory, template_name):
    template_path = os.path.join(directory, 'templates', f"{template_name}.json")
    return os.path.exists(template_path)

def load_template(directory, template_name):
    """
    Load template data from a specified template file.
    
    Parameters:
        directory (str): The directory where templates are stored.
        template_name (str): The name of the template to load.
    
    Returns:
        dict: Template data.
    """
    if template_name:
        template_path = os.path.join(directory, 'templates', f"{template_name}.json")
        return read_json_file(template_path)
    return {}