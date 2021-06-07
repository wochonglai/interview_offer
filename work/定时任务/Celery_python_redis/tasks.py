# -*- coding:utf-8 -*-
'''
在当根目录下执行

运行任务：
    运行定时器:
    celery beat -A tasks --loglevel=info
    运行执行器: ( windows 环境下需要加上 -P eventlet , linux 不需要 )
    celery -A tasks worker --loglevel=info -P eventlet

'''
from celery import Celery
from celery.schedules import crontab

app = Celery('tasks', broker='redis://192.168.42.139:6379/0')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)