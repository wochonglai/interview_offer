#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   security_util_AES.py
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/7 23:08   wayne      1.0         None
'''
'''
# 在Linux操作系统下，Python3的默认环境编码变为了utf-8编码，所以在编写代码的时候，字符串大部分都是以utf-8处理
UTF-8:
1byte = 8bit
1个英文字符 = 1byte
1个中文字符 = 3byte

128bit = 16byte = 16个英文字符
192bit = 24byte = 24个英文字符
256bit = 32byte = 32个英文字符

AES256概念
AES是一种对称加密算法，对称指加密和解密使用同一个密钥； 256指密钥的长度是256bit，即32个英文字符的长度；密钥的长度决定了AES加密的轮数

AES256加密参数
密钥： 一个32byte的字符串， 常被叫为key
明文： 待加密的字符串；字节长度(按byte计算)必须是16的整数倍，因此，明文加密之前需要被填充
模式： 加密模式，常用的有ECB、CBC；具体含义见参考链接
iv 偏移量： CBC模式下需要是16byte字符串； ECB下不需要
'''
"""
pip install pycryptodome
ord(): 返回对应字符的ascii码
chr(): 返回ascii码对应的字符， ascii码可以用十进制，也可以用十六进制
"""


import base64
from Crypto.Cipher import AES
from Crypto.Cipher.AES import MODE_CBC, MODE_ECB


PKCS7PADDING = 0
PKCS5PADDING = 1

BASE64 = 0
HEX = 1


class AesCrypto:
    def __init__(self, key, mode=MODE_ECB, padding=PKCS7PADDING, iv=None, encode_type=BASE64):
        """
        :param key: 密钥， 32byte=>256, 16byte=>128, 24byte=>192
        :param mode: 加密模式
        :param iv: 16byte 长度字符串
        :param padding: 填充方式
        :param encode_type: 输出格式
        """

        self.key = key.encode()
        self.mode = mode
        self.encode_type = encode_type
        self.iv = iv
        if self.iv:
            self.iv = self.iv.encode()

        if padding == PKCS7PADDING:
            self.padding_func = self.pkcs7padding
            self.unpadding_func = self.unpadding
        else:
            raise Exception('padding is invalid')

    def pkcs7padding(self, text:str, bs=16):
        """明文使用PKCS7填充 """
        remainder = bs - len(text.encode()) % bs
        padding_text = chr(remainder) * remainder
        return text + padding_text

    def unpadding(self, text):
        """ 去掉填充字符 """
        remainder = text[-1]
        padding_text = ord(remainder) * remainder
        return text.rstrip(padding_text)

    def encrypt(self, text):
        """ 加密 """
        text = self.padding_func(text)
        # 注意：加密中的和解密中的AES.new()不能使用同一个对象，所以在两处都使用了AES.new()
        kwargs = {
            'key': self.key,
            'mode': self.mode
        }
        if self.mode == MODE_CBC:
            kwargs['iv'] = self.iv
        text = AES.new(**kwargs).encrypt(text.encode())
        if self.encode_type == BASE64:
            return base64.b64encode(text).decode()

    def decrypt(self, text):
        """ 解密 """
        if self.encode_type == BASE64:
            text = base64.b64decode(text.encode())
        kwargs = {
            'key': self.key,
            'mode': self.mode
        }
        if self.mode == MODE_CBC:
            kwargs['iv'] = self.iv
        text = AES.new(**kwargs).decrypt(text)
        text = self.unpadding_func(text.decode())
        return text


# 异或运算 java Xor ^
a = 123
b = 34
c = a^b
print(c)

'''
AES
级加密标准（Advanced Encryption Standard，AES），是美国联邦政府采用的一种区块加密标准。这个标准用来替代原先的DES，
已经被多方分析且广为全世界所使用。经过五年的甄选流程，高级加密标准由美国国家标准与技术研究院（NIST）于2001年11月26日发布于FIPS PUB 197，
并在2002年5月26日成为有效的标准。2006年，高级加密标准已然成为对称密钥加密中最流行的算法之一。
AES只是个基本算法，实现AES有若干模式。其中的CBC模式因为其安全性而被TLS（就是https的加密标准）和IPSec（win采用的）作为技术标准。简单地说，
CBC使用密码和salt（起扰乱作用）按固定算法（md5）产生key和iv。然后用key和iv（初始向量，加密第一块明文）加密（明文）和解密（密文）。
PyCrypto是一个免费的加密算法库，支持常见的DES、AES加密以及MD5、SHA各种HASH运算。AES加密的初始密钥，根据AES规范，可以是16字节、
24字节和32字节长；其实完全可以由用户输入的口令+salt获得；iv，这里使用了Crypto模块中的Random模块，读取其16字节的数据作为iv的值，
AES的分块大小固定为16字节。
AES.new(key, AES.MODE_CBC,iv)函数，这步可以指定加密模式，这里选择的是CBC模式；data数据长度是否为16字节块的整数倍，
从而进行适当的Padding，这里的关键是利用'%'运算判断是否是16字节的整数倍，然后在尾部追加(16-x)个填充字符；生成的cipher对象的encrypt
方法加密数据，注意这里与iv进行了一次异或。
'''
# encoding:utf-8
import base64
from Crypto.Cipher import AES
from Crypto import Random


def encrypt(data, password):
    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    iv = Random.new().read(bs)
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data = cipher.encrypt(pad(data))
    data = iv + data
    return data


def decrypt(data, password):
    bs = AES.block_size
    if len(data) <= bs:
        return data
    unpad = lambda s: s[0:-ord(s[-1])]
    iv = data[:bs]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(data[bs:]))
    return data





if __name__ == '__main__':
    data = 'd437814d9185a290af20514d9341b710'
    password = '78f40f2c57eee727a4be179049cecf89'  # 16,24,32位长的密码
    encrypt_data = encrypt(data, password)
    encrypt_data = base64.b64encode(encrypt_data)
    print('encrypt_data:', encrypt_data)

    encrypt_data = base64.b64decode(encrypt_data)
    decrypt_data = decrypt(encrypt_data, password)
    print('decrypt_data:', decrypt_data)