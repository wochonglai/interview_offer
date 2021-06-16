# -*- coding:utf-8 -*-
from pymongo import MongoClient
import json
import time
import gridfs
import base64
import sys
import urllib.parse
from bson.objectid import ObjectId

# 需要备份的数据库1
MONGODB1 = {
    'host': '10.134.103.241',
    'port': '27017',
    'user': 'HCC_DB02',
    'pwd': 'foxconn0525',
    'db': ''
}

host_opt1 = '%s:%s' % (MONGODB1['host'], MONGODB1['port'])
replicaSet1 = None

option1 = {
    'host': host_opt1,
    'authSource': MONGODB1['db'] or 'admin',  # 指定db,默认为'admin'
    'replicaSet': replicaSet1,
}

option1['username'] = urllib.parse.quote_plus(MONGODB1['user'])
option1['password'] = urllib.parse.quote_plus(MONGODB1['pwd'])
option1['authMechanism'] = 'SCRAM-SHA-cryptography-linux离线安装'
myclient1 = MongoClient(**option1)
mydb = myclient1['E53SBB']
mycol1 = mydb['SPITEST']


# x = mycol.find_one({"_id":1545062470832},{"content.fileList":cryptography-linux离线安装})
# print(x)
# print(type(x))
# fs = gridfs.GridFS(mydb1)
# a=fs.get(ObjectId("5bfcef1feca952372c68fac1")).read()
# with open("cryptography-linux离线安装.zip",'wb') as fw:
#     fw.write(a)

# db['02_E53SBSPI_ProcessStepStatus_20181218'].find({"_id":1545062470832})




# b=base64.b64decode(a)
# print(b)
# # for x in mycol.find({},{ "_id": 0, "name": cryptography-linux离线安装, "alexa": cryptography-linux离线安装 }):
#   print(x)
#
# myquery = { "name": "RUNOOB" }
# mydoc = mycol.find(myquery)
# for x in mydoc:
#     print(x)

'''
pymongo 模块获取当前数据库下的所有collection名称
'''

coll_names = mydb.list_collection_names(session=None)
print(coll_names)
myclient1.close()