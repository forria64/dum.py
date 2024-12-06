import mimetypes
import os
import sys

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

def write_code_summary(directory_path, text_files):
    """
    Writes a summary of text files and their content to a 'code_summary.txt' file.
    """
    summary_path = os.path.join(directory_path, 'code_summary.txt')
    with open(summary_path, 'w', encoding='utf-8', errors='replace') as summary_file:
        for relative_path in text_files:
            absolute_file_path = os.path.join(directory_path, relative_path)
            summary_file.write(f"File: {relative_path}\n")
            summary_file.write(f"{'-' * 80}\n")
            try:
                with open(absolute_file_path, 'r', encoding='utf-8', errors='replace') as text_file:
                    summary_file.write(text_file.read())
            except Exception as e:
                summary_file.write(f"Error reading file: {e}\n")
            summary_file.write(f"\n{'=' * 80}\n\n")
    
    return summary_path

def main():
    """
    Main function to execute the script. 
    """
    if len(sys.argv) < 2:
        print("Usage: python collect_text_files.py <relative_path_to_directory>")
        sys.exit(1)

    relative_directory_path = sys.argv[1]
    absolute_directory_path = os.path.abspath(relative_directory_path)

    if not os.path.isdir(absolute_directory_path):
        print(f"Error: The path '{relative_directory_path}' is not a valid directory.")
        sys.exit(1)

    text_files = collect_text_files(absolute_directory_path)
    summary_file_path = write_code_summary(absolute_directory_path, text_files)
    
    print(f"Code summary written to: {os.path.abspath(summary_file_path)}")

if __name__ == "__main__":
    main()

