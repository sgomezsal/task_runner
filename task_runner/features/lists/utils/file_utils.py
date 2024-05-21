import os 

def ensure_directory_exists(directory):
    """
    Ensures that a directory exists, creating it if it does not.
    
    Parameters:
        directory (str): The directory path.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)