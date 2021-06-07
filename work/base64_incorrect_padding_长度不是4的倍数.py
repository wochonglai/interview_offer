# -*- coding:utf-8 -*-
missing_padding = 4 - len(re_token) % 4
if missing_padding and missing_padding % 4 != 0:
    re_token += '=' * missing_padding

# 第二种方法
lens=len(strg)
lenx=lens-(lens%4 if lens%4 else 4)
try:
    result=base64.decodestring(strg[:lenx])
except:
    pass