import os

def create_folder(folder_name, path="."):
    """Create a folder at the specified path"""
    full_path = os.path.join(path, folder_name)
    try:
        os.makedirs(full_path, exist_ok=True)
        return f"Folder '{folder_name}' created at {full_path}."
    except Exception as e:
        return f"Error creating folder '{folder_name}': {e}"

def create_file(file_name, path="."):
    """Create a file at the specified path"""
    full_path = os.path.join(path, file_name)
    try:
        with open(full_path, 'w') as file:
            file.write("")  # Create an empty file
        return f"File '{file_name}' created at {full_path}."
    except Exception as e:
        return f"Error creating file '{file_name}': {e}"
