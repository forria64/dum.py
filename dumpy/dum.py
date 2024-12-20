import mimetypes
import os
import sys
import pyperclip

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


def collect_text_files(directory_path):
    """
    Recursively collects all text files in a directory.
    """
    text_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            absolute_file_path = os.path.join(root, file)
            if is_text_file(absolute_file_path):
                relative_path = os.path.relpath(absolute_file_path, directory_path)
                text_files.append(relative_path)
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

