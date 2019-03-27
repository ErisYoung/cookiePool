import redis
import random

# redis数据库地址
REDIS_HOST = "localhost"
# 端口
REDIS_PORT = 6379
# 密码 默认为NOne
REDIS_PASSWORD = None


class RedisClient():
    def __init__(self, type, website, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
        self.type = type
        self.website = website

    def name(self):
        """
        获取Redis—Key
        :return: key
        """
        return "{type}:{website}".format(type=self.type, website=self.website)

    def set(self, user_name, value):
        """
        设置新对
        :param user_name:
        :param value:
        :return:
        """
        return self.db.hset(self.name(), user_name, value)

    def delete(self, user_name):

        return self.db.hdel(self.name(), user_name)

    def get(self, user_name):
        return self.db.hget(self.name(), user_name)

    def count(self):
        return self.db.hlen(self.name())

    def random(self):
        return random.choice(self.db.hvals(self.name()))

    def user_names(self):
        return self.db.hkeys(self.name())

    def all(self):
        return self.db.hgetall(self.name())


if __name__=="__main__":
    db=RedisClient("accounts",'weibo')
    print(db.all())
