<p align="center">
   <img width="600" alt="image" src="https://github.com/user-attachments/assets/bca85f09-f24d-4657-92fd-23e8d755b051"/>
</p>

# File Sorter By Date (FSBD) - GUI VERSION
File Sorter By Date is a tool to automate organizing files into folders by date. FSBD first sorts files by the naming format YYYYMMDD, standard of smartphone camera file naming, otherwise by creation date if the file name does not follow that format. The tool enables the user to specify the source and target directories, whether to backup files, and the file types to include and exclude through a GUI. Extensive logging and error handling is implemented.

## About This Project
This file sorter works by inputting the source and target directories, whether to backup files, and the file types to include and exclude in the GUI and running to result in a sorted file structure in the target directory. I created this tool after recognizing the extensive time I spent manually sorting files into folders by date after downloading them off my phone. This version is a GUI version, created based on my previous code that ran in the terminal with a config.json file (see other project).

## Technologies Used
- Python 3.13
- PyQt5

## Installation
To install the File Sorter By Date, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/jusL98/file-sorter-by-date.git
   cd file-sorter-by-date
   ```

2. Ensure that you have python running on your system.

3. Create and activate a virtual environment:
   - On Windows:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

   - On macOS and Linux:
   
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install PyQt5 
   ```

4. Run the program.
   ```bash
   python main.py
   ```

6. **Alternatively, download and run the filesorter.exe file.**

7. Navigate to the target directory and view the sorted files in date folders formatted by YYYY_MM_DD.
## Usage
1. Run the program or run the .exe file.
2. Configure the settings in the GUI.
3. Navigate to the target directory and view the sorted files in date folders formatted by YYYY_MM_DD.
4. Actions are logged in the log.txt file in the target directory.
5. If backup is enabled, the files (in the unsorted form) were also copied to the backup directory within the target directory.

---

Thank you!

<p align="center">
   <img width="1000" alt="image" src="https://github.com/user-attachments/assets/a766d4cc-24a8-4730-984e-54609e4e5973"/>
</p>
