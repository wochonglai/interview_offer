# -*- coding:utf-8 -*-
import datetime
import time

# 获取一段时间的列表
def get_range_date():
    start_time = datetime.date(2018,1,1)
    end_time = datetime.date(2018,1,10)
    day_range = list()
    for i in range((end_time - start_time).days+1):
        day = start_time + datetime.timedelta(days=i)
        day_range.append(str(day).replace("-",""))

    return day_range

for curr_time in get_range_date():
    print(curr_time)

# 获取昨天日期,返回是一个date类型，可以用str()转换成字符串类型
def get_yesterday_time():
    yesterday = datetime.date.today() - datetime.timedelta(days = 1)
    return yesterday

# 获取当天早上00:00:00时刻时间,晚上23.59.59
current_date = time.strftime('%Y-%m-%d', time.localtime(time.time())) + " 00:00:00"
print(current_date)

current_date = time.strftime('%Y-%m-%d', time.localtime(time.time())) + " 23:59:59"
