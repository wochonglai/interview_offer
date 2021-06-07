# -*- coding:utf-8 -*-
# 获取前一天的日期

def get_yesterday(daystr):
    import datetime
    daylist = daystr.split("/")
    yesterday = datetime.datetime(int(daylist[0]), int(daylist[1]), int(daylist[2])) + datetime.timedelta(days=-1)
    yesterday = str(yesterday)
    return '%s/%s/%s' % (yesterday[:4], yesterday[5:7], yesterday[8:10])

d = get_yesterday('2017/02/09')
print(d)

'''日期迭代'''
import datetime

# 获取一段时间的列表
def get_days_range(stime,etime):
    # stime="20200718"
    # etime="20200809"
    start_time=datetime.datetime.strptime(stime,"%Y%m%d")
    end_time = datetime.datetime.strptime(etime, "%Y%m%d")
    # start_time=datetime.date(2020,7,18)
    # end_time = datetime.date(2020, 8, 9)
    day_range=list()
    for i in range((end_time-start_time).days+1):
        day=start_time+datetime.timedelta(days=i)
        day_range.append(day.strftime("%Y%m%d"))
    return day_range

for i in get_days_range("20200718","20200809"):
    print(i)

# datetime类型直接转时间戳 使用方法.timestamp()

from datetime import datetime, timezone
from pytz import timezone


def utc_2_pk(utctime_str: str) -> datetime:
    '''UTC时间字符串转化为北京时间的datetime对象
    :参数 utctime_str:UTC时间字符串，格式为yyyy-m-d H
    '''
    # 构造出没有时区的datetime对象
    naive_time = datetime.strptime(utctime_str, '%Y-%m-%d %H')
    # 取出上述对象的年月日小时构造一个时区为utc的datetime对象
    utctime = datetime(naive_time.year, naive_time.month, naive_time.day, naive_time.hour, tzinfo=timezone('UTC'))
    # 把时区为utc的对象转化为时区为Asia/Shanghai的datetime对象
    pktime = utctime.astimezone(timezone('Asia/Shanghai'))
    return pktime


def pk_2_utc(pktime_str: str) -> datetime:
    '''北京时间字符串转化为UTC时间的datetime对象
    :参数 pktime_str:北京时间字符串，格式为yyyy-m-d H
    '''
    # 构造出没有时区的datetime对象
    naive_time = datetime.strptime(pktime_str, '%Y-%m-%d %H')
    # 将上述对象转化为时区为Asia/Shanghai的datetime对象
    pktime = naive_time.astimezone(timezone('Asia/Shanghai'))
    # 将时区为上海的datetime对象转化为时区为utc的时间对象
    utctime = pktime.astimezone(timezone('UTC'))
    return utctime

current_time = datetime.datetime.utcnow().isoformat("T")    # '2020-10-15T03:30:29.534260'