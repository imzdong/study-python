import os
import re


def sanitize_filename(path, replacement=''):
    """
    遍历指定路径下的所有文件，并移除文件名中匹配正则表达式pattern的字符。

    参数:
    - path: 要遍历的文件夹路径。
    - pattern: 用于匹配文件名中要移除的字符的正则表达式。
    - replacement: 替换字符，默认为空字符串，即删除匹配的字符。
    """
    # 遍历文件夹
    for filename in os.listdir(path):
        # 检查是否为文件
        if os.path.isfile(os.path.join(path, filename)):
            # 替换文件名中的特殊字符
            sanitized_name = filename.replace(replacement, '')
            if sanitized_name != filename:
                # 构造原始文件的完整路径和新文件的完整路径
                old_file = os.path.join(path, filename)
                new_file = os.path.join(path, sanitized_name)
                # 重命名文件
                os.rename(old_file, new_file)
                print(f'Renamed "{filename}" to "{sanitized_name}"')
        else:
            sanitize_filename(os.path.join(path, filename), replacement)


if __name__ == '__main__':
    # 使用示例
    # 指定要遍历的文件夹路径 D:\WorkSpace\Idea\S\python\251\final\source\images
    directory_path = 'D:\\WorkSpace\\Idea\\S\\python\\251\\final\\source\\images'  # 替换为实际的文件夹路径
    # 定义要移除的特殊字符的正则表达式，例如：[<>:"/\\|?*] 表示Windows系统中不允许的字符
    special_chars_pattern = '[天下无鱼][shikey.com]'
    # 调用函数
    sanitize_filename(directory_path, special_chars_pattern)
