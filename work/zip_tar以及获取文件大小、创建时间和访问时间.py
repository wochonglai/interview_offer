import os, zipfile
#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
  zipf = zipfile.ZipFile(output_filename, 'w')
  pre_len = len(os.path.dirname(source_dir))
  for parent, dirnames, filenames in os.walk(source_dir):
    for filename in filenames:
      pathfile = os.path.join(parent, filename)
      arcname = pathfile[pre_len:].strip(os.path.sep)   #相对路径
      zipf.write(pathfile, arcname)
  zipf.close()
 
import os, tarfile
#一次性打包整个根目录。空子目录会被打包。
#如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
def make_targz(output_filename, source_dir):
  with tarfile.open(output_filename, "w:gz") as tar:
    tar.add(source_dir, arcname=os.path.basename(source_dir))
#逐个添加文件打包，未打包空子目录。可过滤文件。
#如果只打包不压缩，将"w:gz"参数改为"w:"或"w"即可。
def make_targz_one_by_one(output_filename, source_dir):
  tar = tarfile.open(output_filename,"w:gz")
  for root,dir,files in os.walk(source_dir):
    for file in files:
      pathfile = os.path.join(root, file)
      tar.add(pathfile)
  tar.close()


# python 获取文件大小，创建时间和访问时间
# -*- coding: UTF8 -*-

import time
import datetime

import os


'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
  timeStruct = time.localtime(timestamp)
  return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

'''
a = "2013-10-10 23:40:00"
        将其转换为时间数组
        import time
        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
    转换为时间戳:
    timeStamp = int(time.mktime(timeArray))
    timeStamp == 1381419600
    timestr='2018-11-26T11:25:00.407+08:00'
'''
def TimeToTimeStamp(timestr):
  a = timestr.replace("T", " ").split('.')
  timeArray = time.strptime(a[0], "%Y-%m-%d %H:%M:%S")
  timeStamp = int(time.mktime(timeArray))
  b = int(a[1].split('+')[0]) / 1000
  return timeStamp + b




'''获取文件的大小,结果保留两位小数，单位为MB'''
def get_FileSize(filePath):
  filePath = unicode(filePath,'utf8')
  fsize = os.path.getsize(filePath)
  fsize = fsize/float(1024*1024)
  return round(fsize,2)


'''获取文件的访问时间'''
def get_FileAccessTime(filePath):
  filePath = unicode(filePath,'utf8')
  t = os.path.getatime(filePath)
  return TimeStampToTime(t)


'''获取文件的创建时间'''
def get_FileCreateTime(filePath):
  filePath = unicode(filePath,'utf8')
  t = os.path.getctime(filePath)
  return TimeStampToTime(t)


'''获取文件的修改时间'''
def get_FileModifyTime(filePath):
  filePath = unicode(filePath,'utf8')
  t = os.path.getmtime(filePath)
  return TimeStampToTime(t)