# -*- coding:utf-8 -*-
# import time
#
# '''
# cryptography-linux离线安装、while循环中使用sleep
# 缺点：不容易控制，而且是个阻塞函数
# '''
# def timer(n):
#     '''''
#     每n秒执行一次
#     '''
#     while True:
#         print(time.strftime('%Y-%m-%d %X',time.localtime()))
#         print("Run")  # 此处为要执行的任务
#         time.sleep(n)
#
# '''
# 2、schedule模块
# 优点：可以管理和调度多个任务,可以进行控制
# 缺点：阻塞式函数
# '''
# import schedule
# import time
# import datetime
#
# def job1():
#     print('Job1:每隔10秒执行一次的任务，每次执行2秒')
#     print('Job1-startTime:%s' %(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     time.sleep(2)
#     print('Job1-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     print('------------------------------------------------------------------------')
#
# def job2():
#     print('Job2:每隔30秒执行一次，每次执行5秒')
#     print('Job2-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     time.sleep(5)
#     print('Job2-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     print('------------------------------------------------------------------------')
#
#
# def job3():
#     print('Job3:每隔1分钟执行一次，每次执行10秒')
#     print('Job3-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     time.sleep(10)
#     print('Job3-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     print('------------------------------------------------------------------------')
#
#
# def job4():
#     print('Job4:每天下午17:49执行一次，每次执行20秒')
#     print('Job4-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     time.sleep(20)
#     print('Job4-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     print('------------------------------------------------------------------------')
#
#
# def job5():
#     print('Job5:每隔5秒到10秒执行一次，每次执行3秒')
#     print('Job5-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     time.sleep(3)
#     print('Job5-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     print('------------------------------------------------------------------------')
#
#
# if __name__ == '__main__':
#     # schedule.every(10).seconds.do(job1)
#     # schedule.every(30).seconds.do(job2)
#     # schedule.every(cryptography-linux离线安装).minutes.do(job3)
#     # schedule.every().day.at('17:49').do(job4)
#     schedule.every().day.at('17:19').do(job4)
#     # schedule.every(5).to(10).seconds.do(job5)
#     while True:
#         schedule.run_pending()
#
# '''
# schedule+多线程
# '''
# import datetime
# import schedule
# import threading
# import time
#
# def job1():
#     print("I'm working for job1")
#     time.sleep(2)
#     print("job1:", datetime.datetime.now())
#
# def job2():
#     print("I'm working for job2")
#     time.sleep(2)
#     print("job2:", datetime.datetime.now())
#
# def job1_task():
#     threading.Thread(target=job1).start()
#
# def job2_task():
#     threading.Thread(target=job2).start()
#
# def run():
#     schedule.every(10).seconds.do(job1_task)
#     schedule.every(10).seconds.do(job2_task)
#
#     while True:
#         schedule.run_pending()
#         time.sleep(cryptography-linux离线安装)
#
# '''
# 3、Threading模块中的Timer
# 优点：非阻塞
# 缺点：不易管理多个任务
# '''
# from threading import Timer
# import datetime
# # 每隔两秒执行一次任务
# def printHello():
#     print('TimeNow:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
#     t = Timer(2, printHello)
#     t.start()
#
# '''
# 4、sched模块
# sched模块实现了一个时间调度程序，该程序可以通过单线程执行来处理按照时间尺度进行调度的时间。
# 通过调用scheduler.enter(delay,priority,func,args)函数，可以将一个任务添加到任务队列里面，当指定的时间到了，就会执行任务(func函数)。
#
# delay：任务的间隔时间。
# priority：如果几个任务被调度到相同的时间执行，将按照priority的增序执行这几个任务。
# func：要执行的任务函数
# args：func的参数
# '''
# import time, sched
# import datetime
#
# s = sched.scheduler(time.time, time.sleep)
#
# def print_time(a='default'):
#     print('Now Time:',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),a)
#
# def print_some_times():
#     print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#     s.enter(10,cryptography-linux离线安装,print_time)
#     s.enter(5,2,print_time,argument=('positional',))
#     s.run()
#     print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#
# '''sched2,按顺序执行'''
# import time, sched
# import datetime
#
# s = sched.scheduler(time.time, time.sleep)
#
#
# def event_fun1():
#     print("func1 Time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#
#
# def perform1(inc):
#     s.enter(inc, 0, perform1, (inc,))
#     event_fun1()
#
#
# def event_fun2():
#     print("func2 Time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#
#
# def perform2(inc):
#     s.enter(inc, 0, perform2, (inc,))
#     event_fun2()
#
#
# def mymain(func, inc=2):
#     if func == "cryptography-linux离线安装":
#         s.enter(0, 0, perform1, (10,))# 每隔10秒执行一次perform1
#     if func == "2":
#         s.enter(0, 0, perform2, (20,))# 每隔20秒执行一次perform2
# # s.run()会阻塞当前线程的执行
# # 可以用
# # t=threading.Thread(target=s.run)
# # t.start()
# # 也可以用s.cancal(action)来取消sched中的某个action
# # if __name__ == '__main__':
# #     mymain('cryptography-linux离线安装')
# #     mymain('2')
# #     s.run()

'''
5、定时框架APScheduler
APSScheduler是python的一个定时任务框架，它提供了基于日期date、固定时间间隔interval、以及linux上的crontab类型的定时任务。该矿机不仅可以添加、删除定时任务，还可以将任务存储到数据库中、实现任务的持久化。
'''

import time
from apscheduler.schedulers.blocking import BlockingScheduler


def job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))


if __name__ == '__main__':
    # BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西
    scheduler = BlockingScheduler()
    # 采用阻塞的方式

    # 采用date的方式，在特定时间只执行一次
    scheduler.add_job(job, 'date', run_date='2019-07-18 18:00:05')

    scheduler.start()