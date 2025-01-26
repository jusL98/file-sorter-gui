# Imports
import os
import shutil
from datetime import datetime
from PyQt5 import QtWidgets

ERROR_MESSAGES = {
    "loading_config": "Failed to load configuration: {}",
    "source_not_exist": "Source directory does not exist.",
    "target_not_exist": "Target directory does not exist.",
    "no_files_to_move": "No files to move.",
    "logging_error": "Failed to write to log file: {}"
}

class FileSorterApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Sorter By Date")
        self.setGeometry(100, 100, 600, 300)

        # Layout
        layout = QtWidgets.QVBoxLayout()


        # Source Directory
        self.source_label = QtWidgets.QLabel("Source Directory:")
        self.source_entry = QtWidgets.QLineEdit()
        self.source_button = QtWidgets.QPushButton("Browse")
        self.source_button.clicked.connect(self.browse_source)
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_entry)
        layout.addWidget(self.source_button)

        # Target Directory
        self.target_label = QtWidgets.QLabel("Target Directory:")
        self.target_entry = QtWidgets.QLineEdit()
        self.target_button = QtWidgets.QPushButton("Browse")
        self.target_button.clicked.connect(self.browse_target)
        layout.addWidget(self.target_label)
        layout.addWidget(self.target_entry)
        layout.addWidget(self.target_button)

        # Backup Option
        self.backup_var = QtWidgets.QCheckBox("Enable Backup")
        layout.addWidget(self.backup_var)

        # File Types to Include
        self.include_label = QtWidgets.QLabel("File Types to Include (comma-separated):")
        self.include_entry = QtWidgets.QLineEdit()
        layout.addWidget(self.include_label)
        layout.addWidget(self.include_entry)

        # File Types to Exclude
        self.exclude_label = QtWidgets.QLabel("File Types to Exclude (comma-separated):")
        self.exclude_entry = QtWidgets.QLineEdit()
        layout.addWidget(self.exclude_label)
        layout.addWidget(self.exclude_entry)

        # Start Sorting Button
        self.start_button = QtWidgets.QPushButton("Start Sorting")
        self.start_button.clicked.connect(self.start_sorting)
        layout.addWidget(self.start_button)


        # Set Layout
        self.setLayout(layout)

    def browse_source(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if directory:
            self.source_entry.setText(directory)

    def browse_target(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Target Directory")
        if directory:
            self.target_entry.setText(directory)

    def validate(self):
        self.source_directory = self.source_entry.text()
        self.target_directory = self.target_entry.text()
        self.backup_wanted = self.backup_var.isChecked()

        # Update log file and backup directory paths.
        self.log_file = os.path.join(self.target_directory, "log.txt")
        self.backup_directory = os.path.join(self.target_directory, "_BACKUP_")

        # Get file types to include and exclude from the entries.
        self.file_types_to_include = [ext.strip() for ext in self.include_entry.text().split(',') if ext.strip()]
        self.file_types_to_exclude = [ext.strip() for ext in self.exclude_entry.text().split(',') if ext.strip()]

        # Ensure the source and target directories exist.
        if not os.path.exists(self.source_directory) or not os.path.exists(self.target_directory):
            if not os.path.exists(self.source_directory):
                QtWidgets.QMessageBox.critical(self, "Error", ERROR_MESSAGES["source_not_exist"])
                print('ERROR: Source directory does not exist.')
            if not os.path.exists(self.target_directory):
                QtWidgets.QMessageBox.critical(self, "Error", ERROR_MESSAGES["target_not_exist"])
                print('ERROR: Target directory does not exist.')
            return False
        return True
    
    def start_sorting(self):
        if not self.validate():
            return

        log_message("**************************************************\n", level="decorating", log_file=self.log_file)
        log_message(f"New Log Entry - {datetime.now()}\n", level="decorating", log_file=self.log_file)
        log_message("**************************************************\n", level="decorating", log_file=self.log_file)

        log_message("Settings:\n", level="decorating", log_file=self.log_file)
        log_message(f"  - Source Directory: {self.source_directory}\n", level="decorating", log_file=self.log_file)
        log_message(f"  - Target Directory: {self.target_directory}\n", level="decorating", log_file=self.log_file)
        log_message(f"  - Backup: {'Enabled' if self.backup_wanted else 'Disabled'}\n", level="decorating", log_file=self.log_file)
        log_message(f"  - File Types To Include: {', '.join(self.file_types_to_include) if self.file_types_to_include else 'All'}\n", level="decorating", log_file=self.log_file)
        log_message(f"  - File Types To Exclude: {', '.join(self.file_types_to_exclude) if self.file_types_to_exclude else 'None'}\n", level="decorating", log_file=self.log_file)

        log_message("--------------------------------------------------\n", level="decorating", log_file=self.log_file)

        grouped_files = sort_files_by_date(self.source_directory, self.log_file)
        move_files(grouped_files, self.source_directory, self.target_directory, self.backup_wanted, self.backup_directory, self.file_types_to_include, self.file_types_to_exclude, self.log_file)

        log_message("\n==================================================\n", level="decorating", log_file=self.log_file)

# Handles logging and printing messages.
def log_message(message, level="info", log_file="log.txt", backup_wanted=False):
    levels = {
        "info": "",
        "moving": "MOVING: ",
        "warning": "WARNING: ",
        "error": "ERROR: ",
        "decorating": ""
    }
    prefix = levels.get(level, "")
    base_message = f"{prefix}{message}"
    
    if level == "info":
        final_message = f"{datetime.now()}: {base_message}\n"
    elif level == "moving":
        final_message = f"{datetime.now()}:  --> {base_message} {'Backup created.' if backup_wanted else ''}\n"
    elif level == "warning":
        final_message = f"{datetime.now()}:  --> {base_message} Skipping move. {'Backup not created.' if backup_wanted else ''}\n"
    elif level == "error":
        final_message = f"{datetime.now()}: {base_message} Exiting.\n"
    elif level == "decorating":
        final_message = base_message

    with open(log_file, "a") as log:
        log.write(final_message)

# Gets the sort method for each file either based on the file name of YYYYMMDD (first 8 digits), otherwise if not named like that, based on creation date.
def get_sort_key(file, source_directory):
    file_path = os.path.join(source_directory, file) 

    # Sorts by file name
    if len(file) >= 8 and file[:8].isdigit():
        return datetime.strptime(file[:8], "%Y%m%d")
    
    # Sorts by creation date
    else:
        return datetime.fromtimestamp(os.path.getmtime(file_path))

# Sorts and orders files and stores it in a dictionary. If the file is a directory or the log file, it will skip it.
def sort_files_by_date(source_directory, log_file):
    files = os.listdir(source_directory)
    sorted_files = sorted(files, key=lambda file: get_sort_key(file, source_directory))
    grouped_files = {}

    for file in sorted_files:
        file_path = os.path.join(source_directory, file)
        
        # Skip directories and the log file.
        if os.path.isdir(file_path) or file_path == log_file: #or file_path == os.path.join(source_directory, "log.txt"): <-- This is to also skip a log file if in the source directory.
            continue

        date_key = get_sort_key(file, source_directory).date().strftime("%Y_%m_%d")
        grouped_files.setdefault(date_key, []).append(file) # Groups files by the same date key together, creates a new key under the date key if it doesn't exist.
    return grouped_files

# Moves files to their respective date folders and creates a backup of the files before moving them.
def move_files(grouped_files, source_directory, target_directory, backup_wanted, backup_directory, file_types_to_include, file_types_to_exclude, log_file):
    total_files_found = sum(len(files) for files in grouped_files.values())
    total_files_moved = 0

    log_message(f"TOTAL FILES FOUND: {total_files_found}\n", level="decorating", log_file=log_file)

    # EXIT 1 - Check for conflicts between whitelist and blacklist
    if set(file_types_to_include) & set(file_types_to_exclude):
        log_message("Conflict detected between whitelist and blacklist.", level="error", log_file=log_file)
        log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating", log_file=log_file)
        print("ERROR: Conflict detected between whitelist and blacklist.")
        return total_files_found, total_files_moved

    # EXIT 2 - Checks if there are no files to move.
    if not total_files_found:
        log_message("No files to move.", level="error", log_file=log_file)
        log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating", log_file=log_file)
        print("ERROR: No files to move.")
        return total_files_found, total_files_moved

    # Creates a backup directory if backup is wanted.
    if backup_wanted:
        os.makedirs(backup_directory, exist_ok=True)

    for date, files in grouped_files.items():
        # Creates a directory for each date.     
        date_directory = os.path.join(target_directory, date)
        if not os.path.exists(date_directory):
            os.makedirs(date_directory, exist_ok=True)
            log_message(f"New directory created: {date}", log_file=log_file)
        else:
            log_message(f"Using existing directory: {date}", log_file=log_file)

        for file in files:
            source_path = os.path.join(source_directory, file)
            destination_path = os.path.join(date_directory, file)

            # FILE SKIP 1 - Checks and handles if the file already exists in the destination directory.
            if os.path.exists(destination_path):
                log_message(f"File '{file}' already exists in '{date_directory.replace(os.sep, '/')}'.", level="warning", log_file=log_file)
                continue
            
            # FILE SKIP 2 - Check file extension against whitelist and blacklist.
            file_extension = os.path.splitext(file)[1].lower()
            if file_types_to_include and file_extension not in file_types_to_include:
                log_message(f"File '{file}' excluded ({file_extension} not in include list).", level="warning", log_file=log_file)
                continue
            if file_extension in file_types_to_exclude:
                log_message(f"File '{file}' excluded ({file_extension} in exclude list).", level="warning", log_file=log_file)
                continue

            # Backups the file if backup is wanted and overwrites the previous backup file if it already exists.
            if backup_wanted:
                shutil.copy2(source_path, os.path.join(backup_directory, file))

            # Moves the file to the date directory.
            log_message(f"File '{file}' to '{date_directory.replace(os.sep, '/')}'.", level="moving", log_file=log_file)
            shutil.move(source_path, destination_path)
            total_files_moved += 1

    log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating", log_file=log_file)
    print("Completed.")
    print(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}")
    return total_files_found, total_files_moved

# Main function
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = FileSorterApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()