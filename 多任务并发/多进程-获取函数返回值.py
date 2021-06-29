#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   多进程-获取函数返回值.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/29 23:52   wayne      1.0         None
'''

# https://blog.csdn.net/ztf312/article/details/80337255?utm_term=python%E5%A4%9A%E8%BF%9B%E7%A8%8B%E6%96%B9%E6%B3%95%E6%9C%89%E8%BF%94%E5%9B%9E%E5%80%BC&utm_medium=distribute.pc_aggpage_search_result.none-task-blog-2~all~sobaiduweb~default-8-80337255&spm=3001.4430
# apply_async()本身就可以返回被进程调用的函数的返回值。上一个创建多个子进程的代码中，如果在函数func中返回一个值，
# 那么pool.apply_async(func, (msg, ))的结果就是返回pool中所有进程的值的对象（注意是对象，不是值本身）。

import multiprocessing
import time


def func(msg):
    return multiprocessing.current_process().name + '-' + msg


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)  # 创建4个进程
    results = []
    for i in xrange(10):
        msg = "hello %d" % (i)
        results.append(pool.apply_async(func, (msg,)))
    pool.close()  # 关闭进程池，表示不能再往进程池中添加进程，需要在join之前调用
    pool.join()  # 等待进程池中的所有进程执行完毕
    print("Sub-process(es) done.")

    for res in results:
        print(res.get())



# 方法2
# # 创建进程的方式有两种, 1.封装一个类, 并让该类继承multiprocessing.Process类 2.将方法名和参数传给multiprocessing.Process()的构造函数;
# # 每个进程都有一套自己的内存, 所以在子进程中创建的list或者dict没法直接传回子进程, 只能用多进程模块提供的队列或者管道
# import multiprocessing
# import random
# import os
#
#
# class MyClass(multiprocessing.Process):
#
#     def __init__(self, arr, queue):
#         super().__init__()
#         self.arr = arr
#         self.queue = queue
#
#     def calPow(self):
#         print('父进程id:', os.getppid(), '\t当前子进程id:', os.getpid(), '\n')
#         res = []
#         for i in self.arr:
#             res.append(i * i)
#         # 将结果放入队列
#         self.queue.put(res)
#
#     def run(self):
#         self.calPow()
#
#
# def main():
#     # 生成4个长度为5的list, 等会用4个进程分别计算这4个list中元素的平方
#     arrs = [[random.randint(1, 15) for x in range(5)] for x in range(4)]
#     jobs = []
#     print('\n打印4个list:')
#     for i in range(4):
#         print(arrs[i])
#
#     # 使用4个进程
#     print('\n调用4个子进程:')
#     queues = []
#     for i in range(4):
#         # 使用多进程时，一般使用消息机制实现进程间通信
#         # 每个进程都有一套自己的内存, 所以在子进程中创建的容器没法直接传回子进程, 只能用多进程模块提供的队列或者管道
#         queue = multiprocessing.Queue()
#         queues.append(queue)
#         t = MyClass(arrs[i], queue)
#         jobs.append(t)
#         t.start()
#     result = []
#     # 获取每个进程的结果
#     # print('\n获取每个进程的结果')
#     for i, t in enumerate(jobs):
#         # 等待子进程完成
#         t.join()
#         # 获取子进程的结果
#         result.append(queues[i].get())
#
#     print('\n打印最终结果:')
#     for i in result:
#         print(i)
#
#
# if __name__ == '__main__':
#     main()
# # ————————————————
# # 版权声明：本文为CSDN博主「littlehaes」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# # 原文链接：https://blog.csdn.net/littlehaes/article/details/102626610



# 方法3
# from multiprocessing import Pool
# #pool = Pool（）必须放在if __name__ == '__main__':判断语句中否则报错
# if __name__ == '__main__':
#     pool = Pool（）
#     # 返回值1 = pool.apply_async(函数名，args=（，）).get()
#     # 返回值2 = pool.apply_async(函数名，args=（，）).get()
#     # 返回值3 = pool.apply_async(函数名，args=（，）).get()
#     pool.close()
#     pool.join()
# ————————————————
# 版权声明：本文为CSDN博主「七月__」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/qq_15506981/article/details/113180735