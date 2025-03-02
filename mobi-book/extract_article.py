import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

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

def process_html(input_file):
    # 创建输出目录
    output_dir = os.path.dirname(input_file)
    img_dir = os.path.join(output_dir, 'images')
    os.makedirs(img_dir, exist_ok=True)
    
    # 读取HTML文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # 提取标题
    title = soup.title.string if soup.title else "无标题"
    
    # 找到主要内容区域（这里需要根据实际HTML结构调整）
    article = soup.find('article') or soup.find('div', class_='article-content')
    if not article:
        # 如果找不到特定标签，尝试查找主要内容区域
        article = soup.find('div', class_=re.compile(r'content|article|main'))
    
    if article:
        # 处理图片
        for img in article.find_all('img'):
            src = img.get('src')
            if src:
                # 下载图片
                local_img = download_image(src, img_dir)
                if local_img:
                    img['src'] = f'images/{local_img}'
        
        # 创建新的HTML文档
        new_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
</head>
<body>
{article.prettify()}
</body>
</html>"""
        
        # 保存新文件
        output_file = os.path.join(output_dir, 'article666.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print(f"处理完成！新文件保存在: {output_file}")
        print(f"图片保存在: {img_dir}")
    else:
        print("未找到文章内容")

if __name__ == "__main__":
    input_file = "/Users/admin/trae-work-splace/study-python/mobi-book/01丨模块导学：是什么在影响架构活动的成败？.html"
    process_html(input_file)