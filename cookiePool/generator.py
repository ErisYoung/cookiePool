import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from db import RedisClient
from weibo.cookies import WeiboCookies

BROWSER_TYPE="Chrome"

class CookiesGenerator():
    def __init__(self,website="default"):
        self.website=website
        self.cookie_db=RedisClient('cookies',self.website)
        self.account_db = RedisClient('accounts', self.website)
        self.browser=self.init_browser()

    def init_browser(self):
        if BROWSER_TYPE=="PhantomJS":
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

            browser=webdriver.PhantomJS(desired_capabilities=caps)
            browser.set_window_size(1400,500)
            return browser
        elif BROWSER_TYPE=="Chrome":
            browser=webdriver.Chrome()
            return browser

    def new_cookies(self,username,password):

        raise NotImplementedError

    def parse_cookies_dict(self,cookies):
        dic={}
        for cookie in cookies:
            dic[cookie['name']]=cookie['value']

        return dic

    def run(self):
        account_usernames=self.account_db.usernames()
        cookies_usernames = self.cookie_db.usernames()

        for username in account_usernames:
            if not username in cookies_usernames:
                password=self.account_db.get(username)
                print("正在生成Cookies",username,password)
                result=self.new_cookies(username,password)
                if result.get("status")==1:
                    cookies=self.parse_cookies_dict(result.get('content'))
                    print("成功获取Cookies",cookies)
                    if self.cookie_db.set(username,json.dumps(cookies)):
                        print("成功保存Cookies")
                elif result.get('status')==2:
                    print("密码错误")
                    if self.account_db.delete(username):
                        print("删除成功")
                else:
                    print(result.get("content"))

        print("所有账号已经成功获取Cookies")

    def close(self):
        try:
            print("Closing Browser")
            self.browser.close()
            del self.browser
        except TypeError:
            print("Browser not opened")

    def __del__(self):
        self.close()



class WeiboCookiesGenerator(CookiesGenerator):
    def __init__(self,website="weibo"):
        super().__init__(website)
        self.website=website

    def new_cookie(self,username,password):
        weiboCookie=WeiboCookies(username,password,self.browser)
        return weiboCookie.main()

if __name__=="__main__":
    generator=WeiboCookiesGenerator()
    generator.run()


