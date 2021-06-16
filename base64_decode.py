# -*- coding: utf-8 -*-
import base64
# with open(r"C:\Users\Wayne-PC\PycharmProjects\waynePy\Thingworx\heatmap\spi_scatter1.jpg","rb") as f:
# # b64encode是编码，b64decode是解码
#     base64_data = base64.b64encode(f.read())
# # base64.b64decode(base64data)
#     print(base64_data)
#     print(base64_data.decode('utf-8'))
#     print(type(base64_data.decode('utf-8')))
aa=b'\x00Sw\xb0\x00\x00\x01~{"MessageName":"CFX.EndpointConnected","Version":"cryptography-linux离线安装.0","TimeStamp":"2019-11-21T17:26:05.6373601+08:00","UniqueID":"deec15e8-a7a3-45c8-bf60-e2bbd7290f81","Source":"Panasonic.NPMDX1","Target":"MES.NPMDX1","RequestID":null,"MessageBody":{"CFXHandle":"Panasonic.NPMDX1","RequestNetworkUri":"amqp://haina_mind02:goodluck@6805ca667e5c:6007/","RequestTargetAddress":"/queue/Pana_receive"}}'
missing_padding = 4 - len(aa) % 4
print(missing_padding)
a=base64.b64decode(aa+b'='*missing_padding)
print(a)

bb=b"AFN3sAAAAip7Ik1lc3NhZ2VOYW1lIjoiQ0ZYLkhhaU5hLlByb2dyYW1Jbml0aWFsaXplZCIsIlZlcnNpb24iOiIxLjEiLCJUaW1lU3RhbXAiOiIyMDE5LTExLTEyVDE2OjM4OjAxLjUxMTcxODcrMDg6MDAiLCJVbmlxdWVJRCI6IjA0NzA4NjgxLTg2MjEtNDlkYi1hZDk4LWRkZWFmNTE4YmE0NCIsIlNvdXJjZSI6IkNGWC5TTVQuUHJpbnRlciIsIlRhcmdldCI6bnVsbCwiUmVxdWVzdElEIjpudWxsLCJNZXNzYWdlQm9keSI6eyJNZXNzYWdlQ29uZmlnIjp7IkhhbmRsZXIiOiJDRlguU01ULlByaW50ZXIiLCJSZXF1ZXN0TmV0d29ya1VyaSI6ImFtcXA6Ly9na2ctUEMvIiwiUmVxdWVzdFRhcmdldEFkZHJlc3MiOm51bGx9LCJFcXVpcG1lbnRJbmZvIjp7IkVxdWlwbWVudElQIjoiMTkyLjE2OC4xMDMuNjAiLCJMaW5lSUQiOiJGMjAiLCJNb2RlbE5hbWUiOiJHVCsiLCJCcmFuZE5hbWUiOiJHS0ciLCJNQUNBZGRyZXNzIjoiQzQtMDAtQUQtMkItQ0YtRTgiLCJFcXVpcG1lbnRTTiI6IkdMMDMwIn0sIkhlcm1lc0luZm9ybWF0aW9uIjp7IkVuYWJsZWQiOiJPRkYiLCJWZXJzaW9uIjoiMS4xIn19fQ=="
missing_padding = 4 - len(bb) % 4
print(missing_padding)
b=base64.b64decode(bb+b'='*missing_padding)
print(b)

print(base64.b64encode(b))
# missing_padding = 4 - len(re_token) % 4
# if missing_padding and missing_padding % 4 != 0:
#     re_token += '=' * missing_padding
'''
Python中将base64转为opencv的Mat格式
import cv2
import base64
imgData = base64.b64decode(base64_data)
nparr = np.fromstring(imgData, np.uint8)
img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#cv2.imshow("test",img_np)
#cv2.waitKey(0)

Python中将opencv的Mat格式转为base64
import cv2
import base64
imgData = base64.b64decode(base64_data)
nparr = np.fromstring(imgData, np.uint8)
img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

image = cv2.imencode('.jpg', img_np)[cryptography-linux离线安装]
base64_data = str(base64.b64encode(image))[2:-cryptography-linux离线安装])
'''