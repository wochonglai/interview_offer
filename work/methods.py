# -*- coding:utf-8 -*-
# 日期格式转换  年/月 ——年/月/日 HH：MM 不区分闰年（二月都是28号）用于月初
import time,json,datetime
import base64
import hmac
import subprocess
import pika
from pika.exceptions import ChannelClosed
from pika.exceptions import ConnectionClosed
from functools import wraps
# from .sqlserver_py import Mssql

def record_http_request(func):
    @wraps(func)
    def record(self, *args, **kwargs):
        request_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        response = func(self, *args, **kwargs)
        http_request = dict(
            request_time=request_time,
            expend_time=self.request.request_time(),
            request_text=self.request.body.decode('utf-8'),
            response_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            request_ip=self.request.remote_ip,
            method=self.request.method,
            url=self.request.uri,
            request_params=self.request.arguments,
            response_code=self.get_status(),
            response_text=self.response_value,
        )
        with open('mind_request-%s.log'%request_time[:10], 'a', encoding='utf-8') as f:
            f.write(str(http_request)+ '\n')
        return response

    return record

'''把时间戳转化为时间: 1479264792 to 20161116 00:00:00'''
def tStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)

def send_msg(send_type, userIds, msg):
    sqlc = Mssql()  # 创建SQL连接实例
    try:
        if send_type == 0:  # 群发
            send_time=time.time()
            id=int(float('%.3f'%send_time)*1000)
            msg['id']=id
            msg['senderType'] = send_type
            msg['sender'] = 'SYSTEM'
            msg['senderTime'] = tStampToTime(send_time)
            m = RabbitMQ_fanout()
            m.start_publish(msg)  # msg为字典，发出为json
            # 信息发送log
            sql = "insert into IDB_MSG_LOG(ID,SENDER_TYPE,SENDER,RECEIVER,MSG_HEAD,MSG_TYPE,MESSAGE,SENDER_TIME) values({},0,'SYSTEM','ALL','{}','{}','{}','{}')".format(
                id,msg["msgHead"], msg["msgType"], msg["message"], msg['senderTime'])
            sqlc.exec(sql)
        elif send_type == 1:  # 单发
            if userIds.split(";"):
                if len(userIds.split(";")) > 1:
                    sql = "select USER_ID,DEVICE_ID from DASHBOARD_APP_USER where USER_ID in {}".format(
                        tuple(userIds.split(";")))
                    deviceId_l = sqlc.all(sql) if sqlc.all(sql) else []
                else:
                    sql = "select USER_ID,DEVICE_ID from DASHBOARD_APP_USER where USER_ID='{}'".format(
                        userIds.split(";")[0])
                    deviceId_l = sqlc.all(sql) if sqlc.all(sql) else []
                for i in deviceId_l:
                    send_time = time.time()
                    id = int(float('%.3f' % send_time) * 1000)
                    msg['id'] = id
                    msg['senderType'] = send_type
                    msg['sender'] = 'SYSTEM'
                    msg['senderTime'] = tStampToTime(send_time)
                    m = RabbitMQ_one()
                    m.start_publish(i[1], msg)
                    # 信息发送log
                    update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    sql = "insert into IDB_MSG_LOG(ID,SENDER_TYPE,SENDER,RECEIVER,DEVICE_ID,MSG_HEAD,MSG_TYPE,MESSAGE,SENDER_TIME) values({},1,'SYSTEM','{}','{}','{}','{}','{}','{}')".format(id,
                        i[0], i[1], msg["msgHead"], msg["msgType"], msg["message"], msg['senderTime'])
                    sqlc.exec(sql)
    except:
        raise Exception
    finally:
        sqlc.close()

'''
推播 RabbitMQ
'''
# rabbitmq 配置信息
MQ_CONFIG = {
    "host": "10.134.103.241",
    # "host":"127.0.0.1",
    "port": 5672,
    "vhost": "/",
    "user": "mind_other01",
    "passwd": "Mind_other2019",
    "fanout_ex": "fanout_ex",
    "direct_ex":"direct_ex",
    "topic_ex":"f20_machine"
}

# 用于请求amqp APi 请求获取某exchangeName的所有routing_key列表
def get_bindings(exchangeName):
    command = 'curl -u %s:%s http://10.134.103.241:15672/api/bindings' % (MQ_CONFIG['user'], MQ_CONFIG['passwd'])
    result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # print(json.loads(result.stdout.readlines()[3].decode('utf-8')))
    r = []
    bindings = []
    try:
        r = json.loads(result.stdout.readlines()[3].decode('utf-8'))
    except IndexError as e:
        pass
    try:
        for line in r:
            if line['source']==exchangeName:
                bindings.append(line['routing_key'])
    except KeyError as e:
        pass
    return bindings

'''把时间戳转化为时间: 1479264792 to 20161116'''
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y%m%d', timeStruct)


def T2TStamp(timestr):
  a = timestr.replace("T", " ").split('.')
  timeArray = time.strptime(a[0], "%Y-%m-%d %H:%M:%S")
  timeStamp = int(time.mktime(timeArray))
  b = int(a[1].split('+')[0]) / 1000
  return timeStamp + b

# 将'2018-11-26 11:25:00'转为时间戳
def TStamp(timestr):
  timeArray = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
  return int(time.mktime(timeArray))

def generate_token(userId, key, create_time,expire=3600):
    r'''
    @Args:
     key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
     expire: int(最大有效时间，单位为s)
    @Return:
     state: str
    '''
    ts_str = str(create_time + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    token = str(userId)+':'+ts_str + ':' + sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")

# 列表统计，分成n份，返回每份区间数量
def statistic_list(l,n):
    from itertools import groupby
    result = []
    try:
        ll = (max(l)-min(l))/n
        d={}
        for k, g in groupby(sorted(l), key= lambda x:int((x-min(l))/ll)):
            d[k] = len(list(g))
        for i in range(n):
            if i not in d:
                result.append(((i+1)*ll+min(l),0))
            else:
                result.append(((i + 1) * ll + min(l), d[i]))
        result[n-1]=(max(l),1)
        return result
    # 如果列表中值均相等
    except:
        return [(max(l),len(l))]


def certify_token(token,token1,expireTime):
    if T2TStamp(expireTime) < time.time():
    # token expired
        return False
    if token != token1:
    # token certification failed
        return False
    # token certification success
    return True

def ym_ymd1(a):
    return a+"/1 00:00:00.000"

# 日期格式转换  年/月 ——年/月/日 HH：MM 不区分闰年（二月都是28号）用于月末
def ym_ymd2(a):
    l = a.split("/")
    if l[1] in ["1","3","5","7","8","10","12"]:
        l.append("31 23:59:59.999")
        return '/'.join(l)
    elif l[1] =="2":
        l.append("28 23:59:59.999")
        return '/'.join(l)
    else:
        l.append("30 23:59:59.999")
        return '/'.join(l)

# 获取当月有多少天，传入年，月
def m_days(month,year="2018"):
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month ==2:
        # 2月需要判断是否是闰年
        if ((year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)):
            return 29
        else:
            return 28
    else:
        return 30

# 返回一个列表中的项与另一个值相等的索引
def indexx(a,b):
    for i in range(len(a)):
        if a[i]["campusCode"] == b["campusCode"]:
            return i
def indexy(a,b):
    for i in range(len(a)):
        if b["corpList"][0]["corpId"] == a[i]["corpId"]:
            return i


class RabbitMQ_fanout(object):
    def __init__(self):
        self.exchange = MQ_CONFIG.get("fanout_ex")
        self.connection = None
        self.channel = None

    def reconnect(self):
        try:

            if self.connection and not self.connection.is_closed:
                self.connection.close()

            credentials = pika.PlainCredentials(MQ_CONFIG.get("user"), MQ_CONFIG.get("passwd"))
            parameters = pika.ConnectionParameters(MQ_CONFIG.get("host"), MQ_CONFIG.get("port"), MQ_CONFIG.get("vhost"),
                                                   credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.exchange, exchange_type="fanout",durable=True)
        except Exception as e:
            print(e)

    def start_publish(self,msg):
        self.reconnect()
        message = dict_to_json(msg)
        try:
            self.channel.basic_publish(exchange=self.exchange, routing_key="", body=message)
        except ConnectionClosed as e:
            self.reconnect()
        except ChannelClosed as e:
            self.reconnect()
        except Exception as e:
            self.reconnect()


class RabbitMQ_one(object):
    def __init__(self):
        # self.exchange = MQ_CONFIG.get("direct_ex")
        self.connection = None
        self.channel = None

    def reconnect(self,queue):
        try:

            if self.connection and not self.connection.is_closed:
                self.connection.close()

            credentials = pika.PlainCredentials(MQ_CONFIG.get("user"), MQ_CONFIG.get("passwd"))
            parameters = pika.ConnectionParameters(MQ_CONFIG.get("host"), MQ_CONFIG.get("port"), MQ_CONFIG.get("vhost"),
                                                   credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue, durable=True)
        except Exception as e:
            print(e)

    def start_publish(self,queue,msg):
        self.reconnect(queue)
        message = dict_to_json(msg)
        try:
            self.channel.basic_publish(exchange="", routing_key=queue, body=message)
        except ConnectionClosed as e:
            self.reconnect(queue)
            self.channel.basic_publish(exchange="", routing_key=queue, body=message)
        except ChannelClosed as e:
            self.reconnect(queue)
            self.channel.basic_publish(exchange="", routing_key=queue, body=message)
        except Exception as e:
            self.reconnect(queue)
            self.channel.basic_publish(exchange="", routing_key=queue, body=message)


class RabbitMQ_topic(object):
    def __init__(self):
        self.exchange = MQ_CONFIG.get("topic_ex")
        self.connection = None
        self.channel = None

    def reconnect(self,queue):
        try:

            if self.connection and not self.connection.is_closed:
                self.connection.close()

            credentials = pika.PlainCredentials(MQ_CONFIG.get("user"), MQ_CONFIG.get("passwd"))
            parameters = pika.ConnectionParameters(MQ_CONFIG.get("host"), MQ_CONFIG.get("port"), MQ_CONFIG.get("vhost"),
                                                   credentials)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue, durable=False)
            self.channel.exchange_declare(exchange=self.exchange,exchange_type='topic')  # 创建模糊匹配类型的exchange。。
            self.channel.queue_bind(exchange=self.exchange,queue=queue,routing_key=queue)

        except Exception as e:
            print(e)

    def start_publish(self,queue,msg):
        self.reconnect(queue)
        message = dict_to_json(msg)
        try:
            self.channel.basic_publish(exchange=self.exchange, routing_key=queue, body=message)
        except ConnectionClosed as e:
            self.reconnect(queue)
            self.channel.basic_publish(exchange=self.exchange, routing_key=queue, body=message)
        except ChannelClosed as e:
            self.reconnect(queue)
            self.channel.basic_publish(exchange=self.exchange, routing_key=queue, body=message)
        except Exception as e:
            self.reconnect(queue)
            self.channel.basic_publish(exchange=self.exchange, routing_key=queue, body=message)


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def dict_to_json(po):
    jsonstr = json.dumps(po, ensure_ascii=False, cls=CJsonEncoder)
    return jsonstr


def json_to_dict(jsonstr):
    if isinstance(jsonstr, bytes):
        jsonstr = jsonstr.decode("utf-8")
    d = json.loads(jsonstr)
    return d

# 两个时间比较，目前取得是差异30分钟
def time_compare(nowTime,t,setTime):
    try:
        if time.mktime(time.strptime(nowTime, "%Y-%m-%d %H:%M:%S"))-time.mktime(time.strptime(t.replace("/","-").replace("T"," ")[:19], "%Y-%m-%d %H:%M:%S"))<(setTime*60):
            return 1
        else:
            return 2
    except:
        return 2

if __name__ == '__main__':
    # a=RabbitMQ_fanout()
    # a.start_publish('OK')
    # a=RabbitMQ_one()
    # a.start_publish('G1670004','OK')
    RabbitMQ_topic().start_publish("TRI_test","123456")