import requests
import openpyxl
import config
import time
import random
import json

'''
关键字解释：
cooike帮我们绕过登录过程
fakeid是目标公众号的唯一标识符
user-agent可以模拟浏览器请求至此信息获取部分完成，下面开始开始代码部分。
'''

count = 5
# 爬不同公众号只需要更改 fakeid 1857985110
rootPath = 'D:\\WorkSpace\\idea\\python\\wechat\\'
wxlistfile = rootPath + 'wxlist.xlsx'

def getwxlist(wxid):

    begin = "0"
    params = {
        "action": "list_ex",
        "begin": begin,
        "count": count,
        "fakeid": wxid,
        "type": "9",
        "token": config.token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }
    # 会封锁的，但是隔一段时间就会解封了。拉取间隔长一点，像同一个公众号的不同文章间隔30s获取一次，不同公众号间隔1分钟，这样就基本不会被封。虽然总体时间长了点，但是胜在稳定
    # 获取历史抓取记录
    wb = openpyxl.load_workbook(wxlistfile)
    ws = wb.active
    # 在不知道公众号有多少文章的情况下，使用while语句
    # 也方便重新运行时设置页数
    i = 0
    # 新增抓取计数
    j = 0
    while True:
        begin = i * count
        params["begin"] = str(begin)
        resp = requests.get(config.articles_url, headers=config.headers, params=params)
        # 微信流量控制, 退出
        if resp.json()['base_resp']['ret'] == 200013:
            print("frequencey control, stop at {}".format(str(begin)))
            wb.save(wxlistfile)
            time.sleep(random.randint(60*60, 62*60))
            continue
        # 如果返回的内容中为空则结束
        if len(resp.json()['app_msg_list']) == 0:
            print("all ariticle parsed")
            print(f"新增页面抓取已完成,{j}篇文章已添加\n")
            break
        msg = resp.json()
        if "app_msg_list" in msg:
            for item in msg["app_msg_list"]:
                op = json.dumps(item)
                # printing result as string
                print("final string = ", op)
                row = [item['title'], item['link'], op]
                ws.append(row)
                j += 1
            print(f"第{i}页爬取成功\n")
        # 翻页
        i += 1
        # 随机暂停几秒，避免过快的请求导致过快的被查到
        time.sleep(random.randint(1*60, 3*60))
    wb.save(wxlistfile)

if __name__ == '__main__':
    getwxlist(config.fakeid)

