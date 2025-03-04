import os
import re
from bs4 import BeautifulSoup

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



def process_html_meta(directory):
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            
            # 读取HTML文件
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # 替换meta标签
            pattern = r'<meta\s+charset="utf-8">'
            replacement = '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>'
            new_content = re.sub(pattern, replacement, content, count=1)
            
            # 写回文件
            if new_content != content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
                print(f"已更新meta标签: {filename}")

if __name__ == "__main__":
    input_dir = "D:\\BaiduNetdiskDownload\\mobile-book\\郭东白的架构课-final"
    process_html_meta(input_dir)
    #process_directory(input_dir)
    #process_toc_file(input_dir)
