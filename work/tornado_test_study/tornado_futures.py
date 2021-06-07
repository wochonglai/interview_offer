# -*- coding:utf-8 -*-
# 一个用concurrent.futures 下的 ThreadPoolExecutor解决tornado单线程处理耗时任务的例子
import tornado.ioloop
import tornado.web
import tornado.httpserver
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import time
class App(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/sleep/(\d+)', SleepHandler),
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, **settings)
class BaseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world %s" % time.time())
class SleepHandler(BaseHandler):
    @run_on_executor
    def get(self, n):
        time.sleep(float(n))
        self._callback()
    def _callback(self):
        self.write("after sleep, now I'm back %s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
if __name__ == "__main__":
    app = App()
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
