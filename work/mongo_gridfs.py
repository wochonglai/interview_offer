# -*- coding:utf-8 -*-
import pymongo
import gridfs
import os.path
from bson.objectid import ObjectId  # *******************
import json
import base64


'''
# 创建类
client = pymongo.MongoClient()
# 选择了test数据库
db = client.test
# 指定GridFS的collection为upload，如果是fs则修改第二个参数或不填
fs = gridfs.GridFS(db, "upload")
# 指定collection
collection = db.upload.files
# 保存文件路径
dirs = "/root/pic/upload/"

for row in collection.find({}, no_cursor_timeout=True):
    filename = row["filename"]
    md5 = row["md5"]
    # 保存文件名
    localfile = dirs + "/" + md5[0:2] + "/" + md5[2:4] + "/" + os.path.basename(filename)
    os.makedirs(os.path.dirname(localfile), mode=0o777, exist_ok=True)  # python2需判断文件夹是否存在，去除exist_ok
    with open(localfile, "wb") as f:
        f.write(fs.get(ObjectId(row["_id"])).read())

'''
client = pymongo.MongoClient('10.134.103.241', 27017)
db = client.test
fs = gridfs.GridFS(db)
with open(r"E:\Data\02_E53SBBSPI1\E53SBSPI-1542191260389-103-ProcessStepStatus-20181114182734444.json", 'r') as jsonfile:
    v = json.load(jsonfile)
zip_fileName = v["content"]["fileList"][0]["fileName"]
zip_fileData = v["content"]["fileList"][0]["fileData"]
zip_file=base64.b64decode(zip_fileData)
a = fs.put(zip_file)
print(a)
print(type(a))

# 要读取fs存储文件
print(fs.get(a).read())
with open("test1.zip",'wb') as fw:
    fw.write(fs.get(a).read())


v["content"]["fileList"][0]["fileData"]=a
db.get_collection("SPITEST").insert(v)
test1 = b''
print(fs.put(zip_file))