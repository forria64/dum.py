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
    # Step 1: Check the MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and not mime_type.startswith('text/'):
        # If MIME type exists and doesn't start with 'text/', it's not a text file.
        return False

    # Step 2: Check for binary content by reading a chunk of the file
    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)  # Read the first 1024 bytes
            if b'\0' in chunk:  # Null byte indicates binary content
                return False
            else:
                return True
    except Exception as e:
        # Log errors for inaccessible files
        print(f"Error reading file {file_path}: {e}")
        return False

def collect_text_files(directory_path):
    """
    Recursively collects all text files in a directory.

    Args:
        directory_path (str): Path to the directory to search for text files.
    
    Returns:
        list: A list of relative paths to text files in the directory.
    """
    text_files = []
    
    # Walk through the directory structure
    for root, _, files in os.walk(directory_path):
        for file in files:
            absolute_file_path = os.path.join(root, file)
            if is_text_file(absolute_file_path):
                # Convert absolute path to a relative path for portability
                relative_path = os.path.relpath(absolute_file_path, directory_path)
                text_files.append(relative_path)

    return text_files

def write_code_summary(directory_path, text_files):
    """
    Writes a summary of text files and their content to a 'code_summary.txt' file.

    Args:
        directory_path (str): Base directory path.
        text_files (list): List of relative paths to text files.
    """
    summary_path = os.path.join(directory_path, 'code_summary.txt')

    with open(summary_path, 'w', encoding='utf-8', errors='replace') as summary_file:
        for relative_path in text_files:
            absolute_file_path = os.path.join(directory_path, relative_path)
            summary_file.write(f"File: {relative_path}\n")
            summary_file.write(f"{'-' * 80}\n")
            try:
                # Read and write file content to the summary file
                with open(absolute_file_path, 'r', encoding='utf-8', errors='replace') as text_file:
                    summary_file.write(text_file.read())
            except Exception as e:
                # Log any errors while reading files
                summary_file.write(f"Error reading file: {e}\n")
            summary_file.write(f"\n{'=' * 80}\n\n")

def main():
    """
    Main function to execute the script. Parses command-line arguments, validates
    the input directory, collects text files, and writes a summary.
    """
    if len(sys.argv) < 2:
        # Display usage instructions if no directory argument is provided
        print("Usage: python collect_text_files.py <relative_path_to_directory>")
        sys.exit(1)

    # Convert the provided relative directory path to an absolute path
    relative_directory_path = sys.argv[1]
    absolute_directory_path = os.path.abspath(relative_directory_path)

    # Check if the given path is a valid directory
    if not os.path.isdir(absolute_directory_path):
        print(f"Error: The path '{relative_directory_path}' is not a valid directory.")
        sys.exit(1)

    # Collect all text files in the directory
    text_files = collect_text_files(absolute_directory_path)

    # Generate the code summary and save it in the specified directory
    write_code_summary(absolute_directory_path, text_files)
    print(f"Code summary written to: {os.path.join(relative_directory_path, 'code_summary.txt')}")

if __name__ == "__main__":
    # Entry point for the script
    main()
