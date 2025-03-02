import os
import shutil

def move_files_to_target(source_dir, target_dir):
    """
    Recursively find all HTML files and toc.md in source_dir and move them to target_dir
    """
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    # Walk through source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # Check if file is HTML or toc.md
            if file.endswith('.html') or file == 'toc.md':
                source_path = os.path.join(root, file)
                target_path = os.path.join(target_dir, file)
                
                # Handle duplicate filenames
                counter = 1
                base_name = os.path.splitext(file)[0]
                extension = os.path.splitext(file)[1]
                while os.path.exists(target_path):
                    new_name = f"{base_name}_{counter}{extension}"
                    target_path = os.path.join(target_dir, new_name)
                    counter += 1
                
                # Move the file
                shutil.move(source_path, target_path)

if __name__ == "__main__":
    source_directory = "path/to/source/directory"  # Replace with source directory path
    target_directory = "path/to/target/directory"  # Replace with target directory path
    move_files_to_target(source_directory, target_directory)
