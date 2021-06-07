# -*- coding:utf-8 -*-
import pymongo
import gridfs
import urllib.parse
from bson.objectid import ObjectId

MONGODB = {
    'host':'10.134.103.241:27017',
    'username':urllib.parse.quote_plus('E53SBB'),
    'password':urllib.parse.quote_plus('E53SBB20190326'),
    'authMechanism':'SCRAM-SHA-1',
    'authSource':'admin',
    'replicaSet':None
}

client = pymongo.MongoClient(**MONGODB)
mydb = client['E53SBBSPI1'] # 对应的数据库
fs = gridfs.GridFS(mydb)
filename="20181217084231_FOC2250203P_1-PASS.zip"   # spi中是"content.fileList.0.fileName" :
object_id="5c17c84694f4de635909bfaa"  # 文件的objectid，spi中是"content.fileList.0.fileData"对应的)

# 通过object_id获取gridfs中对应的文件，返回是  base64格式?? 字符串
a=fs.get(ObjectId(object_id)).read()

# 写回zip档
with open(filename,'wb') as fw:
    fw.write(a)

