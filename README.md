<a id="readme-top"></a>

# File Sorter - GUI Version

This is a tool to automate organizing files into folders by date. The program first sorts files by the naming format YYYYMMDD, standard of smartphone camera file naming, otherwise by creation date if the file name does not follow that format. The tool enables the user to specify the source and target directories, whether to backup files, and the file types to include and exclude in the GUI. Extensive logging and error handling is implemented.

This project is based on my [previous file sorter](https://github.com/jusL98/file-sorter), improved from a terminal UI to a proper desktop GUI.

<p align="left">
   <img width="600" alt="image" src="https://github.com/user-attachments/assets/bca85f09-f24d-4657-92fd-23e8d755b051"/>
</p>

<p align="left">
   <img width="600" alt="image" src="https://github.com/user-attachments/assets/a766d4cc-24a8-4730-984e-54609e4e5973"/>
</p>

<p align="left">
   <img width="600" alt="image" src="https://github.com/user-attachments/assets/1bf0f0f6-f66b-4bd1-9f1c-d392aa2adaaa"/>
</p>

## Description

File Sorter involves the user configuring the following settings in the GUI:
- the source directory
- the target directories
- whether to backup files
- file types to include
- file types to exclude file

Then, the program can be run to result in a sorted file structure in the target directory, formatted YYYY_MM_DD. A log file will be created to track the file movements and any errors/skips. If backup is enabled, all unsorted files are copied to a backup folder within the target directory.

## Built With

- [Python 3.13](https://www.python.org/): Programming language for complete functionality
- [PyQt5](https://pypi.org/project/PyQt5/): Library for creating the GUI


## Quick Start

### Prerequisites

- OS
- Python 3.13 or higher
- Terminal or CLI Access

### Installation

To install File Sorter, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/jusL98/file-sorter-gui.git
   cd file-sorter-gui
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

### Setup

N/A

### Run

5. Run File Sorter:
   ```bash
   python main.py
   ```
6. Alternatively, download and run the `filesorter.exe` file.

## Usage

1. Configure the settings in the GUI.
2. Run the program.
3. Navigate to the target directory and view the sorted files in date folders formatted by YYYY_MM_DD.
4. Actions are logged in the log.txt file in the target directory.
5. If backup is enabled, the files (unsorted) were also copied to the backup directory within the target directory.

## Contributing

1. Fork & branch off main.
2. Make your changes.
3. PRs welcome!

## Project Structure

```
├── file-sorter-gui/
│   ├── main.py                        # contains the main program code and logic
│   └── filesorter.exe                 # .exe file for compiled version of File Sorter
```

## Acknowledgements
This project was created for myself after recognizing the extensive time I spent manually sorting files into folders by date after downloading them from my phone.

## License
This project is licensed under the [MIT](LICENSE.txt) License. See LICENSE.txt for more information.

<br>

---

Thank you!

<p align="left">
  <a href="mailto:justin.matthew.lee.18@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"/>
  </a>
  <a href="https://www.linkedin.com/in/justin-matthew-lee/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
  </a>
    <a href="https://github.com/jusl98">
    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/>
  </a>
</p>

<p align="right">(<a href="#readme-top">BACK TO TOP</a>)</p>
