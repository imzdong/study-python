import requests
from urllib.parse import urlparse, parse_qs

url = 'https://mmbiz.qpic.cn/mmbiz_gif/93v3S81Awkn5lJTmtibMxJOZaNoraDaCzRVa42zpRjVf4t27LX3aiaGoWXu3W0bYgla6orKG9qHpXnObUGR5PK6g/640?wx_fmt=gif'


if __name__ == '__main__':
    # 发送 GET 请求
    response = requests.get(url)
    # 解析 URL
    parsed_url = urlparse(url)

    # 提取查询字符串
    query_params = parse_qs(parsed_url.query)

    # 获取 wx_fmt 参数
    wx_fmt = query_params.get('wx_fmt', [''])[0]

    print(f"wx_fmt: {wx_fmt}")
    # 检查请求是否成功
    if response.status_code == 200:
        # 从 URL 中获取文件名
        parsed_url = urlparse(url)
        filename = parsed_url.path.split('/')[-1]

        # 如果 Content-Disposition 中有文件名信息，优先使用它
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            import re
            match = re.search(r'filename=(.+)', content_disposition)
            if match:
                filename = match.group(1).strip('"\'')  # 去掉引号

        # 写入文件
        with open(filename, 'wb') as f:
            f.write(response.content)

        print(f"File saved as {filename}")
    else:
        print("Failed to download the file.")