# -*- coding:utf-8 -*-
from apscheduler.schedulers.background import BlockingScheduler
import time


scheduler=BlockingScheduler()
@scheduler.scheduled_job("cron",second='*/5')
def run():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))


# scheduler.add_job(run,trigger="cron",second='*/5')
# scheduler.add_job(run,"interval",minutes=2)
scheduler.start()