# -*- coding:utf-8 -*-
import jwt,base64

headers={
  "alg": "HS256",
  "typ": "JWT"
}
payload={"id":"121","name":"xiaochi","sub":"owner","iat":1616599532,"exp":1616599582}
sec='secretabcabcabcabcabcabcabcabcabcabcabcabcabc'

secret=base64.b64decode(sec)
encoded_jwt = jwt.encode(payload, secret, algorithm='HS256',headers=headers)
print(encoded_jwt)

# # 解密
# token='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMDAiLCJyb2xlcyI6IkJVU0lORVNTVVNFUiIsIm1vZGUiOiJzdG9yZWFwcCIsImlhdCI6MTQ5NDg1ODk4MCwiZXhwIjoxNDk0ODY0OTgwfQ.ckFnGv1NT-Ui2S90DNr50YoHSXc1ZLBNnEErnGMWL-E'
# secret='123456AB'
# payload_decoded=jwt.decode(token,base64.b64decode(secret),algorithms=["HS256"], options={ 'verify_exp': False})
# print(payload_decoded)

# # a="eyJpZCI6IjEyMSIsIm5hbWUiOiJ4aWFvY2hpIiwic3ViIjoib3duZXIiLCJpYXQiOjE2MTY1OTk1MzIsImV4cCI6MTYxNjU5OTU4Mn0=="
# # print(len(a),base64.b64decode(a)) #
# # 解密
# token='eyJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEyMSIsIm5hbWUiOiJ4aWFvY2hpIiwic3ViIjoib3duZXIiLCJpYXQiOjE2MTY1OTk1MzIsImV4cCI6MTYxNjU5OTU4Mn0.6_6jcY7Vm_1thyunWxezjxVMAlIoBrRK45woz6IVH2U'
# secret='secretabcabcabcabcabcabcabcabcabcabcabcabcabc'
# # payload_decoded=jwt.decode(token,base64.b64decode(secret),algorithms=["HS256"], options={ 'verify_exp': False})
# payload_decoded=jwt.decode(token,secret,algorithms=["HS256"], options={ 'verify_exp': False})
# print(payload_decoded)