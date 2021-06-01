#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   leak_memory.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/2 1:01   wayne      1.0         None
'''
'''python内存泄漏调试
https://zhmin.github.io/2018/12/22/python-meomory-leak/
记录一次内存泄漏的调试经历
最近写了一个项目，是关于爬虫的，里面涉及到了django作为orm。当时在服务器上运行程序，发现内存占用持续增长，最后直到被系统kill。遇到这个问题，首先要弄清楚内存里面，到底存储了哪些类型的数据。这里主要使用了objgraph，pympler，guppy工具。

使用objgraph观察
这里简化下代码, 使用函数dosomething表示一次爬取任务执行。每1分钟执行一次'''

import objgraph
import schedule


def dosomething():
    objgraph.show_growth()
    # ........ 爬取任务
    pass


schedule.every(1).minutes.do(dosomething)

'''
注意到第一次会出现大幅的增量，是因为第一运行加载类，函数等对象。 从后面的输出结果，可以看到ObservationList和IdentityPartitionCluster一直在持续增长，但是只能看到数量，并不能看到占用内存的数据大小和内容。

使用pympler工具
pympler工具可以很容易看到内存的使用情况，用法如下
'''
import objgraph
import schedule
from pympler import tracker, muppy, summary

tr = tracker.SummaryTracker()


def dosomething():
    print
    "memory total"
    all_objects = muppy.get_objects()
    sum1 = summary.summarize(all_objects)
    summary.print_(sum1)

    print
    "memory difference"
    tr.print_diff()
    # ........ 爬取任务
    pass


schedule.every(1).minutes.do(dosomething)

'''
可以看到unicode类型，一直在持续增长。从当初4M多，一直持续增长到385M。知道了是unicode的问题，接下来要观察下这些unicode被哪些对象引用。

使用guppy工具
guppy可以查看到heap内存的具体使用情况，哪些对象占用多少内存。'''

import objgraph
import schedule
import guppy
from pympler import tracker, muppy, summary

tr = tracker.SummaryTracker()
hp = guppy.hpy()  # 初始化了SessionContext，使用它可以访问heap信息


def dosomething():
    print
    "heap total"
    heap = hp.heap()  # 返回heap内存详情
    references = heap[0].byvia  # byvia返回该对象的被哪些引用， heap[0]是内存消耗最大的对象
    print
    references

    # ........ 爬取任务
    pass


schedule.every(1).minutes.do(dosomething)
# 比如上面的代码，返回哪些object引用了unicode这个类型。


import objgraph
import schedule
import guppy
from pympler import tracker, muppy, summary

tr = tracker.SummaryTracker()
hp = guppy.hpy()


def dosomething():
    print
    "heap total"
    heap = hp.heap()
    references = heap[0].byvia
    print
    references[0].kind
    print
    references[0].shpaths
    print
    references[0].rp

    # ........ 爬取任务
    pass


schedule.every(1).minutes.do(dosomething)
# shpaths返回从最顶端的root到这个object的最短引用路径。rp返回被哪些类型应用信息。

# 可以明显得看到是django的问题，后来上网查了下django内存泄漏，原来是因为django在debug模式下，会保存每一次的sql语句。终于弄清楚了原因，解决办法是把django的settings的debug设置为False。