#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   多进程-multiprocessing.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/29 22:36   wayne      1.0         None
'''

'''
重点在于
from multiprocessing import Pool
而不是
from multiprocessing.dummy import Pool
'''
import math
from multiprocessing import Pool

def f(x):
    # CPU密集型计算
    return reduce(lambda a, b: math.log(a + b), xrange(10 **5), x)

if __name__ == '__main__':
    pool = Pool(processes=5)
    result = pool.map(f, range(10000000))