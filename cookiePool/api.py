import json
from flask import Flask, g
from db import RedisClient

GENERATOR_MAP = {
    'weibo': 'WeiboCookiesGenerator',
}

__all__ = ['app']
app = Flask(__name__)


@app.route('/')
def index():
    return "<h2>Welcome to Cookie Pool System</h2>"


def get_conn():
    """
    动态设置参数，对于每个站点，使用eval
    :return:
    """
    for website in GENERATOR_MAP:
        if not hasattr(g, website):
            setattr(g, website + "_cookies", eval("RedisClient('cookies','" + website + "')"))
            setattr(g, website + "_accounts", eval("RedisClient('accounts','" + website + "')"))
    return g


@app.route('/<website>/random')
def random(website):
    conn = get_conn()
    cookies = getattr(conn, website + "_cookies").random()
    return cookies


@app.route('/<website>/count')
def count(website):
    conn = get_conn()
    cookies_count = getattr(conn, website + "_cookies").count()
    return json.dumps({'count': cookies_count, 'status': '1'})


@app.route('/<website>/add/<username>/<password>')
def add(website, username, password):
    conn = get_conn()
    getattr(conn, website + "_accounts").set(username, password)
    return json.dumps({'status': '1'})
