# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from tasks import *


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Happy!")
        asyget.delay(['http://www.baidu.com'])

class TaskHandler(tornado.web.RequestHandler):
    def get(self):
        taskname=self.get_argument('taskname')
        if taskname=='geturl':
            self.write('run task:'+taskname)
            asyget.delay(['http://www.baidu.com'])
        elif taskname=='ptime':
            self.write('run task:' + taskname)
            print_time.delay()

application=tornado.web.Application(
    [
        (r'/',MainHandler),
        (r'/api/task',TaskHandler),
    ]
)

if __name__=="__main__":
    application.listen(9009)
    tornado.ioloop.IOLoop.instance().start()