# -*- coding:utf-8 -*-
from redis import StrictRedis
import time,json,datetime,sys

redis_=StrictRedis(host='10.157.10.110',port=6379,db=1,password='hcc123456')
# redis_.set('name','Wayne')
# print(redis_.get('temp_wet'))   # b'Wayne'
# print(redis_.get('name').decode('utf-8'))


# redis_.set('ab098397-8613-42a4-9d30-6291604a0819','还在',ex=5)    # 设置过期时间
# with open(r"E:\data_bak01\0507_Pana_HUB_log\MIND-IMS-Pana-API测试\IMS主动发起\FEAT028_UnlockStationResponse.json",encoding="utf-8") as f:
#     d=json.load(f)
#     a=json.dumps(d)
#     print(a)
# redis_.set(d["UniqueID"],a)
# print(redis_.get(d["UniqueID"]))
# time.sleep(5)
# print(redis_.get(d["UniqueID"]))
# print(redis_.get("ab098397-8613-42a4-9d30-6291604a0819"))


# list操作
# redis_.lpush("F20S01B_Reflow08","")
for i in range(10):
    redis_.lpush("rsn","testSN%d"%i)

print(redis_.lrange("rsn",0,-1))
redis_.ltrim("rsn",0,0)
print(redis_.lrange("rsn",0,-1))
redis_.rpop("rsn")
print(redis_.lrange("rsn",0,-1))
print(redis_.lrange("temp_wet",0,-1))
# # list 长度控制
# redis_.ltrim("F20S01B_Reflow08",0,7)    #控制为8个
# print(redis_.lrange("F20S01B_Reflow08",0,-1))
# for i in redis_.lrange("F20S01B_Reflow08",0,-1):
#     print("a"+i.decode()+"c")
# redis_.delete("F20S01B_Reflow08")
# redis_.ltrim("temp_wet", 0, 0)
# print(redis_.lrange("temp_wet",0,-1))
# a=redis_.lrange("temp_wet",0,1)[0].decode('utf-8')
# print(redis_.lrange("temp_wet",0,1))
# b=eval(a)
# print(type(b))
# print(b)
# print(b[2])

# sys.path.append("..")
# from common.mysql_exc import Mysqlpython
#
# sqlc = Mysqlpython(host="10.134.103.247",db="smt_mind")
# a=redis_.lrange("temp_wet",0,2)
# value_sql = "insert into temp_wet_records values(%s,%s,%s,%s,%s)"
# value_list = [eval(i.decode('utf-8'))[:5] for i in a]
# for j in value_list:
#     try:
#         sqlc.exec(value_sql,j)
#     except:
#         traceback.print_exc()
# # print(value_list)
# # print(type(value_list[0][4]))
# # sqlc.exec_many(value_sql, value_list)
# sqlc.close()