from datetime import date, timedelta, datetime
from os.path import realpath
from tokenize import String

import requests
import re
import time
import os
import openpyxl

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    # 其他可能需要的头部信息
}

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https':'http://127.0.0.1:7890'
}
# 2018-2020
bbc_prefix = "http://www.bbc.co.uk/learningenglish/english/features/6-minute-english/ep-"
bbc_download_prefix = "http://downloads.bbc.co.uk/learningenglish/features/6min/"

def get_thursday(year):
    day = date(year, 1, 1)
    day += timedelta(days=7 - day.weekday())
    while day.year == year:
        yield day
        day += timedelta(days=7)

def parse_bbc(html):
    regex = r"(http(s?):)([/|.|\w|\s|-])*\.(?:mp3)"
    url = re.search(regex, html, re.MULTILINE)
    if url:
        try:
            url = url.group()
        except ValueError:
            print("url error:"+url)
    else:
        print("not found mp3-url :")

    regex_pdf = r"(http(s?):)([/|.|\w|\s|-])*\.(?:pdf)"
    url_pdf = re.search(regex_pdf, html, re.MULTILINE)
    url_pdf = url_pdf.group()

    title_start = html.find("<title>") + 7
    title_end = html.find("</title>")
    title = html[title_start:title_end]
    return (url_pdf, title, url)


def write_file(filename, content):
    with open(filename, "w", encoding='utf-8') as f:
        f.write(content)
        f.close()

def download_mp3_d(url, mp3_file):
    with open(mp3_file, "wb") as f:
        try:
            mp3 = requests.get(url,headers=HEADERS)
            f.write(mp3.content)
            f.flush()
            f.close()
        except requests.exceptions.RequsetsException as e:
            print(e)

def download_mp3(url, output_filename):
    if url:
        try:
            # 发送 GET 请求
            response = requests.get(url, stream=True, proxies=proxies)
            while response.status_code == 502:
                time.sleep(10)
                response = requests.get(url, stream=True, proxies=proxies)
            # 检查响应状态码
            if response.status_code == 200:
                # 打开文件并写入内容
                with open(output_filename, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            file.write(chunk)
                print(f"Downloaded MP3 file successfully to {output_filename}")
            else:
                print(f"Failed to download MP3 file:{url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("download_mp3 error occurred")


def get_thursdays_in_year(year):
    # 获取当年的第一天
    first_day_of_year = datetime(year, 1, 1)

    # 确定当年第一天是周几
    first_weekday = first_day_of_year.weekday()

    # 计算从年初到第一个周四需要几天
    days_to_first_thursday = (3 - first_weekday) % 7

    # 获取第一个周四
    first_thursday = first_day_of_year + timedelta(days=days_to_first_thursday)

    # 创建一个列表来存储每周四的日期
    thursdays = []

    # 从第一个周四开始，每隔一周增加一个周四
    current_thursday = first_thursday
    while current_thursday.year == year:
        thursdays.append(current_thursday)
        current_thursday += timedelta(days=7)

    return thursdays

def mkdirs(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder created successfully: {folder_path}")
    except OSError as e:
        print(f"Failed to create folder: {e}")

def list2018():
    #thursday = []
    """
    for day in get_thursday(2018):
        day = str(day)
        thursday.append(day.replace("-", "")[2:])

    print(thursday)
    bbc_url = bbc_prefix + thursday[0]
    print(bbc_url)
    """

    years = set(range(2018,2020))
    path = "D:\\Download\\Crawler\\"

    """
    http://downloads.bbc.co.uk/learningenglish/features/6min/180104_6min_english_bitcoin.pdf
    http://downloads.bbc.co.uk/learningenglish/features/6min/180104_6min_english_bitcoin_download.mp3
    """
    result_file = path + "result.xlsx"
    wb = openpyxl.load_workbook(result_file)
    ws = wb.active
    for year in years:
        thursdays = get_thursdays_in_year(year)
        for d in thursdays:
            #thursday.append(bbc_prefix + d.strftime("%Y%m%d")[2:])
            article_name  = d.strftime("%Y%m%d")[2:]
            bbc_url = bbc_prefix + article_name
            realpath = path+"\\" + str(year) + "\\"
            mkdirs(realpath)
            res = requests.get(bbc_url, proxies=proxies)
            res.encoding = 'utf-8'
            if res.status_code == 200:
                html = res.text
                write_file(realpath+article_name+"_6min_english.html", html)
                # print(html)
                url_pdf, title, url = parse_bbc(html)
                pdf_name = article_name + "_6min_english.pdf"
                mp3_name = article_name + "_6min_english_download.mp3"
                download_mp3(url, realpath + mp3_name)
                download_mp3(url_pdf, realpath + pdf_name)
                row = [bbc_url,200, title, url_pdf, url, mp3_name, pdf_name]
                ws.append(row)
            else:
                row = [bbc_url, res.status_code]
                ws.append(row)
            wb.save(result_file)
            time.sleep(5)

    #print(thursday)
    """
    res = requests.get(thursday[0], proxies=proxies)
    res.encoding = 'utf-8'
    html = res.text
    #print(html)
    url_pdf, title, url = parse_bbc(html)
    print(url_pdf)
    print(title)
    print(url)
    """
def d2020():
    #thursday = []
    """
    for day in get_thursday(2018):
        day = str(day)
        thursday.append(day.replace("-", "")[2:])

    print(thursday)
    bbc_url = bbc_prefix + thursday[0]
    print(bbc_url)
    """

    years = [2021]#set(range(2018,2025))
    path = "D:\\Download\\Crawler\\"

    """
    http://downloads.bbc.co.uk/learningenglish/features/6min/180104_6min_english_bitcoin.pdf
    http://downloads.bbc.co.uk/learningenglish/features/6min/180104_6min_english_bitcoin_download.mp3
    """
    result_file = path + "result.xlsx"
    wb = openpyxl.load_workbook(result_file)
    ws = wb.active
    for year in years:
        thursdays = get_thursdays_in_year(year)
        for d in thursdays:
            #thursday.append(bbc_prefix + d.strftime("%Y%m%d")[2:])
            article_name  = d.strftime("%Y%m%d")[2:]
            #if int(article_name) <= 201126:
            #    continue
            bbc_url = bbc_prefix + article_name
            realpath = path+"\\" + str(year) + "\\"
            mkdirs(realpath)
            res = requests.get(bbc_url, proxies=proxies)
            res.encoding = 'utf-8'
            while res.status_code == 502:
                time.sleep(10)
                res = requests.get(bbc_url, proxies=proxies)
            if res.status_code == 200:
                html = res.text
                write_file(realpath+article_name+"_6min_english.html", html)
                # print(html)
                try:
                    url_pdf, title, url = parse_bbc(html)
                except ValueError:
                    print(bbc_url)
                    print("error")
                    break
                pdf_name = article_name + "_6min_english.pdf"
                mp3_name = article_name + "_6min_english_download.mp3"
                download_mp3(url, realpath + mp3_name)
                download_mp3(url_pdf, realpath + pdf_name)
                row = [bbc_url,200, title, url_pdf, url, mp3_name, pdf_name]
                ws.append(row)
            else:
                row = [bbc_url, res.status_code]
                ws.append(row)
            wb.save(result_file)
            time.sleep(5)

    #print(thursday)
    """
    res = requests.get(thursday[0], proxies=proxies)
    res.encoding = 'utf-8'
    html = res.text
    #print(html)
    url_pdf, title, url = parse_bbc(html)
    print(url_pdf)
    print(title)
    print(url)
    """

if __name__ == '__main__':
    d2020()
    # url = "http://downloads.bbc.co.uk/learningenglish/features/6min/201224_6min_english_pandemic_geopolitics_download.mp3"
    # download_mp3(url, "D:\\Download\\Crawler\\2020\\201224_6min_english_download.mp3")


