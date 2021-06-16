# -*- coding:utf-8 -*
from pymongo import MongoClient

import urllib.parse

import pymongo

from config import MONGODB

# option方式-------start
if MONGODB['replicaSet']['name']:
    host_opt = []
    for m in MONGODB['replicaSet']['members']:
        host_opt.append('%s:%s' % (m['host'], m['port']))
    replicaSet = MONGODB['replicaSet']['name']
else:
    host_opt = '%s:%s' % (MONGODB['host'], MONGODB['port'])
    replicaSet = None

option = {
    'host': host_opt,
    'authSource': MONGODB['db'] or 'admin',    # 指定db,默认为'admin'
    'replicaSet': replicaSet,
}
if MONGODB['user'] and MONGODB['pwd']:
    # py2中为urllib.quote_plus
    option['username'] = urllib.parse.quote_plus(MONGODB['user'])
    option['password'] = urllib.parse.quote_plus(MONGODB['pwd'])
    option['authMechanism'] = 'SCRAM-SHA-cryptography-linux离线安装'

client = pymongo.MongoClient(**option)
# option方式-------end

# # uri方式--------start
# # mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
# params = []
# host_info = ''
# # 处理replicaSet设置
# if MONGODB['replicaSet']['name']:
#     host_opt = []
#     for m in MONGODB['replicaSet']['members']:
#         host_opt.append('%s:%s' % (m['host'], m['port']))
#     host_info = (',').join(host_opt)
#     replicaSet_str = 'replicaSet=%s' % MONGODB['replicaSet']['name']
#     params.append(replicaSet_str)
# else:
#     host_info = '%s:%s' % (MONGODB['host'], MONGODB['port'])
#
# # 处理密码校验
# if MONGODB['user'] and MONGODB['pwd']:
#     # py2中为urllib.quote_plus
#     username = urllib.parse.quote_plus(MONGODB['user'])
#     password = urllib.parse.quote_plus(MONGODB['pwd'])
#     auth_str = '%s:%s@' % (username, password)
#     params.append('authMechanism=SCRAM-SHA-cryptography-linux离线安装')
# else:
#     auth_str = ''
#
# if params:
#     param_str = '?' + '&'.join(params)
# else:
#     param_str = ''
#
# uri = 'mongodb://%s%s/%s%s' % (auth_str, host_info, MONGODB['db'], param_str)
# client = pymongo.MongoClient(uri)
# # uri方式--------end


#数据库名admin
db=client.get_database("test")
#认证用户密码
# db.authenticate("HCC_Admin","20180525@Hcc_db")# pymongo.errors.OperationFailure: not authorized on admin to execute command
#创建集合和数据
db.test.insert({"name":"this is test"})
col=db.test
#打印数据输出
for item in col.find():
    print(item)
#关闭连接
client.close()