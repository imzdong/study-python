import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import uuid
import shutil

def download_image(img_url, save_dir):
    """下载图片并返回本地路径"""
    try:
        # 从URL中提取文件名
        img_name = os.path.basename(img_url.split('?')[0])
        if not img_name:
            img_name = f"img_{hash(img_url)}.jpg"
        
        # 保存路径
        save_path = os.path.join(save_dir, img_name)
        
        # 如果图片已存在，直接返回路径
        if os.path.exists(save_path):
            return img_name
            
        # 下载图片
        response = requests.get(img_url, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return img_name
    except Exception as e:
        print(f"下载图片失败 {img_url}: {str(e)}")
    return None

def process_html_files(input_dir, output_dir):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 遍历输入目录中的所有HTML文件
    for file_name in os.listdir(input_dir):
        input_file = os.path.join(input_dir, file_name)
        
        # 处理 toc.md 文件
        if file_name == 'toc.md':
            output_file = os.path.join(output_dir, file_name)
            shutil.copy2(input_file, output_file)
            print(f"复制完成：{file_name}")
            continue
            
        # 处理 HTML 文件
        if not file_name.endswith('.html'):
            continue
            
        # 读取并解析HTML
        with open(input_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # 检查是否只有 body 标签
        body = soup.find('body')
        if body and len(body.find_all()) == 0:
            output_file = os.path.join(output_dir, file_name)
            shutil.copy2(input_file, output_file)
            print(f"复制完成：{file_name}")
            continue
        
        # 查找指定class的内容
        content = soup.find(class_='SlateRichContent_main_1Bj6H')
        if content:
             # 移除所有元素的 class 属性
            for tag in content.find_all(True):
                if tag.has_attr('class'):
                    del tag['class']
            
            # 处理图片
            for img in content.find_all('img'):
                src = img.get('data-savepage-src')
                if src:
                    # 下载图片到输出目录
                    local_img = download_image(src, output_dir)
                    if local_img:
                        # 创建新的img标签，只保留class和src属性
                        new_img = soup.new_tag('img')
                        new_img['src'] = local_img
                        img.replace_with(new_img)
            
            # 创建新的HTML文档
            new_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{file_name}</title>
</head>
<body>
{content.prettify()}
</body>
</html>"""
            
            # 保存新文件
            output_file = os.path.join(output_dir, file_name)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            print(f"处理完成：{file_name}")
        else:
            print(f"未找到指定内容：{file_name}")

if __name__ == "__main__":
    input_dir = "/Users/admin/Downloads/mobile-book/6"
    output_dir = "/Users/admin/Downloads/mobile-book/6-out"
    process_html_files(input_dir, output_dir)