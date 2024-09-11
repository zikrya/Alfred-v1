import os
from collections import deque

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
    full_path = os.path.join(resolve_path(path), file_name)
    try:
        with open(full_path, 'w') as file:
            file.write("")
        return f"File '{file_name}' created at {full_path}."
    except Exception as e:
        return f"Error creating file '{file_name}': {e}"

def list_files_and_folders(path="."):
    """List all files and folders in the specified directory."""
    try:
        return os.listdir(path)
    except Exception as e:
        return f"Error accessing the directory: {e}"

def read_file_contents(filepath):
    """Read and return the contents of the specified file."""
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file '{filepath}': {e}"

def is_hidden_or_system_folder(path):
    """Check if a folder is hidden or part of a system directory."""
    return any(part.startswith('.') for part in path.split(os.sep))

def has_access(path):
    """Check if the current user has access permissions to the given path."""
    return os.access(path, os.R_OK | os.X_OK)

def search_for_folder(foldername):
    """Efficiently search for a folder through common user-accessible directories."""
    search_paths = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Documents"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Pictures"),
        os.path.join(os.path.expanduser("~"), "Music"),
        os.path.join(os.path.expanduser("~"), "Movies"),
    ]

    result = []
    queue = deque(search_paths)

    try:
        while queue:
            current_path = queue.popleft()

            # Skip hidden or system directories
            if is_hidden_or_system_folder(current_path) or not has_access(current_path):
                continue

            try:
                with os.scandir(current_path) as it:
                    for entry in it:
                        if entry.is_dir(follow_symlinks=False):
                            if entry.name == foldername:
                                result.append(os.path.join(current_path, entry.name))
                            queue.append(entry.path)
            except PermissionError:
                continue
            except Exception as e:
                continue

        if result:
            return f"Folder '{foldername}' found at: {result[0]}"
        else:
            return f"Folder '{foldername}' not found."

    except Exception as e:
        return f"Error occurred: {e}"

def search_for_file(filename, search_path="."):
    """Efficiently search for a file through common user-accessible directories or a given search path."""
    search_paths = [
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.join(os.path.expanduser("~"), "Documents"),
        os.path.join(os.path.expanduser("~"), "Downloads"),
        os.path.join(os.path.expanduser("~"), "Pictures"),
        os.path.join(os.path.expanduser("~"), "Music"),
        os.path.join(os.path.expanduser("~"), "Movies"),
    ]

    if search_path != ".":
        search_paths = [search_path]

    result = []
    queue = deque(search_paths)

    try:
        while queue:
            current_path = queue.popleft()

            # Skip hidden or system directories
            if is_hidden_or_system_folder(current_path) or not has_access(current_path):
                continue

            try:
                with os.scandir(current_path) as it:
                    for entry in it:
                        if entry.is_file(follow_symlinks=False):
                            if entry.name == filename:
                                result.append(os.path.join(current_path, entry.name))
                        elif entry.is_dir(follow_symlinks=False):
                            queue.append(entry.path)
            except PermissionError:
                continue
            except Exception as e:
                continue

        if result:
            return f"File '{filename}' found at: {result[0]}"
        else:
            return f"File '{filename}' not found."

    except Exception as e:
        return f"Error occurred: {e}"

