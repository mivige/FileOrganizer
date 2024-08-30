# File Organizer

![Version](https://img.shields.io/badge/Version-0.1.0-brightgreen)
![Language](https://img.shields.io/badge/Language-python-blue)
![License](https://img.shields.io/badge/License-GPL_3.0-red)
---
File Organizer is a Python-based GUI application that helps you organize files in a specified directory based on different criteria such as file type, date, or file size.

## Features

- Organize files by:
  - File type
  - Date (last modified)
  - File size
- Auto-name folders or specify custom folder names
- Set minimum number of items per folder
- User-friendly GUI interface

## Requirements

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library modules)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/mivige/FileOrganizer.git
   ```
2. Navigate to the project directory:
   ```
   cd FileOrganizer
   ```

## Usage

1. Run the application:
   ```
   python gui.py
   ```
2. The File Organizer GUI will appear.

3. Select the target folder you want to organize by clicking the "Browse" button.

4. Choose an organization method:
   - Filetype: Organizes files based on their type (e.g., images, documents, audio)
   - Date: Organizes files based on their last modified date
   - Filesize: Organizes files into categories based on their size (Large: >100 MB, Medium: 10-100 MB, Small: <10 MB)

5. (Optional) Check the "Auto-name folders" box to automatically generate folder names based on the selected organization method. If unchecked, you can specify custom folder names.

6. If using auto-naming, set the minimum number of items per folder. Files that would go into folders with fewer than this number will be placed in an "Other" folder.

7. If not using auto-naming, specify the number of sub-folders and their names.

8. Click the "Organize Files" button to start the organization process.

9. A success message will appear when the organization is complete.

## File Structure

- `gui.py`: Contains the GUI implementation using tkinter
- `folder_operator.py`: Contains the logic for file organization

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/mivige/FileOrganizer/issues) if you want to contribute.
