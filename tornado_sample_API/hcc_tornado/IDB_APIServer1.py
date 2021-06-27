# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver,urllib.parse,datetime
import logging,sys,json
sys.path.append("..")
from HCCAPI.HCC_Mind01 import *
from HCCAPI.HCC_Mind02 import *
from HCCAPI.HCC_Mind03 import *
import uuid # 用于生成全局唯一标识符GUID
from apicommon.methods import send_msg

from apscheduler.schedulers.tornado import TornadoScheduler
from apscheduler.executors.pool import (
    ThreadPoolExecutor,
    ProcessPoolExecutor
)
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.jobstores.base import JobLookupError
scheduler = None

'''
api 调用结束往PLATFORM_API_LOG写API日志 API_STOP API_PERIOD 单位ms
'''
def modify_logger(logger, log_file):
    formatter = logging.Formatter(
        fmt='\n'.join([
            '[%(name)s] %(asctime)s.%(msecs)d',
            '\t%(pathname)s [line: %(lineno)d]',
            '\t%(processName)s[%(process)d] => %(threadName)s[%(thread)d] => %(module)s.%(filename)s:%(funcName)s()',
            '\t%(levelname)s: %(message)s\n'
        ]),
        datefmt='%Y-%m-%d %H:%M:%S'
    )
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
    # 日志定制
    scheduler._logger = modify_logger(scheduler._logger, log_file=log_file)
    return scheduler

# 初始化
def init_scheduler():
    global scheduler
    scheduler = get_scheduler()
    scheduler.start()
    print('[Scheduler Init]APScheduler has been started')

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Welcome to Haina IDB!")
'''
/MINDAPI/MIND002, Mind_scheduler,用于定时发送消息
'''
class Mind_scheduler(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        try:
            rec = json.loads(urllib.parse.unquote(self.request.body.decode('utf-8')))
            send_type = rec["type"]  # 推播类型，群发0或单发1
            userIds = rec["userIds"] if  "userIds" in rec else ""   # 单发的userId字符串，以 ；分割
            sendTimeType = rec["sendTimeType"]  if  "sendTimeType" in rec else "" # 1 定时发送、0 正常发送
            timing = rec["timing"] if  "timing" in rec else ""
            msg=rec["msg"]
            job_id = rec["job_id"]
            action = rec["action"]
            # 新建空字典，用来存储返回数据
            res = {}

            if sendTimeType==1:
                # add
                if 'add' == action:
                    try:
                        scheduler.add_job(send_msg, 'date', run_date=timing, kwargs={"send_type":send_type, "userIds":userIds, "msg":msg})
                    except JobLookupError:
                        self.write('[TASK EXISTS] - {}'.format(job_id))
                # remove
                elif 'remove' == action:
                    try:
                        scheduler.remove_job(job_id)
                    except JobLookupError:
                        print(JobLookupError)
                elif 'modify' == action:
                    try:
                        scheduler.modify_job(job_id,next_run_time=timing,kwargs={"send_type":send_type, "userIds":userIds, "msg":msg})
                    except JobLookupError:
                        print(JobLookupError)
                elif 'removeAll'==action:
                    if job_id=="p@ssword":
                        scheduler.remove_all_jobs()
                elif 'getJobs'==action:
                    jobs = scheduler.get_jobs()
                    task_list=[]
                    for job in jobs:
                        jobInfo={}
                        jobInfo["jobId"] = job.id
                        jobInfo["jobName"] = job.name
                        jobInfo["jobFunc"] = str(job.func)
                        jobInfo["jobNextRunTime"] = str(job.next_run_time)
                        jobInfo["jobKwargs"] = job.kwargs
                        task_list.append(jobInfo)
                    res['taskList'] = task_list
                    # print(jobs)
                    # for i in jobs:
                    #     print(i)
                    #     print(i.id)
                    #     print(i.kwargs)
            elif sendTimeType==0:
                send_msg(send_type, userIds, msg)
            # 新建空字典result_d，用来存储res中键result对应的值

            res['resultCode'] = 1
            res['errorMessage'] = None
            res['errorCode'] = None
            response = json.dumps(res, ensure_ascii=False)
            self.write(response)
        # 如果参数不全
        except Exception as e:
            res = {"resultCode": 0, "result": None, "errorMessage": "缺少必要參數", "errorCode": "ER001"}
            # response = json.dumps(res, ensure_ascii=False)
            self.write(res)


def make_app():
    return tornado.web.Application([
        (r"/MINDAPI/MINDtest", GetTestAPI),
        (r"/", MainHandler),
        (r"/MINDAPI/MIND001", MindLogin),
        (r"/MINDAPI/MIND002", Mind_scheduler),
        (r"/MINDAPI/MIND003", MIND_APP_login),
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
    httpServer.bind(8008)
    httpServer.start()
    tornado.ioloop.IOLoop.current().start()