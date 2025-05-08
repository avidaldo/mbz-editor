# MBZ Editor

A simple Tkinter GUI application for working with Moodle backup files (.mbz format).

## Features

- Decompress MBZ files (which are tar.gz archives) to a folder
- Compress a folder back into an MBZ file in the proper format for Moodle import
- Analyze MBZ files to check their structure
- Simple, user-friendly interface

## Requirements

- Python 3.6 or higher
- Standard Python libraries (no additional installations required):
  - tkinter (usually comes with Python)
  - os
  - tarfile
  - gzip
  - shutil

## Usage

1. Run the program:
   ```
   python mbz_editor.py
   ```

2. To decompress an MBZ file:
   - Click the "Decompress" tab
   - Select the .mbz file
   - Choose an output directory
   - Optionally check/uncheck "Open folder after extraction"
   - Click "Decompress MBZ File"
   - The contents will be extracted to a folder with the same name as the .mbz file

3. To compress a folder to MBZ:
   - Click the "Compress" tab
   - Select the folder containing the extracted MBZ contents
   - Choose where to save the new .mbz file
   - Click "Compress to MBZ File"
   - The folder will be compressed in the correct format for Moodle import

4. To analyze an MBZ file:
   - Click the "Analyze" tab
   - Select the .mbz file
   - Click "Analyze MBZ File"
   - Review the file structure and contents

## Important Notes

- MBZ files are tar.gz archives with a specific structure required by Moodle
- After decompressing, you can manually edit the XML files before compressing again
- When compressing, the folder structure must remain exactly as it was when extracted
- The compression method preserves the paths exactly as needed for Moodle import
- Do not add, rename, or move files/folders within the extracted structure unless you know what you're doing

## Troubleshooting

If you encounter import issues with your compressed MBZ file:

1. Make sure you haven't changed the folder structure after extraction
2. Ensure all XML files are valid if you've made manual edits
3. Check that you have permission to read/write to the selected directories
4. If the issue persists, try using the original Moodle backup functionality instead

## How It Works

The application uses Python's tarfile module to extract and create tar.gz archives. The key to successful MBZ file handling is maintaining the exact file paths and structure that Moodle expects. The compression function preserves these paths by temporarily changing to the parent directory of the source folder before adding files to the archive. 