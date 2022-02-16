#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
https://stackoverflow.com/questions/64113853/converting-java-code-for-3des-encryption-with-md5-message-digest-and-desede-cbc
@File    :   des3_python.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/2/16 21:47   wayne      1.0         None
'''
import base64
# from Crypto.Cipher import AES
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
# import pyDes
# from Crypto import Random
import hashlib


def encrypt(message, passkey):
    # hash_object = hashlib.md5(passkey.encode("utf-8"))
    hash_object = hashlib.md5(passkey)
    digested_passkey = hash_object.digest()
    print("digested_passkey", digested_passkey)
    print("digested_passkey array", [i for i in digested_passkey])

    # key24 = "[:24]".format(digested_passkey)
    key24 = digested_passkey + digested_passkey[0:8]  # Derive key as in Java
    print("key24", key24)

    # des = pyDes.des(key24);                                # Remove pyDes

    # message = message.encode('utf-8')
    # message = message + (16 - len(message) % 16) * chr(16 - len(message) % 16)
    print("before pad", message)
    message = pad(message, 8)  # Use padding from PyCryptodome
    print("after pad", message)

    # iv = Random.new().read(AES.block_size)                 # For Java code compliance: Use 0-IV
    iv = bytes.fromhex('0000000000000000')

    # cipher = AES.new(des, AES.MODE_CBC, iv)                # For Java code compliance: Use TripleDES
    cipher = DES3.new(key24, DES3.MODE_CBC, iv)

    # return base64.b64encode(iv + cipher.encrypt(message))  # For Java code compliance: Don't concatenate IV and ciphertext
    return base64.b64encode(cipher.encrypt(message))


# print(encrypt('aug@2019', 'Lgp!kdao2020'))                 # Better: Pass binary data
print(encrypt(b'123456789123456789123456789123456789123456789', b'Lgp!kdao2020'))