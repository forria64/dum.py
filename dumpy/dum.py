import mimetypes
import os
import sys
import pyperclip
import fnmatch

def is_text_file(file_path):
    """
    Determines if a file is a text file by:
    1. Checking the MIME type.
    2. Analyzing the file's binary content for non-text characters.
    
    Args:
        file_path (str): Path to the file being checked.
    
    Returns:
        bool: True if the file is a text file, False otherwise.
    """
    # Check if the file has a `.rs` extension
    if file_path.endswith('.rs'):
        return True
    if file_path.endswith('.js'):
        return True
    if file_path.endswith('.json'):
        return True

    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and not mime_type.startswith('text/'):
        return False

    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:  # Null byte indicates binary content
                return False
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False
    return True

def load_gitignore_patterns(directory_path):
    """
    Loads ignore patterns from a .gitignore file in the given directory.
    Also ensures that the .git directory is always ignored.
    
    Args:
        directory_path (str): The root directory to look for .gitignore.
    
    Returns:
        list: A list of ignore patterns.
    """
    patterns = []
    gitignore_path = os.path.join(directory_path, ".gitignore")
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line == "" or line.startswith("#"):
                        continue
                    patterns.append(line)
        except Exception as e:
            print(f"Error reading .gitignore: {e}")
    # Always ignore the .git directory.
    if ".git/" not in patterns and ".git" not in patterns:
        patterns.append(".git/")
    return patterns


def is_ignored(relative_path, ignore_patterns):
    """
    Determines if a given relative path matches any of the ignore patterns.
    
    Args:
        relative_path (str): The file or directory path relative to the root.
        ignore_patterns (list): List of ignore patterns.
    
    Returns:
        bool: True if the path should be ignored, False otherwise.
    """
    # Normalize the path to use forward slashes.
    norm_path = relative_path.replace(os.sep, "/")
    for pattern in ignore_patterns:
        if pattern.endswith("/"):
            # For directory patterns, extract the basename.
            base = os.path.basename(pattern.rstrip("/"))
            # Check if any component of the path matches the directory basename.
            if base in norm_path.split("/"):
                return True
        else:
            # For other patterns, try matching against the full path or its basename.
            if fnmatch.fnmatch(norm_path, pattern) or fnmatch.fnmatch(os.path.basename(norm_path), pattern):
                return True
    return False



def collect_text_files(directory_path):
    """
    Recursively collects all text files in a directory,
    while excluding files and directories specified in .gitignore.
    
    Args:
        directory_path (str): The root directory to search.
    
    Returns:
        list: List of relative paths to text files.
    """
    ignore_patterns = load_gitignore_patterns(directory_path)
    text_files = []
    for root, dirs, files in os.walk(directory_path):
        rel_root = os.path.relpath(root, directory_path)
        if rel_root == ".":
            rel_root = ""
        # Exclude ignored directories from traversal
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(rel_root, d) if rel_root else d, ignore_patterns)]
        for file in files:
            rel_file = os.path.join(rel_root, file) if rel_root else file
            if is_ignored(rel_file, ignore_patterns):
                continue
            absolute_file_path = os.path.join(root, file)
            if is_text_file(absolute_file_path):
                text_files.append(rel_file)
    return text_files

def generate_summary(directory_path, text_files):
    """
    Generates a summary string of all text files and their contents.
    
    Args:
        directory_path (str): The directory containing the text files.
        text_files (list): List of relative paths to text files.
    
    Returns:
        str: The concatenated summary content.
    """
    summary_content = []
    for relative_path in text_files:
        absolute_file_path = os.path.join(directory_path, relative_path)
        summary_content.append(f"File: {relative_path}")
        summary_content.append('-' * 80)
        try:
            with open(absolute_file_path, 'r', encoding='utf-8', errors='replace') as text_file:
                summary_content.append(text_file.read())
        except Exception as e:
            summary_content.append(f"Error reading file: {e}")
        summary_content.append('=' * 80)
        summary_content.append('')  # Blank line after each file's content
    return "\n".join(summary_content)


def main():
    """
    Main function to execute the script. 
    
    Usage:
        python dum.py <directory> [-f output_file.txt]
        
    By default, if -f is not provided, the concatenated contents are copied to clipboard 
    and the user is notified in the terminal.
    If -f is provided, the concatenated contents are written to the specified file.
    """
    if len(sys.argv) < 2:
        print("Usage: python dum.py <relative_path_to_directory> [-f output_file.txt]")
        sys.exit(1)

    # Parse arguments
    relative_directory_path = sys.argv[1]
    output_file = None
    if "-f" in sys.argv:
        f_index = sys.argv.index("-f")
        if f_index + 1 < len(sys.argv):
            output_file = sys.argv[f_index + 1]
        else:
            print("Error: -f flag provided but no file specified.")
            sys.exit(1)

    absolute_directory_path = os.path.abspath(relative_directory_path)

    if not os.path.isdir(absolute_directory_path):
        print(f"Error: The path '{relative_directory_path}' is not a valid directory.")
        sys.exit(1)

    text_files = collect_text_files(absolute_directory_path)
    summary_content = generate_summary(absolute_directory_path, text_files)

    if output_file:
        # Write concatenated contents to the specified file
        with open(output_file, 'w', encoding='utf-8', errors='replace') as out_f:
            out_f.write(summary_content)
        print(f"Concatenated contents written to: {os.path.abspath(output_file)}")
    else:
        # Copy concatenated contents to clipboard
        pyperclip.copy(summary_content)
        print("Concatenated contents have been copied to the clipboard.")

if __name__ == "__main__":
    main()

