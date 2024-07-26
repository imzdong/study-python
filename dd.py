import requests

'''
关键字解释：
cooike帮我们绕过登录过程
fakeid是目标公众号的唯一标识符
user-agent可以模拟浏览器请求至此信息获取部分完成，下面开始开始代码部分。
'''

headers = {
    "cookie": "appmsglist_action_3094473706=card; ua_id=ux3LuOWf6ocUYGvpAAAAAHuBi-Ig1E1HhD6Q7B9NLxg=; wxuin=10469175239859; _qimei_uuid42=185100b362c100066c02924fda63204ab606aea5a0; _qimei_fingerprint=4b609d3d1c5c156310315cbfe2e03de0; _qimei_q36=; _qimei_h38=fded78e16c02924fda63204a0200000a118510; mm_lang=zh_CN; ETCI=e3e5d3e1a1ea40da9bf2c4809a00d72f; _clck=3094473706|1|fnr|0; uuid=bc53c5ed137b5a9ebd88ba785a76ac65; rand_info=CAESIB1n4FNRqXU/CYHOT/YUY5kCiGUFMP1XUeBxYWLC1bNp; slave_bizuin=3094473706; data_bizuin=3094473706; bizuin=3094473706; data_ticket=FwuMP6TlpAG3LybOPQpXG2/aT8Aud7ltAuFjPbDFpsFY6UlkbXwY/UsGdCG28If8; slave_sid=SHp4Tm1pZlFsd2hDeFFNcEJFUlM5S1ByZXRuenlDTkR0MFZWemJhTjYzbEszRlI1MHRRd3hIZ3BZenJIUnBRQ2JkNmRwVEZfYU04MUJUS2xMUGwxYk9BOF80aFpHVVp0RWFnSEYwTnlSbFpranFUMTZGYjV5dkhvalVJMWhNOU43SFFWQTBESHJOVVE1aWlz; slave_user=gh_195ed1058a3c; xid=6b509838f192f6142e6e7a2ff5fac532; rewardsn=; wxtokenkey=777; _clsk=7dx3qc|1721878774146|1|1|mp.weixin.qq.com/weheat-agent/payload/record",
    "X-Requested-With": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
}

url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
fad = 'MzUzMjY0NDY4Ng%3D%3D'  # 爬不同公众号只需要更改 fakeid
# MzUzMjY0NDY4Ng==    MjM5MzU1NzkxNQ
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
          'fakeid': fad,
          'type': '9',
          'query': '',
          'token': '254774819',
          'lang': 'zh_CN',
          'f': 'json',
          'ajax': '1',
      }
      r = requests.get(url, headers=headers, params=data)
      dic = r.json()
      for i in dic['app_msg_list']: # 遍历dic['app_msg_list']中所有内容
          title.append(i['title']) # 取 key键 为‘title’的 value值
          link.append(i['link']) # 去 key键 为‘link’的 value值
  return title, link


if __name__ == '__main__':
  (tle, lik) = page(5)
  for x, y in zip(tle, lik):
      print(x, y)