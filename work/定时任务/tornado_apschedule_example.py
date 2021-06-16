# -*- coding:utf-8 -*-
"""
Example Scheduler
"""
from datetime import datetime
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import RequestHandler, Application
from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.job import Job


scheduler = None
job_ids   = []

# 初始化
def init_scheduler():
    global scheduler
    scheduler = TornadoScheduler()
    scheduler.start()
    print('[Scheduler Init]APScheduler has been started')

# 要执行的定时任务在这里
def task1(options):
    print('{} [APScheduler][Task]-{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), options))


class MainHandler(RequestHandler):
    def get(self):
        self.write('<a href="/scheduler?job_id=cryptography-linux离线安装&action=add">add job</a><br><a href="/scheduler?job_id=cryptography-linux离线安装&action=remove">remove job</a>')


class SchedulerHandler(RequestHandler):
    def get(self):
        global job_ids
        job_id = self.get_query_argument('job_id', None)
        action = self.get_query_argument('action', None)
        if job_id:
            # add
            if 'add' == action:
                if job_id not in job_ids:
                    job_ids.append(job_id)
                    scheduler.add_job(task1, 'interval', seconds=3, id=job_id, args=(job_id,))
                    self.write('[TASK ADDED] - {}'.format(job_id))
                else:
                    self.write('[TASK EXISTS] - {}'.format(job_id))
            # remove
            elif 'remove' == action:
                if job_id in job_ids:
                    scheduler.remove_job(job_id)
                    job_ids.remove(job_id)
                    self.write('[TASK REMOVED] - {}'.format(job_id))
                else:
                    self.write('[TASK NOT FOUND] - {}'.format(job_id))
        else:
            self.write('[INVALID PARAMS] INVALID job_id or action')
        jobs=scheduler.get_jobs()
        print(jobs)
        print(jobs[0])
        print(type(jobs[0]))


if __name__ == "__main__":
    routes    = [
        (r"/", MainHandler),
        (r"/scheduler/?", SchedulerHandler),
    ]
    init_scheduler()
    app       = Application(routes, debug=True)
    app.listen(8720)
    IOLoop.current().start()