from jinja2 import Environment, FileSystemLoader
import os
from bs4 import BeautifulSoup


def _render_file(template_name: str, context: dict) -> str:
    """
    生成 html 文件
    """
    # 设置模板文件夹
    file_loader = FileSystemLoader('D:\\WorkSpace\\Idea\\S\\python\\study\\study-python\\templates')
    env = Environment(loader=file_loader)

    # 加载模板
    template = env.get_template(template_name)

    # 渲染模板
    rendered_html = template.render(context)
    return rendered_html


def handler_html(directory, dest):
    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            # 构建文件的完整路径
            md_file_path = os.path.join(directory, filename)
            # 读取 Markdown 文件内容
            with open(md_file_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()

            # 将 Markdown 转换为 HTML
            soup = BeautifulSoup(md_content, "html.parser")
            html_content = soup.find('div', attrs={'class': 'widget-richtext'})

            # 构建 HTML 文件的完整路径
            html_filename = os.path.splitext(filename)[0] + '.html'

            html_new_content = _render_file(
                'article.html',
                {'title': os.path.splitext(filename)[0] , 'content': html_content}
            )

            html_file_path = os.path.join(dest, html_filename)

            # 写入 HTML 文件
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(html_new_content)

            #print(f'Converted "{filename}" to "{html_filename}"')
            print(f'## {html_filename.split('.')[0]}')


if __name__ == '__main__':
    # 使用示例
    # 指定要遍历的文件夹路径 D:\WorkSpace\Idea\S\python\251\toc\org
    directory_path = 'D:\\Download\\BaiduNetdiskDownload\\2022-2024\\2024'
    dest_path = 'D:\\Download\\BaiduNetdiskDownload\\2022-2024\\dest' # 替换为实际的文件夹路径
    # 调用函数
    handler_html(directory_path, dest_path)