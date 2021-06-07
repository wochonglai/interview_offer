# -*- coding:utf-8 -*-
import logging

# 创建一个logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler(r'C:\Users\user\PycharmProjects\wayne\work\test.log',encoding='utf-8')
fh.setLevel(logging.INFO)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
# formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)-8s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

# 记录一条日志
logger.info('foorbar')
try:
    print(1/0)
except Exception as e:
    logger.error(e)
try:
    print(1/0)
except Exception as e:
    logger.exception(e)
print(1)