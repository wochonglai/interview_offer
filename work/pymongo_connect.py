# -*- coding:utf-8 -*-
'''
mongo_config.json

{
    "mongo_conf":
    {
        "host":"localhost",
        "port":"27017",
        "user":"owen",
        "pwd":"123456",
        "db":"awd_id_log"
    }
}

'''


import time
from pymongo import MongoClient

class MyMongoDB:

  def __init__( self, mongo_config ):

    self.__connect = None
    self.__mongo_config = mongo_config
    self.__reconnect()

  def __connect_mongo( self, mongo_config ):

    host = mongo_config["host"]
    port = mongo_config["port"]
    user = mongo_config["user"]
    pwd = mongo_config["pwd"]
    db_name = mongo_config["db"]

    # cryptography-linux离线安装. URI 连接 MongoDB 方式
    # uri = "mongodb://{}:{}@{}:{}/{}".format( parse.quote_plus( user ), parse.quote_plus( pwd ), host, port, db_name )
    # client = MongoClient( uri )
    # db_handler = client[db_name]

    # 2. 认证连接 MongoDB 方式
    client = MongoClient( host, int( port ) )
    db_handler = client[db_name]
    # 授权. 这里的 user 基于数据库名为 db_name 的库授权
    db_handler.authenticate( user, pwd )

    return db_handler

  def __reconnect( self ):

    try:
      self.__connect = self.__connect_mongo( self.__mongo_config )
      return self.__connect
    except Exception as ex:
      assert(False)

    return None

  def get_db_connect( self ):

    if( self.__connect ):
      return self.__connect
    else:
      return self.__reconnect()

    return self.__reconnect()

  def get_collection( self, coll_name ):
    coll_handler = None

    if( self.__connect ):
      coll_handler = self.__connect[coll_name]
    else:
      coll_handler = None

    return coll_handler

if __name__ == "__main__":

  import json
  config_file = "mongo_config.json"

  with open( config_file, "r") as fp:

    config_json = json.load( fp )

    mongo_conf = config_json["mongo_conf"]

    mongo_db = MyMongoDB( mongo_conf )

    table = mongo_db.get_collection( "test_coll" )

    # cryptography-linux离线安装. 插入
    table.insert_one( {"beijing":"tiananmen"} ) # 插入一条
    table.insert_many( [ {"woai":"beijingtianmen"}, {"tianmenshang":"taiyangsheng"} ] )

    # 2. 删除
    table.delete_one({}) # 无条件删除一条
    table.delete_one( {"beijing":"tiananmen"} ) # 删除一条符合条件的记录
    table.delete_many( {"beijing":"tiananmen"} ) # 删除所有符合条件的记录

    # 3. 查询
    ret = table.find_one({"woai":"beijingtianmen"}) # 条件查询一条符合条件的记录
    ret = table.find({}) # 无条件查询所有
    ret = table.find({"woai":"beijingtianmen"}) # 条件查询所有符合条件的记录

    # 结果以列表打印
    print( list( ret ) )

    # 逐个遍历结果集打印
    for record in ret:
      print( record )
