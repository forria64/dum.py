```
░░░░░░  ░░    ░░ ░░░    ░░░    ░░░░░░  ░░    ░░ 
▒▒   ▒▒ ▒▒    ▒▒ ▒▒▒▒  ▒▒▒▒    ▒▒   ▒▒  ▒▒  ▒▒  
▒▒   ▒▒ ▒▒    ▒▒ ▒▒ ▒▒▒▒ ▒▒    ▒▒▒▒▒▒    ▒▒▒▒   
▓▓   ▓▓ ▓▓    ▓▓ ▓▓  ▓▓  ▓▓    ▓▓         ▓▓    
██████   ██████  ██      ██ ██ ██         ██    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v1.1-beta
A Python tool for analyzing and summarizing text files,
designed to streamline AI workflows by identifying,
validating, and summarizing text files within a directory.

This script is ideal for preparing text-based datasets for
machine learning, natural language processing, or documentation analysis.

FEATURES

    1. Text File Validation: Ensures files are valid text files
    by checking MIME types and analyzing binary content
    to exclude non-text files.

    2. Dataset Preparation: Automates the discovery and validation
    of text files for AI workflows.

    3. Summarized Output: Generates a code_summary.txt file containing 
    the content of all valid text files for quick reference or preprocessing.
    
    4. Error Handling: Handles unreadable files gracefully and logs errors.
    
INSTALLATION

    REQUIRED PACKAGES:
        -git
        -python3
        -pipx
    RUN:
        pipx install git+https://github.com/forria64/dum.py.git#egg=dumpy

USAGE

    dumpy <dataset directory>
