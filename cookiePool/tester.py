import requests as rq
import json
from db import RedisClient

TEST_URL_MAP={"weibo":"https://m.weibo.cn/"}

class Tester():
    def __init__(self,website="default"):
        self.website=website
        self.cookie_db = RedisClient('cookies', self.website)
        self.account_db = RedisClient('accounts', self.website)

    def test(self,username,cookie):
        raise NotImplementedError

    def run(self):
        cookies=self.cookie_db.all()
        for username,cookie in cookies.items():
            self.test(username,cookie)

class WeiboTester(Tester):
    def __init__(self,website="weibo"):
        super().__init__(website)
        self.website=website

    def test(self,username,cookie):
        try:
            cookies=json.loads(cookie)
        except TypeError:
            self.cookie_db.delete(username)
            return
        try:
            url=TEST_URL_MAP[self.website]
            res=rq.get(url,cookies=cookies,timeout=5,allow_redirects=False)
            if res.status_code==200:
                print("Cookie有效",username)
                print("部分结果",res.text[:50])
            else:
                print(res.status_code,res.headers)
                print("Cookie 失效，删除",username)
                self.cookie_db.delete(username)
        except ConnectionError as e:
            print("出现异常",e.args)




