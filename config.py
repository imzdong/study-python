# 请求的cookie
COOKIE = 'appmsglist_action_3094473706=card; ua_id=ux3LuOWf6ocUYGvpAAAAAHuBi-Ig1E1HhD6Q7B9NLxg=; wxuin=10469175239859; _qimei_uuid42=185100b362c100066c02924fda63204ab606aea5a0; _qimei_fingerprint=4b609d3d1c5c156310315cbfe2e03de0; _qimei_q36=; _qimei_h38=fded78e16c02924fda63204a0200000a118510; mm_lang=zh_CN; ETCI=e3e5d3e1a1ea40da9bf2c4809a00d72f; _clck=3094473706|1|fnr|0; uuid=bc53c5ed137b5a9ebd88ba785a76ac65; rand_info=CAESIB1n4FNRqXU/CYHOT/YUY5kCiGUFMP1XUeBxYWLC1bNp; slave_bizuin=3094473706; data_bizuin=3094473706; bizuin=3094473706; data_ticket=FwuMP6TlpAG3LybOPQpXG2/aT8Aud7ltAuFjPbDFpsFY6UlkbXwY/UsGdCG28If8; slave_sid=SHp4Tm1pZlFsd2hDeFFNcEJFUlM5S1ByZXRuenlDTkR0MFZWemJhTjYzbEszRlI1MHRRd3hIZ3BZenJIUnBRQ2JkNmRwVEZfYU04MUJUS2xMUGwxYk9BOF80aFpHVVp0RWFnSEYwTnlSbFpranFUMTZGYjV5dkhvalVJMWhNOU43SFFWQTBESHJOVVE1aWlz; slave_user=gh_195ed1058a3c; xid=6b509838f192f6142e6e7a2ff5fac532; _clsk=1i6k65o|1721872291912|6|1|mp.weixin.qq.com/weheat-agent/payload/record'
# 请求的token
TOKEN = 'xxx'
# 需要查询的公众号列表
FAKE_ID_LIST = [
    {
        'name': '珠海执优租房',
        'fakeId': 'MzU4MDIyMzU4Mg=='
    }
]

# 是否过滤 0 否， 1 是
IS_FILTER = 0

# 过滤条件，一级的数组需要都满足，二级的数组满足一个即可
KEY_WORDS = [
    ['两室','两厅'],
    ['金湾'],
    ['电梯']
]
# 查询时间范围的，0为今天，1昨天到今天，2前天到今天，以此类推
QUERY_TIME_RANGE = 1


