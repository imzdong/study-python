import os

def read_toc_and_generate_index(toc_path, output_path, book_title="郭东白的架构课", author="郭东白"):
    """读取目录文件并生成主HTML"""
    
    # 读取toc.md文件
    with open(toc_path, 'r', encoding='utf-8') as f:
        toc_content = f.readlines()
    
    # 生成HTML内容
    html_content = []
    html_content.append('<!DOCTYPE html>')
    html_content.append('<html lang="zh-CN">')
    html_content.append('<head>')
    html_content.append('    <meta charset="UTF-8">')
    html_content.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html_content.append(f'    <title>{book_title}</title>')
    html_content.append('</head>')
    html_content.append('<body>')
    
    # 添加封面
    html_content.append('    <!-- 封面 -->')
    html_content.append('    <div class="cover">')
    html_content.append(f'        <h1>{book_title}</h1>')
    html_content.append(f'        <p>{author}</p>')
    html_content.append('    </div>')
    
    # 添加目录
    html_content.append('    <!-- 目录 -->')
    html_content.append('    <nav epub:type="toc" id="table-of-contents">')
    html_content.append('        <h2>目录</h2>')
    html_content.append('        <ol>')
    
    # 处理目录内容
    current_section = None
    for line in toc_content:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('# '):
            # 一级标题，创建新的章节
            if current_section:
                html_content.append('            </ol>')
                html_content.append('        </li>')
            title = line[2:]
            current_section = title
            html_content.append(f'        <li>')
            html_content.append(f'            <a href="{title}.html">{title}</a>')
            html_content.append('            <ol>')
        elif line.startswith('## '):
            # 二级标题
            title = line[3:]
            html_content.append(f'                <li><a href="{title}.html">{title}</a></li>')
    
    # 关闭最后一个章节
    if current_section:
        html_content.append('            </ol>')
        html_content.append('        </li>')
    
    # 关闭目录
    html_content.append('        </ol>')
    html_content.append('    </nav>')
    html_content.append('</body>')
    html_content.append('</html>')
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_content))

if __name__ == '__main__':
    toc_path = "/Users/admin/Downloads/mobile-book/6/toc.md"
    output_path = "/Users/admin/Downloads/mobile-book/6/index.html"
    read_toc_and_generate_index(toc_path, output_path)