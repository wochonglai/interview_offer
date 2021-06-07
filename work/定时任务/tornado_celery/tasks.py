# -*- coding:utf-8 -*-

import time
from celery.bin import worker as celery_worker
from celery import Celery, platforms
from datetime import timedelta
from urllib import request
from tornado.httpclient import HTTPClient


platforms.C_FORCE_ROOT=True
broker='amqp://admin:guest@127.0.0.1:5672/'
backend='redis://192.168.42.139:6379/2'

celery=Celery('tasks',broker=broker,backend=backend)

celery.conf.update(
    CELERYBEAT_SCHEDULE={
        'perminute':{
            'task':'tasks.asyget',
            'schedule':timedelta(seconds=1),
            'args':['http://www.baidu.com']
        }
    }
)

@celery.task
def asyget(urls):
    """
    req = request.Request(url='%s' % (urls))
    res = request.urlopen(req)
    res = res.read()
    print(res.decode(encoding='utf-8'))
    """

    http_client=HTTPClient()
    response=http_client.fetch(urls)
    print(response.body)

@celery.task
def print_time():
    print("now is: "+str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))

def work_start():
    worker=celery_worker.worker(app=celery)
    worker.run(
        broker=broker,
        concurrency=4,
        traceback=False,
        loglevel='INFO'
    )

if __name__=='__main__':
    work_start()