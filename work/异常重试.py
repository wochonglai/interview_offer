# -*- coding:utf-8 -*-
import time

# 常规方法
attempts = 0
success = False
while attempts < 3 and not success:
    try:
        # crawl_page(url)
        1/0
        success = True
    except:
        attempts += 1
        time.sleep(1)
        if attempts == 3:
            break
print(2)

# retrying库或者rety库