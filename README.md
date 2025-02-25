```
░░░░░░  ░░    ░░ ░░░    ░░░    ░░░░░░  ░░    ░░ 
▒▒   ▒▒ ▒▒    ▒▒ ▒▒▒▒  ▒▒▒▒    ▒▒   ▒▒  ▒▒  ▒▒  
▒▒   ▒▒ ▒▒    ▒▒ ▒▒ ▒▒▒▒ ▒▒    ▒▒▒▒▒▒    ▒▒▒▒   
▓▓   ▓▓ ▓▓    ▓▓ ▓▓  ▓▓  ▓▓    ▓▓         ▓▓    
██████   ██████  ██      ██ ██ ██         ██    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v1.2-beta
```
A Python tool for analyzing and summarizing text files,
designed to streamline AI workflows by identifying,
validating, and summarizing text files within a directory.

This script is ideal for preparing text-based datasets for
machine learning, natural language processing, or documentation analysis.

**FEATURES**

1. **Text File Validation:**  
   Ensures files are valid text files by checking MIME types and analyzing binary content to exclude non-text files.

2. **Dataset Preparation:**  
   Automates the discovery and validation of text files for AI workflows.

3. **Summarized Output:**  
   Copies or generates a file containing the content of all valid text files for quick reference or preprocessing.

4. **.gitignore Support:**  
   Automatically reads a `.gitignore` file (if present in the target directory) and excludes files and directories matching its patterns. This ensures that only the relevant text files are processed.

5. **Error Handling:**  
   Handles unreadable files gracefully and logs errors.
    
**INSTALLATION**

- **REQUIRED PACKAGES:**
  - git
  - python3
  - pipx

- **RUN:**
```bash
pipx install git+https://github.com/forria64/dum.py.git#egg=dumpy
```
**USAGE**
```bash
dumpy <dataset_directory> [-f output_file.txt]
```
By default, if -f is not provided, the concatenated contents are copied to clipboard and the user is notified in the terminal. If -f is provided, the concatenated contents are written to the specified file.
