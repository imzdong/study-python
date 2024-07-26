# -*- coding: utf-8 -*-
import datetime

import requests
import time

import config
from datetime import datetime
from bs4 import BeautifulSoup
# 两个工具类，文章下面有补充
from utils.dbUtils import mysqlUtils as db
from utils.drawingDBUtils import qiniuUtils

# 会封锁的，但是隔一段时间就会解封了。拉取间隔长一点，像同一个公众号的不同文章间隔30s获取一次，不同公众号间隔1分钟，这样就基本不会被封。虽然总体时间长了点，但是胜在稳定

# 目标url
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"

# 使用Cookie，跳过登陆操作
headers = {
    "Cookie": config.COOKIE,
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


# 处理数据库存放结构
def make_data_obj(title, author, cover, synopsis, info_sources, info_url, content, release_time):
    return {
        'title': title,
        'author': author,
        'cover': qiniuUtils.upload_to_qiniu(cover, cover[cover.rfind("=") + 1:]),
        'synopsis': synopsis,
        'info_sources': info_sources,
        'info_url': info_url,
        'content': content,
        'release_time': release_time,
        'create_time': datetime.now(),
    }


# 查询回来的文章对象
""""
{
  "aid": "2658870927_1",
  "album_id": "0",
  "appmsg_album_infos": [],
  "appmsgid": 2658870927,
  "checking": 0,
  "copyright_type": 0,
  "cover": "https://mmbiz.qlogo.cn/sz_mmbiz_jpg/ibQ2cXpBDzUO30PiaMTpymX1DO8UfrZSJVBvSMksJqvKqQMcic0d6l9npiaMHxWLUbxthrylK2zYdU6dibsB0UnNTCg/0?wx_fmt=jpeg",
  "create_time": 1688882993,
  "digest": "",
  "has_red_packet_cover": 0,
  "is_pay_subscribe": 0,
  "item_show_type": 11,
  "itemidx": 1,
  "link": "http://mp.weixin.qq.com/s?__biz=MjM5NzI3NDg4MA==&mid=2658870927&idx=1&sn=644b8b17ba102ebdc61b09a5991720ec&chksm=bd53f2e08a247bf6816c4ef12c2692785f9e95259c54eec20a1643eeff0a41822a1fa51f6550#rd",
  "media_duration": "0:00",
  "mediaapi_publish_status": 0,
  "pay_album_info": {"appmsg_album_infos": []},
  "tagid": [],
  "title": "“现实版许三多”，提干了！",
  "update_time": 1688882992
}
"""


# 获取文章
def do_acquire(number, fakeId, count, author):
    """
    需要提交的data
    以下个别字段是否一定需要还未验证。
    注意修改yourtoken,number
    number表示从第number页开始爬取，为5的倍数，从0开始。如0、5、10……
    token可以使用Chrome自带的工具进行获取
    fakeid是公众号独一无二的一个id，等同于后面的__biz
    """
    data = {
        "token": config.TOKEN,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": number,
        "count": count,
        "query": "",
        "fakeid": fakeId,
        "type": "9",
    }
    # 使用get方法进行提交
    content_json = requests.get(url, headers=headers, params=data).json()
    article_list = []
    now_time = datetime.now()
    # 返回了一个json，里面是每一页的数据
    for item in content_json["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        dt = datetime.fromtimestamp(item["create_time"])
        diff = now_time - dt
        if diff.days <= config.QUERY_TIME_RANGE:
            content = get_article_content(item["link"])
            if filerInfo(content):
                article_list.append(
                    make_data_obj(item["title"], author, item["cover"], "", author, item["link"], content, dt))
                print(item["title"])
            # 间隔5秒防止被封
            time.sleep(5)
        else:
            break
    return article_list


# 是否过滤
def filerInfo(info):
    if config.IS_FILTER == 0:
        for rule in config.KEY_WORDS:
            flag = False
            for keyWords in rule:
                if keyWords in info:
                    flag = True
                    break
            if not flag:
                return False
    return True


def do_query_list():
    count = 5
    for item in config.FAKE_ID_LIST:
        num = 0
        while True:
            infoList = do_acquire(num, item['fakeId'], count, item['name'])
            for info in infoList:
                db.insert_info_reptile_data(info)
            if count > len(infoList):
                break
            # 间隔10秒防止被封
            time.sleep(10)
            num += 5


# 将内容换成字符串类型
def get_article_content(url):
    bf = get_beautiful_soup(url)
    div = bf.find(id='page-content')
    js_content = div.find(id='js_content')
    js_content['style'] = 'visibility: initial'
    filter_tag_src(div)
    return str(div)


# 过滤图片资源
def filter_tag_src(div):
    list = div.find_all('img')
    if len(list) > 0:
        for item in list:
            if item.has_attr('data-src') and item.has_attr('data-type'):
                new_src = qiniuUtils.upload_to_qiniu(item['data-src'], item['data-type'])
                del item['data-src']
                del item['data-type']
                item['src'] = new_src
    return


# 解析url
def get_beautiful_soup(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    html = res.text
    return BeautifulSoup(html, "html5lib")


if __name__ == '__main__':
    do_query_list()


