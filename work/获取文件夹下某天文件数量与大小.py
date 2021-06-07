# -*- coding:utf-8 -*-
import time
import datetime
import os

showtime = "20181125"
dirpath = r"E:\Data"

'''把时间戳转化为时间: 1479264792 to 20161116'''
def TimeStampToTime(timestamp):
  timeStruct = time.localtime(timestamp)
  return time.strftime('%Y%m%d',timeStruct)

'''获取文件的大小,结果保留两位小数，单位为MB'''
def get_FileSize(filePath):
  fsize = os.path.getsize(filePath)
  fsize = fsize/float(1024*1024)
  return round(fsize,2)

'''获取文件的创建时间'''
def get_FileCreateTime(filePath):
  t = os.path.getctime(filePath)
  return TimeStampToTime(t)


with open('count_size.txt', 'a', encoding='utf-8') as f:
    for root,dir1,filename in os.walk(dirpath):
        for dirname in dir1:
            filesize = 0
            filecount = 0
            for root1, dir2, filenameList in os.walk(root+'\\'+dirname):
                for filename2 in filenameList:
                    if get_FileCreateTime(root1+'\\'+filename2)==showtime:
                        filesize+=get_FileSize(root1+'\\'+filename2)
                        filecount+=1
            f.write(showtime+' '+dirname + '新增 '+ '文件数量：'+str(filecount)+'  文件大小：'+str(filesize))
            f.write('\n')