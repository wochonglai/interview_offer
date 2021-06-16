#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   hash512_byte_array.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/9 22:24   wayne      cryptography-linux离线安装.0         None
'''
import hashlib
a = "拉风"
from array import array
print(array("b", a.encode("utf8")))
bb = bytearray(a,encoding='utf-8')
print(bb.decode("utf-8"))
print([x for x in bytearray(a,'utf_8')])

# java和python处理字节的方式不同，所以我对如何将byte []转换为python字符串感到有些困惑，我在Java中有这个byte []
b=[118, -86, -46, -63, 100, -69, -30, -102, -82, -44, -40, 92, 0, 98, 36, -94]
# str=""
# for i in b:
#     str=str+chr(abs(i))
'''
ava byte类型是一个有符号整数；该值的范围介于-128和127之间。Python的chr期望值介于0和255之间。在Java教程的“ 原始数据类型”部分中：
byte：字节数据类型是8位带符号的二进制补码整数。最小值为-128，最大值为127（含）。
您需要将2s补余转换为无符号整数：
'''
def twoscomplement_to_unsigned(i):
    return i % 256

result = bytes(map(twoscomplement_to_unsigned, b))
print(result)

def jb2pb(byte_arr):
     """
     java 字节数组转python字节数组
     :return:
     """
     return [i + 256 if i < 0 else i for i in byte_arr]
print(jb2pb(b))














































'''
场景是这个样子的,我这边要实现一个接口, 服务器端是java做的,客户端是python做的,服务器端向客户端提供了一个login的接口,
需要客户端实现,login需要给服务器返回一个byte[] 的值 ,但是python中貌似没有byte这个类型,我该怎么处理?
'''
import base64

"""
Some useful functions for interacting with Java web services from Python.
"""


def make_file_java_byte_array_compatible(file_obj):
    """
    Reads in a file and converts it to a format accepted as Java byte array
    :param file object
    :return string
    """
    encoded_data = base64.b64encode(file_obj.read())
    strg = ''
    for i in range((len(encoded_data) / 40) + 1):
        strg += encoded_data[i * 40:(i + 1) * 40]

    return strg


def java_byte_array_to_binary(file_obj):
    """
    Converts a java byte array to a binary stream
    :param java byte array as string (pass in as a file like object, can use StringIO)
    :return binary string
    """
    decoded_data = base64.b64decode(file_obj.read())
    strg = ''
    for i in range((len(decoded_data) / 40) + 1):
        strg += decoded_data[i * 40:(i + 1) * 40]

    return strg
