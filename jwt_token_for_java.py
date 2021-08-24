#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   jwt_token_for_java.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/24 21:18   wayne      1.0         None
'''
from array import array

java_token = "eyJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEyMSIsIm5hbWUiOiJ4aWFvY2hpIiwic3ViIjoib3duZXIiLCJpYXQiOjE2Mjk4MTA5ODIsImV4cCI6MTYyOTgxMTAzMn0.tWUFqdtM7BCxKp4eupKQ8TYTjdFtjr6feRMoTCE-Lfo"
secret = "secretabcabcabcabcabcabcabcabcabcabcabcabcabc"
'''
secret = "secretabcabcabcabcabcabcabcabcabcabcabcabcabc"

Java
import  java.io.UnsupportedEncodingException;
import javax.xml.bind.DatatypeConverter;
// byte[]转base64
String base64Str = DatatypeConverter.printBase64Binary(byteArray);
// base64转byte[]
byte [] byteArray = DatatypeConverter.parseBase64Binary(base64Str);

byte[] apiKeySecretBytes = DatatypeConverter.parseBase64Binary(secret);
        System.out.println(Arrays.toString(apiKeySecretBytes));
         [-79, -25, 43, 122, -42, -101, 113, -90, -36, 105, -73, 26, 109, -58, -101, 113, -90, -36, 105, -73, 26, 109, -58, -101, 113, -90, -36, 105, -73, 26, 109, -58, -101]
Java 转为Bytes，怎样与Python互转？？？？

secret_python_array = [i + 256 if i < 0 else i for i in secret_java_array]
secret_python_array = [177, 231, 43, 122, 214, 155, 113, 166, 220, 105, 183, 26, 109, 198, 155, 113, 166, 220, 105, 183, 26, 109, 198, 155, 113, 166, 220, 105, 183, 26, 109, 198, 155]
print(secret_python_array)
bytes(secret_python_array)
Out[16]: b'\xb1\xe7+z\xd6\x9bq\xa6\xdci\xb7\x1am\xc6\x9bq\xa6\xdci\xb7\x1am\xc6\x9bq\xa6\xdci\xb7\x1am\xc6\x9b'

Optional altchars must be a bytes-like object or ASCII string of length 2
    which specifies the alternative alphabet used instead of the '+' and '/'
    characters.
base64.b64decode(secret+'+++')  # 注意这儿与base64加=不一样，需要加+或者/
Out[74]: b'\xb1\xe7+z\xd6\x9bq\xa6\xdci\xb7\x1am\xc6\x9bq\xa6\xdci\xb7\x1am\xc6\x9bq\xa6\xdci\xb7\x1am\xc6\x9bs\xef\xbe'
然后需要去掉最后多加的3位list(b'\xb1\xe7+z\xd6\x9bq\xa6\xdci\xb7\x1am\xc6\x9bq\xa6\xdci\xb7\x1am\xc6\x9bq\xa6\xdci\xb7\x1am\xc6\x9bs\xef\xbe')[:-3]
'''
secret_java_array = [-79, -25, 43, 122, -42, -101, 113, -90, -36, 105, -73, 26, 109, -58, -101, 113, -90, -36, 105, -73,
                     26, 109, -58, -101, 113, -90, -36, 105, -73, 26, 109, -58, -101]
secret_python_array = [i + 256 if i < 0 else i for i in secret_java_array]
secret_python_array = [177, 231, 43, 122, 214, 155, 113, 166, 220, 105, 183, 26, 109, 198, 155, 113, 166, 220, 105, 183,
                       26, 109, 198, 155, 113, 166, 220, 105, 183, 26, 109, 198, 155]
print(secret_python_array)
# z = array(secret_python_bytes)
# print(z)

import jwt
import base64

print(jwt.decode(java_token, bytes(secret_python_array), algorithms='HS256', options={'verify_exp': False}))


def get_parseBase64Binary(input_str):
    missing_padding = 4 - len(input_str) % 4
    print("missing_padding:", missing_padding)
    if missing_padding == 4:
        return base64.b64decode(input_str)
    else:
        input_str_2 = input_str + missing_padding * "+"
        print(base64.b64decode(input_str_2))
        return base64.b64decode(input_str_2)[:-missing_padding]


print(get_parseBase64Binary(secret))
print(jwt.decode(java_token, get_parseBase64Binary(secret), algorithms='HS256', options={'verify_exp': False}))
secret2 = "secretabcabcabcabcabcabcabcabcabcabcabcabcabcabc"
print(get_parseBase64Binary(secret2))
java_token2 = "eyJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEyMSIsIm5hbWUiOiJ4aWFvY2hpIiwic3ViIjoib3duZXIiLCJpYXQiOjE2Mjk4MjMxNjgsImV4cCI6MTYyOTgyMzIxOH0.mAeKmWaiHP3bLqgPoph9J-0DuRaDkegp4UtK3CkZkkM"
print(jwt.decode(java_token2, get_parseBase64Binary(secret2), algorithms='HS256', options={'verify_exp': False}))
print(jwt.decode(java_token2, get_parseBase64Binary(secret2), algorithms='HS256'))

# import jwt
# import base64
# token='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMDAiLCJyb2xlcyI6IkJVU0lORVNTVVNFUiIsIm1vZGUiOiJzdG9yZWFwcCIsImlhdCI6MTQ5NDg1ODk4MCwiZXhwIjoxNDk0ODY0OTgwfQ.ckFnGv1NT-Ui2S90DNr50YoHSXc1ZLBNnEErnGMWL-E'
# secret ='123456AB'
# # jwt.decode(token,secret,algorithms='HS256')
# print(jwt.decode(token,base64.b64decode(secret),algorithms='HS256',options={ 'verify_exp': False}))
