#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   PBKDF2.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/8 0:03   wayne      1.0         None
'''
import hashlib, binascii


def retrieve_data_from_database(user):
    """从数据库获取指定用户密码的PBKDF2哈希值，这里只是演示
    """
    data = {'yang': b'e75dfdc937acc5b7fccb2bc4237f75248c5bbe01797f70049be8abf43e55be44'}
    return data[user]


def validate_password(user, password):
    """验证密码是否正确
    password的PBKDF2哈希值和存储的PBKDF2哈希值比较，相同则验证通过
    """
    salt = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'
    dk = hashlib.pbkdf2_hmac('sha256', password, salt, 10000)
    saved_data = retrieve_data_from_database(user)
    return binascii.hexlify(dk) == saved_data


def login(user, password):
    """用户登录演示
    """
    if not validate_password(user, password):
        print('user or password error')
    # 其它逻辑