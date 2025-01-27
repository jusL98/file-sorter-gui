"""
This program will take a source directory and sort files within the directory by their creation date.
New date directories are created if they do not already exist.
Files are moved to their respective date directories.

Settings can be modified including:
- Source directory
- Target directory
- Backup: Enabled or Disabled
- File types to include
- File types to exclude
"""

# Imports
import os
from datetime import datetime
import shutil
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class FileSorterApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Sorter by Date')
        self.setGeometry(100, 100, 600, 400)

        layout = QtWidgets.QVBoxLayout()

        self.source_dir_label = QtWidgets.QLabel('Source Directory:')
        self.source_dir_input = QtWidgets.QLineEdit()
        self.source_dir_button = QtWidgets.QPushButton('Browse')
        self.source_dir_button.clicked.connect(self.browse_source_directory)

        self.target_dir_label = QtWidgets.QLabel('Target Directory:')
        self.target_dir_input = QtWidgets.QLineEdit()
        self.target_dir_button = QtWidgets.QPushButton('Browse')
        self.target_dir_button.clicked.connect(self.browse_target_directory)

        self.backup_checkbox = QtWidgets.QCheckBox('Enable Backup')

        self.include_label = QtWidgets.QLabel('File Types to Include (comma separated):')
        self.include_input = QtWidgets.QLineEdit()

        self.exclude_label = QtWidgets.QLabel('File Types to Exclude (comma separated):')
        self.exclude_input = QtWidgets.QLineEdit()

        self.start_button = QtWidgets.QPushButton('Start Sorting')
        self.start_button.clicked.connect(self.start_sorting)

        layout.addWidget(self.source_dir_label)
        layout.addWidget(self.source_dir_input)
        layout.addWidget(self.source_dir_button)
        layout.addWidget(self.target_dir_label)
        layout.addWidget(self.target_dir_input)
        layout.addWidget(self.target_dir_button)
        layout.addWidget(self.backup_checkbox)
        layout.addWidget(self.include_label)
        layout.addWidget(self.include_input)
        layout.addWidget(self.exclude_label)
        layout.addWidget(self.exclude_input)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def browse_source_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if directory:
            self.source_dir_input.setText(directory)

    def browse_target_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Target Directory')
        if directory:
            self.target_dir_input.setText(directory)

    def log_message(self, message, level="info", log_file=None, backup_wanted=False):
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

        if log_file:
            with open(log_file, "a") as log:
                log.write(final_message)

    def get_sort_key(self, file, source_directory):
        file_path = os.path.join(source_directory, file) 
        if len(file) >= 8 and file[:8].isdigit():
            return datetime.strptime(file[:8], "%Y%m%d")
        else:
            return datetime.fromtimestamp(os.path.getmtime(file_path))

    def sort_files_by_date(self, source_directory, log_file):
        files = os.listdir(source_directory)
        sorted_files = sorted(files, key=lambda file: self.get_sort_key(file, source_directory))
        grouped_files = {}

        for file in sorted_files:
            file_path = os.path.join(source_directory, file)
            if os.path.isdir(file_path) or file_path == log_file:
                continue
            date_key = self.get_sort_key(file, source_directory).date().strftime("%Y_%m_%d")
            grouped_files.setdefault(date_key, []).append(file)
        return grouped_files

    def move_files(self, grouped_files, source_directory, target_directory, backup_wanted, file_types_to_include, file_types_to_exclude, log_file):
        total_files_found = sum(len(files) for files in grouped_files.values())
        total_files_moved = 0

        self.log_message(f"TOTAL FILES FOUND: {total_files_found}\n", level="decorating", log_file=log_file)

        if set(file_types_to_include) & set(file_types_to_exclude):
            self.log_message("Conflict detected between whitelist and blacklist.", level="error", log_file=log_file)
            self.log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating", log_file=log_file)
            QMessageBox.warning(self, 'Error', 'Conflict detected between whitelist and blacklist.')
            return total_files_found, total_files_moved

        if not total_files_found:
            self.log_message("No files to move.", level="error", log_file=log_file)
            self.log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating", log_file=log_file)
            QMessageBox.warning(self, 'Error', 'No files to move.')
            return total_files_found, total_files_moved

        backup_directory = os.path.join(target_directory, "_BACKUP_")
        if backup_wanted:
            os.makedirs(backup_directory, exist_ok=True)

        for date, files in grouped_files.items():
            date_directory = os.path.join(target_directory, date)
            if not os.path.exists(date_directory):
                os.makedirs(date_directory, exist_ok=True)
                self.log_message(f"New directory created: {date}", log_file=log_file)
            else:
                self.log_message(f"Using existing directory: {date}", log_file=log_file)

            for file in files:
                source_path = os.path.join(source_directory, file)
                destination_path = os.path.join(date_directory, file)

                if os.path.exists(destination_path):
                    self.log_message(f"File '{file}' already exists in '{date_directory.replace(os.sep, '/')}'.", level="warning", log_file=log_file)
                    continue
                
                file_extension = os.path.splitext(file)[1].lower()
                if file_types_to_include and file_extension not in file_types_to_include:
                    self.log_message(f"File '{file}' excluded ({file_extension} not in include list).", level="warning", log_file=log_file)
                    continue
                if file_extension in file_types_to_exclude:
                    self.log_message(f"File '{file}' excluded ({file_extension} in exclude list).", level="warning", log_file=log_file)
                    continue

                if backup_wanted:
                    shutil.copy2(source_path, os.path.join(backup_directory, file))

                self.log_message(f"File '{file}' to '{date_directory.replace(os.sep, '/')}'.", level="moving", log_file=log_file, backup_wanted=backup_wanted)
                shutil.move(source_path, destination_path)
                total_files_moved += 1

        self.log_message(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}\n", level="decorating", log_file=log_file)
        print("Completed.")
        print(f"TOTAL FILES MOVED: {total_files_moved} of {total_files_found}")
        return total_files_found, total_files_moved

    def start_sorting(self):
        source_directory = self.source_dir_input.text()
        target_directory = self.target_dir_input.text()
        backup_wanted = self.backup_checkbox.isChecked()
        file_types_to_include = self.include_input.text().split(',')
        file_types_to_exclude = self.exclude_input.text().split(',')

        if not source_directory or not target_directory:
            QMessageBox.warning(self, 'Error', 'Source and Target directories must be specified.')
            return

        file_types_to_include = [ft.strip() for ft in file_types_to_include if ft.strip()]
        file_types_to_exclude = [ft.strip() for ft in file_types_to_exclude if ft.strip()]

        log_file = os.path.join(target_directory, "log.txt")

        self.log_message("**************************************************\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)
        self.log_message(f"New Log Entry - {datetime.now()}\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)
        self.log_message("**************************************************\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)

        self.log_message("Settings:\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)
        self.log_message(f"  - Source Directory: {source_directory}\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)
        self.log_message(f"  - Target Directory: {target_directory}\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)
        self.log_message(f"  - Backup: {'Enabled' if backup_wanted else 'Disabled'}\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)
        self.log_message(f"  - File Types To Include: {', '.join(file_types_to_include) if file_types_to_include else 'All'}\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)
        self.log_message(f"  - File Types To Exclude: {', '.join(file_types_to_exclude) if file_types_to_exclude else 'None'}\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)

        self.log_message("--------------------------------------------------\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)

        self.log_message("\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)

        grouped_files = self.sort_files_by_date(source_directory, log_file)
        total_files_found, total_files_moved = self.move_files(grouped_files, source_directory, target_directory, backup_wanted, file_types_to_include, file_types_to_exclude, log_file)

        self.log_message("\n==================================================\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)
        self.log_message("\n\n\n\n", level="decorating", log_file=log_file, backup_wanted=backup_wanted)

        QMessageBox.information(self, 'Completed', f'Total Files Found: {total_files_found}\nTotal Files Moved: {total_files_moved}')

def main():
    app = QtWidgets.QApplication([])
    window = FileSorterApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()