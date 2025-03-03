import os
import re

def clean_filename(filename):
    # Remove Chinese parentheses and special characters
    cleaned = re.sub(r'[（）\(\)\[\]\{\}\<\>\'\"\\\/:*?"<>|]', '', filename)
    return cleaned

def process_toc_file(directory):
    # Read toc.md from current directory
    toc_path = os.path.join(directory, 'toc.md')
    
    if not os.path.exists(toc_path):
        print("toc.md not found in current directory")
        return
        
    # Read and process each line
    with open(toc_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    # Clean filenames and create new content
    cleaned_lines = [clean_filename(line.strip()) for line in lines]
    
    # Write back to toc.md
    with open(toc_path, 'w', encoding='utf-8') as file:
        for line in cleaned_lines:
            file.write(line + '\n')
            
    print("Successfully processed toc.md")

def process_directory(directory):
    # Get all files in directory
    for filename in os.listdir(directory):
        old_path = os.path.join(directory, filename)
        if os.path.isfile(old_path):
            # Clean the filename
            new_filename = clean_filename(filename)
            new_path = os.path.join(directory, new_filename)
            
            # Rename file if name changed
            if new_filename != filename:
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_filename}")
                except OSError as e:
                    print(f"Error renaming {filename}: {e}")


if __name__ == "__main__":
    input_dir = "/Users/admin/Downloads/mobile-book/123out"
    #process_directory(input_dir)
    process_toc_file(input_dir)
