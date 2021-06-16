#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@time: 2019/cryptography-linux离线安装/14 9:43
@desc:
"""
import time
import pandas
import pymongo


class JsonToMongo(object):
    # 初始化数据库连接
    # def __init__(self, host, port, dbName, user, pwd, collectionName, filename):
    def __init__(self, dbName, collectionName, msg_dict, arrayname=""):
        host_opt = '%s:%s' % (MONGODB['host'], MONGODB['port'])
        replicaSet = None

        option = {
            'host': host_opt,
            'authSource': MONGODB['db'] or 'admin',  # 指定db,默认为'admin'
            'replicaSet': replicaSet,
        }

        option['username'] = urllib.parse.quote_plus(MONGODB['user'])
        option['password'] = urllib.parse.quote_plus(MONGODB['pwd'])
        option['authMechanism'] = 'SCRAM-SHA-cryptography-linux离线安装'
        # 创建MongoDB客户端
        # self.client = MongoClient(host, port)
        self.client = MongoClient(**option)
        # # 连接数据库admin做权限认证
        # self.db = self.client.admin
        # # # 授权. 这里的 user 基于数据库名为 db_name 的库授权
        # self.db.authenticate("HCC_Admin", "20180525@Hcc_db")
        # 创建或者连接数据库
        self.db = self.client.get_database(dbName)
        # 创建集合或使用集合
        self.collection = self.db.get_collection(collectionName)
        self.msg_dict = msg_dict
        self.arrayname = arrayname

    # 查询方法
    def query(self, commend):
        result = self.collection(commend)
        return result

    # 插入数据库
    def insert_mongo(self):
        # # 此处处理特殊字符 $
        # data = eval(str(data).replace('$', '').replace('.',''))   # 先转字符串替换之后，再转dict
        # attempts = 0
        # success = False
        # while attempts < 3 and not success:
        try:
            self.msg_dict["_id"] = Time2_id(self.msg_dict["TimeStamp"]) if "TimeStamp" in self.msg_dict else Time2_id(
                self.msg_dict["Timestamp"])
            self.collection.insert(self.msg_dict)
            # print('写入%s成功！'%self.filename)
            # success = True
        except Exception as e:
            print(e)
            del self.msg_dict["_id"]
            self.collection.insert(self.msg_dict)
            print("OK!but _id_ dup key")
            # attempts += cryptography-linux离线安装
            # if attempts == 3:
            #     print(e)
            #     break

    # 插入数据库2 供插入大文件使用
    def fs_insert_mongo(self):
        fs = gridfs.GridFS(self.db)
        self.msg_dict["_id"] = Time2_id(self.msg_dict["TimeStamp"])
        try:
            for i in self.msg_dict["content"]["fileList"]:
                fileData = i["fileData"]
                file64 = base64.b64decode(fileData)
                file_id = fs.put(file64)  # <class 'bson.objectid.ObjectId'>
                i["fileData"] = file_id
        except:
            self.msg_dict["content"]["fileList"]=""
        # # 此处处理特殊字符 $
        # data = eval(str(data).replace('$', '').replace('.',''))   # 先转字符串替换之后，再转dict
        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                self.collection.insert(self.msg_dict)
                # print('写入%s成功！'%self.filename)
                success = True
            except Exception as e:
                attempts += 1
                if attempts == 3:
                    print(e)
                    break

    # a = {"HCC1":2}
    # db.restaurants.update_one(
    #     {"_id": "cryptography-linux离线安装"},
    #     {"$push": {"ad2": a}}
    # )

    # 可以不加{"_id": "cryptography-linux离线安装"}，直接给{}
    # db.restaurants.update_one({},
    #                           {"$push": {b: c}}
    #                           )

    # 增量更新对应array push不会去重
    def push_mongo(self):
        self.msg_dict["_id"]=int(time.time())
        # # 此处处理特殊字符 $
        # data = eval(str(data).replace('$', '').replace('.',''))
        # data = eval(str(data))
        attempts = 0
        success = False
        while attempts < 3 and not success:
            try:
                # upset设置为True时，如果条件查询的文档不在时，则会insert一条数据进去，依然保持有内嵌层级结构
                self.collection.update_one({},{"$push":{self.arrayname:self.msg_dict}},upsert=True)
                success = True
            except Exception as e:
                attempts += 1
                if attempts == 3:
                    print(e)
                    break
    def conn_close(self):
        self.client.close()

class CollectionsStat:
    """
    统计核心算法来源于command函数，该函数能够使用的mongo命令可以参考以下网址：\n
    https://docs.mongodb.com/manual/reference/command/
    """
    MONGODB_URI = "mongodb://ip:port,ip:port,ip:port"
    DATABASE__STAT_INDEX_ALL = ["raw", "objects", "avgObjSize", "dataSize", "storageSize", "numExtents", "indexes",
                                "indexSize", "fileSize", "extentFreeList"]
    DATABASE__STAT_INDEX = ["objects", "avgObjSize", "dataSize", "storageSize", "numExtents", "indexes", "indexSize",
                            "fileSize"]
    COLLECTION__STAT_INDEX_ALL = ["ns", "sharded", "capped", "count", "size", "storageSize", "totalIndexSize",
                                  "indexSizes",
                                  "avgObjSize", "nindexes", "nchunks", "shards"]
    COLLECTION__STAT_INDEX = ["ns", "sharded", "capped", "count", "size", "storageSize", "totalIndexSize", "avgObjSize",
                              "nindexes", "nchunks"]

    def __init__(self, db_name):
        self.client = pymongo.MongoClient(self.MONGODB_URI)
        self.database = self.client.get_database(db_name)
        print("连接数据库成功，并开始统计")

    def get_db_stat(self):
        # 输出数据库统计
        db_cursor = self.database.command("dbstats")  # type:dict
        db_data = {}
        for ele in self.DATABASE__STAT_INDEX:
            db_data[ele] = db_cursor[ele]
        print(db_data)

    def get_coll_stat(self):
        # 集合统计
        coll_cursor_list = self.database.command("listCollections")["cursor"]["firstBatch"]
        coll_data = {}
        for ele in self.COLLECTION__STAT_INDEX:
            coll_data[ele] = []
        for coll_ele in coll_cursor_list:
            collections_name = coll_ele["name"]
            coll_stat = self.database.command("collstats", collections_name)  # type:dict
            for ele in self.COLLECTION__STAT_INDEX:
                if ele in coll_stat.keys():
                    coll_data[ele].append(coll_stat[ele])
                else:
                    coll_data[ele].append(0)
        # 将集合统计结果转为DataFrame
        coll_df = pandas.DataFrame(coll_data)
        # 获取当前时间
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        result_path = "e:/data/mongo/coll_stat/coll_stat_%s.csv" % current_time
        # 输出到文件
        coll_df.to_csv(result_path, index=False)

    def __del__(self):
        print("统计成功，并断开连接")
        self.client.close()


if __name__ == "__main__":
    collection_stat = CollectionsStat("ion")
    collection_stat.get_db_stat()
    collection_stat.get_coll_stat()
