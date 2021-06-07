# -*- coding:utf-8 -*-
# import ftplib
# from ftplib import FTP
#
user = 'program'
passwd = 'foxconn168!!'
# ftp =FTP()
# ftp.connect(host='10.143.192.16')
# ftp.login(user=user, passwd=passwd)
# cat = ftp.dir()
# print(cat.encode("utf-8"))

from ftplib import FTP

encode = ['UTF-8', 'gbk', 'GB2312', 'GB18030', 'Big5', 'HZ']

user = 'program'
passwd = 'foxconn168!!'
ftp =FTP()
ftp.connect(host='10.143.192.16')
ftp.encoding="Big5"
ftp.login(user=user, passwd=passwd)
print (ftp.getwelcome())
cat = ftp.dir()
print(cat)

def logFTP(code):
    ftp = FTP('10.143.192.16')
    try:
        ftp.login(user=user, passwd=passwd)
        ftp.encoding = code
        # lst = ftp.dir()
        ftp.cwd('AOI SPI PROGRAM-重要勿刪!'.encode("utf-8"))
        lst = ftp.nlst()
        for s in lst:
            print(s)
    except(UnicodeDecodeError):
        print('123')
        pass
    finally:
        print(code)
        t = input('Is this?:')
        ftp.quit()


for enc in encode:
    logFTP(enc)