#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   str_bytes_bytearray.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/9 23:22   wayne      1.0         None
'''
'''
首先str是采用Unicode编码方式的序列，主要用于显示。
而bytes是字节序列，主要用于网络和文件传输。
bytearray和bytes是一样的，只是它是可变的，它们的关系和str与list类似。
在aes解密或者网络数据中，数据应该是bytes或bytearray。
str和bytes的相互转化就是编码和解码。'''


# str——》bytes
str = "aabbcc"
bytes = str.encode('utf-8')

print(str)  # aabbcc
print(bytes)    # b'aabbcc'

# 更简单的方式是使用b声明是bytes
bytes = b'aabbcc'

# bytes——》str
bytes = b"aabbcc"
str = bytes.decode('utf-8')
print(bytes)    # b'aabbcc'
print(str)  # aabbcc

# bytes和str转化为bytearray都依赖于bytearray函数

# bytes——》bytearray
bytes = b"aabbcc"
byarray = bytearray(bytes)

print(byarray)  # bytearray(b'aabbcc')

# str——》bytearray
str = "aabbcc"
byarray = bytearray(str)

print(byarray)  # bytearray(b'aabbcc')

# 常见的网络传输时，有hex字符串转为bytearray的需求可以使用bytearray.fromhex()，这时是不需要编码的。

hexstr = "098811"
byarray = bytearray.fromhex(hexstr)
print(byarray)  # bytearray(b'\t\x88\x11')
# 注意到长度减半！！！！！

# bytearray——》str
# bytes
# bytearray转为str和bytes
# 依赖于解码和bytes函数

byarray = bytearray("aabbcc", encoding='utf-8')
str = byarray.decode('utf-8')
bytes = bytes(byarray)
print(byarray)  # bytearray(b'aabbcc')
print(str)  # aabbcc
print(bytes)    # b'aabbcc'