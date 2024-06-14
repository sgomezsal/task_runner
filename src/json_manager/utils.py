import json
import os

def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def save_json(data, filepath, mode='w', seek_start=True):
    with open(filepath, mode) as file:
        if seek_start:
            file.seek(0)
            file.truncate()
        json.dump(data, file, indent=4)

def read_json_file(file_path):
    """Lee un archivo JSON desde una ruta específica y devuelve su contenido como un diccionario."""
    try:
        with open(os.path.expanduser(file_path), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Error decodificando el archivo JSON: {file_path}")
