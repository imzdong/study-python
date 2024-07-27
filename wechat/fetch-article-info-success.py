import requests
import openpyxl
import config
import time
import random
from bs4 import BeautifulSoup
import re
import os
import datetime
from jinja2 import Environment, FileSystemLoader
from urllib.parse import urlparse, parse_qs

# 爬不同公众号只需要更改 fakeid 1857985110
rootPath = config.rootPath
wxlistfile = rootPath + 'wxlist.xlsx'
htmlPath = rootPath + '\\html'

# 解析url
def get_beautiful_soup(url1):
    res = requests.get(url1)
    res.encoding = 'utf-8'
    html = res.text
    return BeautifulSoup(html, "html.parser")

def get_content(curl):
    data = {}
    soup = get_beautiful_soup(curl)
    if soup.find('h1', attrs={'id': 'activity-name'}) == None:
        data['title'] = "Nonetipycal Type"
    else:
        # Get Document Title
        data['title'] = soup.find('h1', attrs={'id': 'activity-name'}).string.strip()
        # Get the publish date parameter
        dateframe = re.findall(r'var ct\s*=\s*.*\d{10}', str(soup))
        # split the parameter as a list
        date = re.split('"', dateframe[0])
        #format the publish date
        data['date'] = time.strftime("%Y-%m-%d",time.localtime(int(date[1])))
        data['time'] = time.strftime("%Y-%m-%d %H:%M",time.localtime(int(date[1])))
        # Get the content
        data['content'] = soup.find('div', attrs={'id': 'js_content'})
        #this makes a list of bs4 element tags img
        data['images'] = [img for img in soup.find('div', attrs={'id': 'js_content'}).find_all('img')]
    return data

imgRootPath = 'https://mp.weixin.qq.com'

def saveData(curl):
    data = get_content(curl)
    image_links = []
    if data.get('images') != None:
        imageNames = []
        if len(data['images']) != 0:
            # compile our unicode list of image links
            image_links = [each.get('data-src') for each in data['images']]
            # create img folder
            # imgFolder = validateTitle (data['time'].split(' ')[0])
            imgFolder = validateTitle(data['date'])
            imgDst = os.path.join(htmlPath, 'imgs', imgFolder).replace('\\', '/')
            if not os.path.exists(imgDst):
                os.makedirs(imgDst)  # make directory
            for index, each in enumerate(image_links):
                # convert abs address
                if not each.startswith("http"):
                    print(f"imgUrl不合法：{each}")
                    continue
                imagename = get_image_name(each, f"image_{index}")
                imageNames.append(imagename)
                # save images
                download_image(each, os.path.join(imgDst, imagename).replace('\\', '/'))
                # join a file name with title and data & replace ilegal tags.
        filename = validateTitle(data['title'] + '.html')
        # replace ilegal tags
        saveDst = os.path.join(htmlPath, filename).replace('\\', '/')

        cleanSoup = data['content']
        if len(image_links) != 0:
            for index, each in enumerate(image_links):
                imagename = imageNames[index]
                srcNew = "./imgs/" + imgFolder + "/" + imagename

                cleanSoup.find('img', {'data-src': each})['src'] = srcNew
                # cleanSoup = BeautifulSoup(str(originalSoup).replace(old, new))
                # cleanSoup = BeautifulSoup(str(cleanSoup).replace(each, srcNew),'html.parser')
        cleanSoup['style'] = 'visibility: initial'
        # Format the parsed html file
        htmlcontent = _render_file(
                'article.html',
                {'title': filename, 'content': cleanSoup.prettify()}
            )
        # print(htmlcontent)

        with open(saveDst, "wt", encoding=("utf-8")) as f:
            f.write(htmlcontent)

        savetolist(curl, data['title'], saveDst, data['date'])
    else:
        saveDst = "None"
        saveDate = time.strftime('%Y-%m-%d')
        savetolist(curl, data['title'], saveDst, saveDate)

def get_image_name(imageUrl, name):
    # 解析 URL
    parsed_url = urlparse(imageUrl)
    # 提取查询字符串
    query_params = parse_qs(parsed_url.query)
    # 获取 wx_fmt 参数
    wx_fmt = query_params.get('wx_fmt', [''])[0]
    return f"{name}.{wx_fmt}"

def getMonth(date_string):
    date_format = "%Y-%m-%d"

    # 将字符串转换为 datetime 对象
    date_object = datetime.strptime(date_string, date_format)

    # 提取年份和月份
    year = date_object.year
    month = date_object.month

    # 如果需要，可以将年份和月份重新格式化为字符串
    return f"{year}-{month:02d}"

def download_image(imageUrl, local_filename):
    # 发送GET请求
    print(f"Image downloaded to {imageUrl}")
    response = requests.get(imageUrl, stream=True)

    # 检查响应状态码是否为200（成功）
    if response.status_code == 200:
        # 打开文件，使用'wb'模式来写入二进制数据
        with open(local_filename, 'wb') as file:
            # 写入图片数据
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Image downloaded to {local_filename}")
    else:
        print("Failed to download the image.")

def _render_file(template_name: str, context: dict) -> str:
    """
    生成 html 文件
    """
    # 设置模板文件夹
    file_loader = FileSystemLoader(rootPath+'\\templates')
    env = Environment(loader=file_loader)

    # 加载模板
    template = env.get_template(template_name)

    # 渲染模板
    rendered_html = template.render(context)
    return rendered_html

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # replace to _
    return new_title


def savetolist(curl, ctitle, lcfile, date):
    lclist = rootPath + '/lclist.xlsx'
    wb = openpyxl.load_workbook(lclist)
    ws = wb.active
    row = [curl, ctitle, lcfile, date]
    ws.append(row)
    wb.save(lclist)

def doGet():
    wb = openpyxl.load_workbook(wxlistfile, True)
    # 获取活动工作表
    ws = wb.active
    # 遍历每一行
    for row in ws.iter_rows(values_only=True):
        print(row[1])
        saveData(row[1])
        time.sleep(random.randint(1, 5))

def savetolistTest():
    lclist = rootPath + '/lclist.xlsx'
    wb = openpyxl.load_workbook(lclist)
    ws = wb.active
    row = [92, 92, 92, 92]
    ws.append(row)
    wb.save(lclist)
    row = [93, 93, 93, 93]
    ws.append(row)
    wb.save(lclist)


'''
/html/body/div[2]/div[2]/div[2]/div/div[1]/div[2]/section[7]/span/img

<img class="rich_pages wxw-img __bg_gif" data-galleryid="" data-ratio="1.1966604823747682" 
data-src="https://mmbiz.qpic.cn/mmbiz_gif/93v3S81Awkn5lJTmtibMxJOZaNoraDaCzRVa42zpRjVf4t27LX3aiaGoWXu3W0bYgla6orKG9qHpXnObUGR5PK6g/640?wx_fmt=gif" 
data-type="gif" data-w="539" style="letter-spacing: 0.578px; height: auto !important; visibility: visible !important; width: 539px !important;" data-original-style="letter-spacing: 0.578px;height: auto !important;" data-index="1" 
src="https://mmbiz.qpic.cn/mmbiz_gif/93v3S81Awkn5lJTmtibMxJOZaNoraDaCzRVa42zpRjVf4t27LX3aiaGoWXu3W0bYgla6orKG9qHpXnObUGR5PK6g/640?wx_fmt=gif&amp;tp=webp&amp;wxfrom=5&amp;wx_lazy=1" _width="539px" data-order="0" alt="图片" data-fail="0">

'''

if __name__ == '__main__':
    wxlistfilefinal = rootPath + '\\wxlist-final.xlsx'
    wb_save = openpyxl.load_workbook(wxlistfilefinal)
    ws_save = wb_save.active

    # 读取每一行的值
    data_list = []
    for row in ws_save.iter_rows(values_only=True):
        data_list.append(row[2])

    for ar_url in data_list:
        print(ar_url)
        saveData(ar_url)
        time.sleep(random.randint(5, 10))

