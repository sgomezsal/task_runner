from datetime import datetime
import os

def create_task_file(title, config):
    """Creates a file for the task with a given title and according to the specified configuration settings."""
    try:
        # Preparar nombre del archivo y ruta completa
        file_directory = os.path.expanduser(config['task_directory'])
        file_extension = config.get('file_extension', '.md')
        file_name = f"{title.replace(' ', '_')}{file_extension}".lower()
        file_path = os.path.join(file_directory, file_name)

        # Crear el archivo
        os.makedirs(file_directory, exist_ok=True)
        with open(file_path, 'w') as file:
            file.write("")

        return file_path
    except KeyError as e:
        raise KeyError(f"Missing configuration parameter: {e}")
    except Exception as e:
        raise Exception(f"Failed to create task file: {e}")
