<div align="center">
  <h1>Duplicate File Manager</h1>
  <p><img src="img/duplicate_file_manager_banner.png" alt="Duplicate File Manager Banner" style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover;"></p>
</div>

Duplicate File Manager is a Python script designed to help you manage duplicate files in a directory. It scans for duplicate files, backs up the duplicates, and optionally deletes them, keeping only the most recent version. It also provides an option to remove empty folders.

## Features

- **Hash-Based Duplication Detection**: Uses MD5 hashing to identify duplicate files.
- **Backup and Deletion**: Automatically backs up and deletes duplicate files based on user confirmation.
- **Logging**: Logs actions to a file for easy tracking and review.
- **Remove Empty Folders**: Cleans up empty folders after deleting duplicates.

## Usage

1. **Setup**: Specify the directory to scan for duplicates and the backup directory.
2. **Execution**: Run the script to find and manage duplicate files.
3. **Confirmation**: Confirm before deleting duplicate files.

## Requirements

- Python 3.x
- `tabulate` library: Install using `pip install tabulate`

## How It Works

The script goes through the following steps:

1. **File Hashing**: Computes an MD5 hash for each file to detect duplicates.
2. **Duplicate Handling**: Compares files based on their hash and modification time, backing up and/or deleting duplicates as configured.
3. **Logging**: Logs all actions, including backups and deletions, in a log file.
4. **Folder Cleanup**: Optionally removes empty folders after duplicates are handled.

## Configuration

Set the following variables in the script:

- `directory_to_scan`: The directory where the script will search for duplicate files.
- `backup_directory`: The directory where backup copies of duplicate files will be saved.
- `log_file`: The file where logs will be written.

Example:

```python
directory_to_scan = "C:\\TestDup"  # Your test directory
backup_directory = "C:\\BackupCopy"  # Separate backup directory
log_file = "duplicate_files_log.txt"
```

## Running the Script
1. **Install Dependencies**: Make sure you have Python and the tabulate library installed. You can install the tabulate library using pip:
```python
pip install tabulate
```

2. **Run the Script**: Execute the script using Python. You can do this by navigating to the directory containing your script and running:
```python
python your_script_name.py
```
Replace your_script_name.py with the actual name of your Python script.

3. **Follow Prompts**: The script will display a list of duplicate files and ask for confirmation before deleting them. Review the list and if you agree, type yes when prompted to delete the duplicates.