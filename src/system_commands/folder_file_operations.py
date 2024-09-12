import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def resolve_path(path):
    """Resolve the user-specified path or use default system paths for known directories."""
    if path.lower() == "desktop":
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif path.lower() == "documents":
        return os.path.join(os.path.expanduser("~"), "Documents")
    elif path.lower() == "downloads":
        return os.path.join(os.path.expanduser("~"), "Downloads")
    else:
        return os.path.expanduser(path)

def create_folder(folder_name, path="."):
    """Create a folder at the specified path."""
    full_path = os.path.join(resolve_path(path), folder_name)
    try:
        os.makedirs(full_path, exist_ok=True)
        return f"Folder '{folder_name}' created at {full_path}."
    except Exception as e:
        return f"Error creating folder '{folder_name}': {e}"

def create_file(file_name, path="."):
    """Create a file at the specified path."""
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


# New optimized search functions using ThreadPoolExecutor for parallel search
def search_target_scandir(path, target_name):
    """Scan a directory for a file or folder, and return the path if found."""
    try:
        with os.scandir(path) as entries:
            subdirs = []
            for entry in entries:
                try:
                    # Check if entry is a file or directory and matches the target
                    if (entry.is_file() or entry.is_dir()) and entry.name == target_name:
                        return entry.path  # Target found, return its path
                    elif entry.is_dir(follow_symlinks=False):
                        subdirs.append(entry.path)
                except (PermissionError, OSError):
                    continue  # Skip directories with permission issues
            return subdirs
    except (PermissionError, OSError):
        return []

def search_target_parallel(root_directory, target_name, max_workers=8):
    """Search for the target file or folder in parallel."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(search_target_scandir, root_directory, target_name)]
        found_target = None
        while futures:
            future = futures.pop(0)
            subdirs = future.result()

            if isinstance(subdirs, str):  # Target found
                found_target = subdirs
                break
            else:
                for subdir in subdirs:
                    futures.append(executor.submit(search_target_scandir, subdir, target_name))

        if found_target:
            return f"Target found: {found_target}"
        else:
            return f"Target '{target_name}' not found."

def search_for_file(filename, search_path="/"):
    """Search for a file in the given path using parallel processing."""
    return search_target_parallel(search_path, filename)

def search_for_folder(foldername, search_path="/"):
    """Search for a folder in the given path using parallel processing."""
    return search_target_parallel(search_path, foldername)

def append_to_file(file_path, content):
    """Append content to an existing file."""
    try:
        with open(file_path, 'a') as file:
            file.write(content + "\n")
        return f"Content appended to {file_path} successfully."
    except Exception as e:
        return f"Error appending to file '{file_path}': {e}"

def search_and_append_to_file(file_name, content, search_path="/"):
    """Search for a file and append content to it."""
    file_path = search_for_file(file_name, search_path)

    if isinstance(file_path, str) and "found" in file_path:
        return append_to_file(file_path.split(": ")[1], content)
    else:
        return f"File '{file_name}' not found in the search path."
