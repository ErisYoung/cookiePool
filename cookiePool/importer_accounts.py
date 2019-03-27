from db import RedisClient

IMPORTER_WEBSITE = 'weibo'

conn = RedisClient('accounts', IMPORTER_WEBSITE)


def set(account, sep='----'):
    username, password = account.strip().split(sep)
    print("账号", username, "密码", password)
    result = conn.set(username, password)
    print("录入成功" if result else "录入失败")


def run():
    print("请输入账号密码,exit退出")
    while True:
        account = input()
        if account == 'exit':
            break
        set(account)


def parse_accounts(sep='----'):
    print("正在导入账户")
    with open("account.txt", 'r') as f:
        for account in f.readlines():
            set(account)


if __name__ == "__main__":
    # run()
    parse_accounts()
