import os
import tarfile
import shutil
import subprocess
from pathlib import Path


def analyze_mbz(mbz_file_path):
    """
    Analyze an MBZ file and return information about its structure
    
    Args:
        mbz_file_path (str): Path to the MBZ file
        
    Returns:
        dict: Dictionary with information about the MBZ file
    """
    info = {
        "file_size": os.path.getsize(mbz_file_path),
        "file_name": os.path.basename(mbz_file_path),
        "is_valid": False,
        "contents": [],
        "top_level_items": 0,
        "xml_files": 0
    }
    
    try:
        with tarfile.open(mbz_file_path, "r:gz") as tar:
            members = tar.getmembers()
            info["is_valid"] = True
            info["contents"] = [m.name for m in members[:20]]  # List first 20 items
            
            # Count top-level items and XML files
            top_level = set()
            xml_count = 0
            
            for member in members:
                if '/' not in member.name:
                    top_level.add(member.name)
                elif member.name.endswith('.xml'):
                    xml_count += 1
            
            info["top_level_items"] = len(top_level)
            info["xml_files"] = xml_count
            info["total_files"] = len(members)
            
    except Exception as e:
        info["error"] = str(e)
        
    return info


def extract_mbz(mbz_file_path, output_dir, open_after=False):
    """
    Extract an MBZ file to a directory
    
    Args:
        mbz_file_path (str): Path to the MBZ file
        output_dir (str): Path to the output directory
        open_after (bool): Whether to open the folder after extraction
        
    Returns:
        str: Path to the extracted directory or error message
    """
    try:
        # Create a folder with the same name as the mbz file (without extension)
        base_name = os.path.basename(mbz_file_path)
        file_name_without_ext = os.path.splitext(base_name)[0]
        extract_dir = os.path.join(output_dir, file_name_without_ext)
        
        # Create the directory if it doesn't exist
        os.makedirs(extract_dir, exist_ok=True)
        
        # Extract using tarfile module
        with tarfile.open(mbz_file_path, "r:gz") as tar:
            tar.extractall(path=extract_dir)
        
        # Open the folder if requested
        if open_after:
            try:
                # Cross-platform way to open a folder
                if os.name == 'nt':  # Windows
                    os.startfile(extract_dir)
                elif os.name == 'posix':  # macOS, Linux
                    if os.uname().sysname == 'Darwin':  # macOS
                        subprocess.call(['open', extract_dir])
                    else:  # Linux
                        subprocess.call(['xdg-open', extract_dir])
            except Exception:
                # If opening the folder fails, just continue (non-critical)
                pass
            
        return extract_dir
    
    except Exception as e:
        return f"Error: {str(e)}"


def create_mbz(source_dir, output_file):
    """
    Create an MBZ file from a directory
    
    Args:
        source_dir (str): Path to the source directory
        output_file (str): Path to the output MBZ file
        
    Returns:
        bool: True if successful, False otherwise
        str: Error message if unsuccessful
    """
    try:
        # Normalize paths to absolute paths
        source_dir = os.path.abspath(source_dir)
        output_file = os.path.abspath(output_file)
        
        # Create tar.gz file with proper structure for Moodle
        with tarfile.open(output_file, "w:gz") as tar:
            # Store the current directory
            original_dir = os.getcwd()
            
            try:
                # Change to the parent directory of the source directory
                parent_dir = os.path.dirname(source_dir)
                os.chdir(parent_dir)
                
                # Get the base directory name (without path)
                base_dir = os.path.basename(source_dir)
                
                # Add all files from the folder, maintaining paths relative to the parent directory
                for root, dirs, files in os.walk(base_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # This ensures the paths in the archive are relative to the parent
                        # directory and maintain the exact same structure as the original
                        tar.add(file_path)
            finally:
                # Always return to the original directory
                os.chdir(original_dir)
        
        return True, "Success"
    
    except Exception as e:
        return False, f"Error: {str(e)}"


def list_xml_files(extracted_dir):
    """
    List all XML files in the extracted directory
    
    Args:
        extracted_dir (str): Path to the extracted directory
        
    Returns:
        list: List of XML files
    """
    xml_files = []
    
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))
                
    return xml_files 