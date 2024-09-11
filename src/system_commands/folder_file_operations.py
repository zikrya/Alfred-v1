import os

def resolve_path(path):
    """Resolve the user-specified path or use default system paths for known directories."""
    if path.lower() == "desktop":
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif path.lower() == "documents":
        return os.path.join(os.path.expanduser("~"), "Documents")
    else:
        return os.path.expanduser(path)

def create_folder(folder_name, path="."):
    """Create a folder at the specified path."""
    # Resolve the path
    full_path = os.path.join(resolve_path(path), folder_name)
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
            file.write("")
        return f"File '{file_name}' created at {full_path}."
    except Exception as e:
        return f"Error creating file '{file_name}': {e}"
