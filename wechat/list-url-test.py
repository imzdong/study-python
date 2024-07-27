import requests
import json
import config

'''
关键字解释：
cooike帮我们绕过登录过程
fakeid是目标公众号的唯一标识符*
user-agent可以模拟浏览器请求至此信息获取部分完成，下面开始开始代码部分。
'''

# sub=list&search_field=null&begin=0&count=5&query=&fakeid=MjM5MzU1NzkxNQ%3D%3D&type=101_1&free_publish_type=1&sub_action=list_ex&token=1857985110&lang=zh_CN&f=json&ajax=1

# 会封锁的，但是隔一段时间就会解封了。拉取间隔长一点，像同一个公众号的不同文章间隔30s获取一次，不同公众号间隔1分钟，这样就基本不会被封。虽然总体时间长了点，但是胜在稳定

def page(num=1): # 要请求的文章页数
  title = []
  link = []
  for i in range(num):
      data = {
          'action': 'list_ex',
          'begin': i * 5, # 页数
          'count': '5',
          'fakeid': config.fakeid,
          'type': '9',
          'query': '',
          'token': config.token,
          'lang': 'zh_CN',
          'f': 'json',
          'ajax': '1',
      }
      r = requests.get(config.articles_url, headers=config.headers, params=data)
      print(r)
      dic = r.json()
      print(dic)
      for i in dic['app_msg_list']: # 遍历dic['app_msg_list']中所有内容
          op = json.dumps(i)
          # printing result as string
          print("final string = ", op)
          title.append(i['title']) # 取 key键 为‘title’的 value值
          link.append(i['link']) # 去 key键 为‘link’的 value值
  return title, link


if __name__ == '__main__':
  (tle, lik) = page(1)
  for x, y in zip(tle, lik):
      print(x, y)