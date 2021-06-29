#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   多线程-threading带返回值.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/29 22:41   wayne      1.0         None
'''

'''
Python 从多线程中返回值，有多种方法：
1、常见的有写一个自己的多线程类，写一个方法返回。
2、可以设置一个全局的队列返回值。
3、也可以用multiprocessing.pool.ThreadPool'''
import time

from threading import Thread

def foo(number):
    time.sleep(20)
    return number

class MyThread(Thread):

    def __init__(self, number):
        Thread.__init__(self)
        self.number = number

    def run(self):
        self.result = foo(self.number)

    def get_result(self):
        return self.result


thd1 = MyThread(3)
thd2 = MyThread(5)
thd1.start()
thd2.start()
thd1.join()
thd2.join()

print(thd1.get_result())
print(thd2.get_result())




from time import ctime, sleep
import threading

loops = [4, 2]


class MyThread(object):
    def __init__(self, func, args, name=''):
        self.name = name
        self.func = func
        self.args = args

    def __call__(self):
        self.func(*self.args)


def loop(nloop, nsec):
    print('start loop', nloop, 'at :', ctime())
    sleep(nsec)
    print('done loop', nloop, 'at:', ctime())


def main():
    print('start at', ctime())
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = threading.Thread(target=MyThread(loop, (i, loops[i]), loop.__name__))
        threads.append(t)
    for i in nloops:  # start threads 此处并不会执行线程，而是将任务分发到每个线程，同步线程。等同步完成后再开始执行start方法
        threads[i].start()
    for i in nloops:  # jion()方法等待线程完成
        threads[i].join()
    print('DONE AT:', ctime())


if __name__ == '__main__':
    main()