import os
from collections import defaultdict

def group_md_files(directory):
    # 创建一个字典来存储分组后的数据
    grouped_files = defaultdict(list)

    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            # 检查文件名中是否包含“（数字）”的模式
            parts = filename.split('（')
            if len(parts) > 1 and parts[0].count('｜') > 0:
                # 提取一级标题（括号前的内容）
                primary_title = parts[0].split("｜")[-1]
                # 构造完整的二级标题
                secondary_title = filename
                # 将二级标题添加到一级标题的列表中
                grouped_files[primary_title].append(secondary_title)
            else:
                # 文件名中不包含“（数字）”，整个文件名作为一级标题
                grouped_files[filename].append(filename)

    # 打印分组后的结果
    for primary_title, secondary_titles in grouped_files.items():
        if len(secondary_titles) > 1:
            print(f"# {primary_title}")
            for secondary_title in secondary_titles:
                print(f"## {secondary_title}")
        else:
            print(f"## {secondary_titles[0]}")


if __name__ == '__main__':
    # D:\WorkSpace\Idea\S\python\251\toc\dest
    group_md_files("D:\\WorkSpace\\Idea\\S\\python\\251\\toc\\dest")
