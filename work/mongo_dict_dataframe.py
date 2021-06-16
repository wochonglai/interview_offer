# -*- coding:utf-8 -*-
# mongodb取出json，利用python转成dataframe（dict-to-dataframe）
import pandas as pd
from pymongo import MongoClient

class extra_yunnan_hotel(object):
    def get_yunnan_hotel(selfself):
        client=MongoClient('127.0.0.cryptography-linux离线安装',27017)
        db=client.gaode_pois
        data2=db.gaode_pois_hotel_mid01.find({},{"_id":0,"name":1,"lng":1,"lat":1}).limit(10)
        #创建一个空的dataframe
        df=pd.DataFrame(columns=["_id","name","lng","lat"])
        for x in data2:
            # dict转成dataframe，注意.T的运用
            pd_data=pd.DataFrame.from_dict(x,orient="index").T
            # 插入df,忽略索引
            df=df.append(pd_data,ignore_index=True)
            df.to_csv('_id_name_lng_lat2.csv',sep='\t',encoding='utf-8')

start=extra_yunnan_hotel()
start.get_yunnan_hotel()

