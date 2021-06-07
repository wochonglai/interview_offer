# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import logging

from datetime import datetime

'''
api 调用结束往PLATFORM_API_LOG写API日志 API_STOP API_PERIOD 单位ms
'''

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to Haina IDB!")

from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.executors.pool import (
    ThreadPoolExecutor,
    ProcessPoolExecutor
)
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.base import JobLookupError
scheduler = None

def modify_logger(logger, log_file):
    # refer: https://docs.python.org/3.5/library/logging.html#logrecord-attributes
    formatter = logging.Formatter(
        fmt='\n'.join([
            '[%(name)s] %(asctime)s.%(msecs)d',
            '\t%(pathname)s [line: %(lineno)d]',
            '\t%(processName)s[%(process)d] => %(threadName)s[%(thread)d] => %(module)s.%(filename)s:%(funcName)s()',
            '\t%(levelname)s: %(message)s\n'
        ]),
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(logging.DEBUG)

    return logger

def get_scheduler(store_path=None, log_file=None):
    if store_path is None:
        store_path = r'jobstore.sqlite'
    if log_file is None:
        log_file = r'logger.log'
    scheduler = TornadoScheduler({'apscheduler.timezone': 'Asia/Shanghai'})
    jobstores = {
        'default': RedisJobStore(host='10.134.103.241', port=6379)
    }
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    scheduler.configure(jobstores=jobstores, executors=executors)
    # # 事件记录
    # scheduler.add_listener(
    #     lambda event: event_listener(event, scheduler),
    #     EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_ADDED | EVENT_JOB_SUBMITTED | EVENT_JOB_REMOVED
    # )
    # 日志定制
    scheduler._logger = modify_logger(scheduler._logger, log_file=log_file)
    return scheduler

# 初始化
def init_scheduler():
    global scheduler
    scheduler = get_scheduler()
    scheduler.start()
    print('[Scheduler Init]APScheduler has been started')



# 要执行的定时任务在这里
def task1(options):
    print('{} [APScheduler][Task]-{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), options))

def task2(*options):
    print('{} [APScheduler][Task]-{}-[msg]:{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), *options))

# 增加任务
def add_task_date(scheduler,func,run_date,args):
    scheduler.add_job(func, 'date', run_date=date(2017, 9, 8), args=[])
    scheduler.add_job(func, 'date', run_date=datetime(2017, 9, 8, 21, 30, 5), args=[])
    scheduler.add_job(func, 'date', run_date='2017-9-08 21:30:05', args=[])

def add_task_interval(scheduler,my_job):
    scheduler.add_job(my_job, 'interval', hours=2)
    scheduler.add_job(my_job, 'interval', hours=2, start_date='2017-9-8 21:30:00', end_date='2018-06-15 21:30:00')

# 删除任务
def del_job(scheduler,job_id=None):
    if job_id is not None:
        scheduler.remove_job(job_id)
    else:
        scheduler.remove_all_jobs()

# 修改任务
def modify_task(scheduler,job_id):
    scheduler.modify_job(job_id,**changes)  # ex: changes={"id":"","func":"","name":"","next_run_time":"","args":[]}


# 查询任务
def get_tasks(scheduler):
    for task in scheduler.get_jobs():
        print(job.id)   # job id
        print(job.args) # 传入的参数



class SchedulerHandler(tornado.web.RequestHandler):
    def get(self):
        job_id = self.get_query_argument('job_id', None)
        action = self.get_query_argument('action', None)
        if job_id:
            # add
            if 'add' == action:
                try:
                    # scheduler.add_job(task1, 'interval', seconds=3, id=job_id, args=(job_id,))  # ,name=task_name
                    # scheduler.add_job(task2, 'date', run_date=datetime(2019, 7, 26, 14, 47, 15), id=job_id, args=[job_id,'海纳智联'])  # ,name=task_name
                    scheduler.add_job(task2, 'date', run_date='2019-8-26 15:30:05', id=job_id,args=[job_id,'海纳智联'])
                    self.write('[TASK ADDED] - {}'.format(job_id))
                except JobLookupError:
                    self.write('[TASK EXISTS] - {}'.format(job_id))
            # remove
            elif 'remove' == action:
                try:
                    scheduler.remove_job(job_id)
                except JobLookupError:
                    print(JobLookupError)
                self.write('[TASK REMOVED] - {}'.format(job_id))
            elif 'modify' == action:
                # try:
                scheduler.modify_job(job_id,args=[job_id,'已修改！'])
                # except JobLookupError:
                #     print(JobLookupError)
                self.write('[TASK MODIFIED] - {}'.format(job_id))
                print(123)

        else:
            self.write('[INVALID PARAMS] INVALID job_id or action')
        jobs=scheduler.get_jobs()
        print(jobs)
        for i in jobs:
            print(i)
            print(i.id)
            print(i.args)



def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/scheduler/?", SchedulerHandler),
    ])

def config_syslog():
	logging.basicConfig(  # filename = os.path.join(os.getcwd(), 'server.log'),
		# level=logging.DEBUG, # if Config.getboolean('Server', 'Debug', False) else logging.WARNING,
        level=logging.INFO,
		filemode='a',
		datefmt='%Y-%m-%d %H:%M:%S',
		format='[%(asctime)s] %(levelname)s: %(message)s')
	logging.info("set sys log!")

# def config_defaultencoding():
# 	try:
# 		reload(sys)
# 		sys.setdefaultencoding('utf-8')
# 		logging.info("set default encodeing utf-8!")
# 	except:
# 		logging.error("set default encoding error!")

if __name__ == "__main__":
    init_scheduler()
    config_syslog()
    # config_defaultencoding()
    app = make_app()
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.bind(8720)
    httpServer.start()
    tornado.ioloop.IOLoop.current().start()