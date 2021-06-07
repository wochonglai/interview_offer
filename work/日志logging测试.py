# -*- coding:utf-8 -*-
import logging,time
import logging.handlers


logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
fh = logging.handlers.TimedRotatingFileHandler(r'test_info.log',when='midnight', interval=1, backupCount=0, encoding='utf-8')  # windows
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s:,%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
# 给logger添加handler
logger.addHandler(fh)

while 1:
    logger.info("1")
    time.sleep(10)