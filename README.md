<p align="center">
   <img width="600" alt="image" src="https://github.com/user-attachments/assets/bca85f09-f24d-4657-92fd-23e8d755b051"/>
</p>\

# File Sorter By Date (FSBD) - GUI VERSION
File Sorter By Date is a tool to automate organizing files into folders by date. FSBD first sorts files by the naming format YYYYMMDD, standard of smartphone camera file naming, otherwise by creation date if the file name does not follow that format. The tool enables the user to specify the source and target directories, whether to backup files, and the file types to include and exclude in the config.json file. Extensive logging and error handling is implemented.

## About This Project
This file sorter works by inputting the source and target directories, whether to backup files, and the file types to include and exclude in the config.json file and running the program to result in a sorted file structure in the target directory. I created this tool after recognizing the extensive time I spent manually sorting files into folders by date after downloading them off my phone.

## Technologies Used
- Python 3.13

## Installation
To install the File Sorter By Date, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/jusL98/file-sorter-by-date.git
   cd file-sorter-by-date
   ```

2. Ensure that you have python running on your system.

3. Ensure that you have a text or code editor like notepad installed on your system to edit the settings in the config.json file.

4. Find the file path of the cloned repository and navigate to it.
   ```bash
   DIR
   ```

5. Open the config.json file and edit the settings to your desired specifications.
<br> - source_directory: Enter the path to the folder containing the files to be sorted.
<br> - target_directory: Enter the path to the folder where the sorted files will be placed.
<br> - backup_wanted: Enter 'true' or 'false' to enable or disable file backups.
<br> - file_types_to_include: Enter an array of file types to include in the sorting process. A blank array will include all file types not excluded below.
<br> - file_types_to_exclude: Enter an array of file types to exclude from the sorting process.
   ```bash
   {
    "source_directory": "C:/Users/justi/Downloads/source_dir_test",
    "target_directory": "C:/Users/justi/Downloads/source_dir_test/target_dir_test",
    "backup_wanted": true,
    "file_types_to_include": [],
    "file_types_to_exclude": [".mp4"]
   }
   ```

6. Once settings are configured, run the program.
   ```bash
   python main.py
   ```

7. Navigate to the target directory and view the sorted files in date folders formatted by YYYY_MM_DD.
## Usage
1. Configure the settings in the config.json file.
2. Run the program.
3. Navigate to the target directory and view the sorted files in date folders formatted by YYYY_MM_DD.
4. Actions are logged in the log.txt file in the target directory.
5. If backup is enabled, the files (in the unsorted form) were also copied to the backup directory within the target directory.

---

Thank you!

<p align="center">
   <img width="1000" alt="image" src="https://github.com/user-attachments/assets/a766d4cc-24a8-4730-984e-54609e4e5973"/>
</p>
