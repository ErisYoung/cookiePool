
import time
from multiprocessing import Process
from generator import *
from tester import *
from api import app

TESTER_MAP={
    'weibo':'WeiboTester',
}

GENERATOR_MAP={
    'weibo':'WeiboCookiesGenerator',
}
API_HOST = '0.0.0.0'
API_PORT = 5555
CYCLE=120

API_ENABLED=True
GENERATOR_ENABLED=True
TEST_ENABLED=True

class Scheduler():
    @staticmethod
    def tester_schedule(cycle=CYCLE):
        while True:
            print("检测Cookies模块开始运行")
            try:
                for website,cls in TESTER_MAP.items():
                    tester=eval(cls+"(website='"+website+"')")
                    tester.run()
                    print("Cookies检查完成一次")
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print("检测模块出错",e.args)

    @staticmethod
    def generator_schedule(cycle=CYCLE):
        while True:
            print("生成Cookies模块开始运行")
            try:
                for website,cls in GENERATOR_MAP.items():
                    generator=eval(cls+"(website='"+website+"')")
                    generator.run()
                    print("Cookies生成")
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print("生成模块出错",e.args)

    @staticmethod
    def api():
        print("API接口模块正在运行")
        app.run(host=API_HOST,port=API_PORT)



    def run(self):
        if API_ENABLED:
            api_schedule=Process(target=Scheduler.api)
            api_schedule.start()

        if TEST_ENABLED:
            test_schedule=Process(target=Scheduler.tester_schedule)
            test_schedule.start()

        if GENERATOR_ENABLED:
            generate_schedule=Process(target=Scheduler.generator_schedule)
            generate_schedule.start()


