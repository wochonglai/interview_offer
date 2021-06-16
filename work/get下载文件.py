# -*- coding:utf-8 -*-
import requests

url = 'http://10.157.10.113:5110/common/download'
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {"filename":"Z3JvdXAyL00wMC8wMC9ENS9DcDBLczEyZWRleUFKald4QUFQS3hNcjVWam84OTQ=-1324119016635_20191010080122_FAIL.zip"}
url2='http://10.157.10.113:5110/common/download?filename=Z3JvdXAyL00wMC8wMC9ENS9DcDBLczEyZWRleUFKald4QUFQS3hNcjVWam84OTQ=-1324119016635_20191010080122_FAIL.zip'
# response = requests.post(url, data=data, headers=headers)
response = requests.get(url, params=data, headers=headers)
for i in response.iter_content(chunk_size=1024):
    print(i)
# print(response.status_code)
print(response.text)
# response.json()['content']
print(response.json())

response2=requests.get(url2,headers=headers)
print(response2)
with open("cryptography-linux离线安装.zip","wb") as f:
    for i in response2.iter_content(chunk_size=1024):
        if i:
            f.write(i)