# -*- coding:utf-8 -*-
import hashlib

# 1.创建一个hash对象
h = hashlib.sha256()
# 2.填充要加密的数据
passwordstr = '123456'
h.update(bytes(passwordstr, encoding='utf-8'))
# 3.获取加密结果
pawd_result = h.hexdigest()