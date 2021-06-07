# -*- coding:utf-8 -*-
import json,datetime,date
from bson.objectid import ObjectId

''' 重写构造json类，遇到日期特殊处理，其余的用内置的就行。'''
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')   # 针对 dateTime 类型
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

''' 重写构造json类，遇到type 'ObjectId'特殊处理，其余的用内置的就行。'''
class ObjectIdError(json.JSONEncoder):
    def default(self, obj):
        print('in')
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)

# 使用方式
json.dumps(dict_data, cls=DateEncoder)

