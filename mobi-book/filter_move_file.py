import os
import shutil

def copy_html_files(src_dir, dest_dir):
    """
    Copy HTML files from source directory to destination directory while preserving directory structure
    
    Args:
        src_dir: Source directory path
        dest_dir: Destination directory path
    """
    # Walk through source directory
    for root, dirs, files in os.walk(src_dir):
        # Filter HTML files
        html_files = [f for f in files if f.endswith('.html')]
        
        for html_file in html_files:
            # Get source file path
            src_file = os.path.join(root, html_file)
            
            # Create relative path from source directory
            rel_path = os.path.relpath(root, src_dir)
            
            # Create destination directory path
            dest_path = os.path.join(dest_dir, rel_path)
            
            # Create destination directories if they don't exist
            os.makedirs(dest_path, exist_ok=True)
            
            # Copy file to destination
            sanitized_name = html_file.replace('[天下无鱼][shikey.com]', '')
            dest_file = os.path.join(dest_path, sanitized_name)
            shutil.copy2(src_file, dest_file)
            print(f"Copied: {src_file} -> {dest_file}")

# Example usage
if __name__ == "__main__":
    source_directory = "/Users/admin/Downloads/212-100099801-专栏课-郭东白-郭东白的架构课（完结）"
    destination_directory = "/Users/admin/Downloads/mobile-book/212-100099801-专栏课-郭东白-郭东白的架构课"
    copy_html_files(source_directory, destination_directory)
