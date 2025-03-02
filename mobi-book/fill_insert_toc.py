import os

def generate_toc(root_dir):
    """
    Generate a table of contents markdown file by recursively scanning HTML files
    """
    # Get the base folder name for the first line
    base_name = os.path.basename(root_dir)
    
    # Initialize toc content with folder name as first line
    toc_content = [base_name + "\n\n"]
    
    # Walk through directory
    for root, dirs, files in os.walk(root_dir):
        # Get relative path from root directory
        # Get relative path and sort files by modification time
        rel_path = os.path.relpath(root, root_dir)
        # Sort directories by name
        dirs.sort()
        # Sort files by name directly
        files.sort() # Extract filenames and sort alphabetically
        
        # Skip the root directory itself
        if rel_path == '.':
            continue
            
        # First level directories become h1 headers
        if os.path.dirname(rel_path) == '':
            toc_content.append(f"# {os.path.basename(rel_path)}\n")
            
            # Create empty HTML file in first level directory
            folder_name = os.path.basename(rel_path)
            empty_html = os.path.join(root_dir, f"{folder_name}.html")
            if not os.path.exists(empty_html):
                with open(empty_html, 'w', encoding='utf-8') as f:
                    f.write("<body></body>")
        
        # Add HTML files as h2 headers
        for file in files:
            if file.endswith('.html'):
                # Skip the empty HTML files we created
                if file == f"{os.path.basename(root)}.html":
                    continue
                    
                # Add as h2 header
                file_name = os.path.splitext(file)[0]
                toc_content.append(f"## {file_name}\n")
    
    # Write toc.md file
    toc_path = os.path.join(root_dir, 'toc.md')
    with open(toc_path, 'w', encoding='utf-8') as f:
        f.writelines(toc_content)

if __name__ == '__main__':
    # Replace with your target directory
    target_dir = '/Users/admin/Downloads/mobile-book/212-100099801-专栏课-郭东白-郭东白的架构课'
    generate_toc(target_dir)
