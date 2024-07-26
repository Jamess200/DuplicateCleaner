import os
import hashlib
import shutil
import logging
from datetime import datetime
from tabulate import tabulate

def get_file_hash(file_path):
    """Generate a hash for a file"""
    hash_algo = hashlib.md5()  # Initialise the MD5 hash algorithm
    with open(file_path, 'rb') as f:  # Open the file in binary read mode
        while True:
            chunk = f.read(4096)  # Read the file in chunks of 4096 bytes
            if not chunk:
                break  # Exit the loop if the chunk is empty (end of file)
            hash_algo.update(chunk)  # Update the hash with each chunk
    return hash_algo.hexdigest()  # Return the hexadecimal digest of the hash


def find_duplicates(directory):
    """Find duplicate files in a directory and keep the most recent one"""
    hashes = {}
    duplicates = []

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_hash = get_file_hash(file_path)
            file_mtime = os.path.getmtime(file_path)
            file_ctime = os.path.getctime(file_path)
            file_size = os.path.getsize(file_path)

            if file_hash in hashes:
                if file_mtime > hashes[file_hash]['mtime']:
                    duplicates.append(hashes[file_hash])
                    hashes[file_hash] = {'path': file_path, 'mtime': file_mtime, 'ctime': file_ctime, 'size': file_size}
                else:
                    duplicates.append({'path': file_path, 'mtime': file_mtime, 'ctime': file_ctime, 'size': file_size})
            else:
                hashes[file_hash] = {'path': file_path, 'mtime': file_mtime, 'ctime': file_ctime, 'size': file_size}

    return duplicates, hashes

def backup_files(file_list, backup_directory):
    """Backup files to a specified directory"""
    os.makedirs(backup_directory, exist_ok=True)
    for file_info in file_list:
        file_path = file_info['path']
        try:
            shutil.copy(file_path, backup_directory)
            print(f"Backed up: {file_path}")
        except Exception as e:
            print(f"Error backing up {file_path}: {e}")

def delete_files(file_list):
    """Delete files without individual confirmation"""
    for file_info in file_list:
        file_path = file_info['path']
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
            logging.info(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
            logging.error(f"Error deleting {file_path}: {e}")

def format_file_info(file_info):
    """Format file information for display"""
    file_path = file_info['path']
    file_size = file_info['size']
    file_ctime = datetime.fromtimestamp(file_info['ctime']).strftime('%Y-%m-%d %H:%M:%S')
    file_mtime = datetime.fromtimestamp(file_info['mtime']).strftime('%Y-%m-%d %H:%M:%S')
    return [file_path, file_size, file_ctime, file_mtime]

def remove_empty_folders(directory):
    """Remove empty folders in the specified directory"""
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            if not os.listdir(folder_path):  # Check if the folder is empty
                try:
                    os.rmdir(folder_path)
                    print(f"Removed empty folder: {folder_path}")
                    logging.info(f"Removed empty folder: {folder_path}")
                except Exception as e:
                    print(f"Error removing folder {folder_path}: {e}")
                    logging.error(f"Error removing folder {folder_path}: {e}")

if __name__ == "__main__":
    directory_to_scan = "C:\\Users\\James\\Desktop\\TestDup"  # Your test directory
    backup_directory = "C:\\Users\\James\\Desktop\\BackupCopy"  # Separate backup directory
    log_file = "duplicate_files_log.txt"

    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    duplicates, kept_files = find_duplicates(directory_to_scan)

    if duplicates:
        print(f"Found {len(duplicates)} duplicate files.")

        backup_files(duplicates, backup_directory)

        # Show the files being kept
        print("\nThe following files will be kept (most recent versions):")
        kept_files_formatted = [format_file_info(file_info) for file_info in kept_files.values()]
        print(tabulate(kept_files_formatted, headers=["Path", "Size (bytes)", "Creation Date", "Modification Date"]))

        # Show the files selected for deletion
        print("\nThe following files are selected for deletion:")
        duplicates_formatted = [format_file_info(file_info) for file_info in duplicates]
        print(tabulate(duplicates_formatted, headers=["Path", "Size (bytes)", "Creation Date", "Modification Date"]))

        # Ask for a single confirmation to delete all selected files
        user_input = input("\nDo you want to delete all the above files? (yes/no): ").strip().lower()
        if user_input == 'yes':
            delete_files(duplicates)
            # Remove empty folders after deletion
            remove_empty_folders(directory_to_scan)
        else:
            print("Deletion aborted.")
    else:
        print("No duplicate files found.")

    # Optionally, remove empty folders even if no duplicates were found
    remove_empty_folders(directory_to_scan)
