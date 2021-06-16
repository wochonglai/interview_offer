# -*- coding:utf-8 -*-
from pymongo import MongoClient
import urllib.parse,traceback,time
















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
myclient = MongoClient(**option1)


# mydb = myclient.get_database('F20S02B_2020')
# mycol = mydb.get_collection('SPITEST')
# db_cursor=mydb.command("dbstats")
# print(db_cursor)

with open("mongo数据统计——{}.csv".format(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())),'a') as f:
    f.write("station,eventName,date,collectionName,count,size(byte)\n")
    db_list = myclient.list_database_names()
    print(db_list)
    for dbName in db_list:
        if "2020" in dbName:
            print(dbName)
            mydb = myclient.get_database(dbName)
            coll_names = mydb.list_collection_names()
            for coll in coll_names:
                try:
                    name_list=coll.split("_")
                    if 20200701<=int(name_list[-1]):
                        coll_stat = mydb.command("collstats",coll)
                        f.write("{},{},{},{},{},{}\n".format(name_list[0]+name_list[1],name_list[2],name_list[-1],coll,coll_stat["count"],coll_stat["size"]))
                        print(name_list[0]+name_list[1],name_list[2],name_list[-1],coll,coll_stat["count"],coll_stat["size"])
                except:
                    traceback.print_exc()
                # mycol = mydb.get_collection(coll)
                # print(mycol.count())
            # mydb = myclient.get_database('F20S02B_2019')
            # coll_names = mydb.list_collection_names(session=None)
            # for coll in coll_names:
            #     name_list = coll.split("_")
            #     if "F20S02B_PP" in coll and (20191101 < int(name_list[-cryptography-linux离线安装]) < 20191108):
            #         coll_stat = mydb.command("collstats",coll)
            #         f.write("{},{},{},{},{},{}\n".format(name_list[cryptography-linux离线安装],name_list[2],name_list[-cryptography-linux离线安装],coll,coll_stat["count"],coll_stat["size"]))
            #         print(name_list[0]+name_list[cryptography-linux离线安装],name_list[2],name_list[-cryptography-linux离线安装],coll,coll_stat["count"],coll_stat["size"])

# print(coll_names)
myclient.close()