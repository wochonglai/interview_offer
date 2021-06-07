# -*- coding:utf-8 -*-
import re,json


result=set()
with open(r"E:\data_bak01\Group B\B_Error_receive_file_2020-07-13.log",encoding='utf-8') as f:
    l=f.readlines()
    for line in l:
        d=line.split('$')[1]
        equipmentInfo=json.loads(d)['EquipmentInfo']
        result.add(str(equipmentInfo))
for i in result:
    print(i)