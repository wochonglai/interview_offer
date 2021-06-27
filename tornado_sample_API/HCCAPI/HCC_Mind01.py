# -*- coding:utf-8 -*-
import tornado.web
import time,json,urllib.parse,datetime,traceback,calendar
from datetime import datetime
from apicommon.methods import *
from apicommon.sqlserver_py import Mssql
from apicommon.mysql_exc import Mysqlpython
from apscheduler.schedulers.tornado import TornadoScheduler
import pymongo
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

class BaseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(10)

# 提供MIND APP登录 MIND_APP_login MIND0003
class MIND_APP_login(tornado.web.RequestHandler):
    def post(self):
        self.set_header("Content-Type", "application/json; charset=utf-8")
        API_START = str(datetime.now())[:-3]
        starttime = time.time()
        sqlc = Mssql()  # 创建SQL连接实例
        try:
            rec = json.loads(urllib.parse.unquote(self.request.body.decode('utf-8')))
            # colLang = rec["colPara"]["lang"]
            userId = rec["userId"]
            userPwd = rec["userPwd"]
            deviceId=rec["deviceId"]
            model=rec["model"]
            brand = rec["brand"]
            os_type = rec["osType"]
            os_edition = rec["osEdition"]
            # 新建空字典，用来存储返回数据
            res = {}
            # 新建空字典result_d，用来存储res中键result对应的值
            result_d={}
            res['resultCode'] = 1
            res['errorMessage'] = None
            res['errorCode'] = None
            # password查询语句
            pd_sql = "select USER_PWD,DEVICE_ID,USER_NAME from DASHBOARD_APP_USER WHERE USER_ID='{}'".format(userId)
            pd=sqlc.all(pd_sql)
            login_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            update_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            update_by='000000'
            if not pd:
                res="用户不存在"
                response = json.dumps(res, ensure_ascii=False)
                self.write(response)
            else:
                if userPwd==pd[0][0]:
                    deviceId_l=[]
                    for i in pd:
                        deviceId_l.append(i[1])
                    # 如果deviceId已经在表里存在，则略过
                    if deviceId in deviceId_l:  # 需更新最后登录时间
                        pass
                    # 如果deviceId不存在需判断，一个人只能有最多两台设备
                    else:
                        if deviceId_l[0]==None: # 如果他从未录入deviceId
                            # 更新最后一次登录时间最久的
                            sql = "update DASHBOARD_APP_USER set DEVICE_ID='{}',MODEL='{}',BRAND='{}',OS_TYPE='{}',OS_EDITION='{}',LAST_LOGIN='{}',UPDATE_DATE='{}',UPDATE_BY='{}' where ID in (select top 1 ID " \
                                  "from DASHBOARD_APP_USER where USER_ID='{}' order by LAST_LOGIN)".format(deviceId,model,brand,os_type,os_edition,login_time,update_time,update_by,userId)
                            sqlc.exec(sql)
                        elif len(deviceId_l)<2:
                            sql = "insert into DASHBOARD_APP_USER(USER_ID,USER_NAME,USER_PWD,USER_TYPE,DEVICE_ID,MODEL,BRAND,OS_TYPE,OS_EDITION,DATE_JOINED," \
                                  "LOGIN_ERROR_COUNT,LAST_LOGIN,ACTIVE,ALIVE,CREATE_DATE,CREATE_BY,UPDATE_DATE,UPDATE_BY) " \
                                  "values('{}','{}','{}',2,'{}','{}','{}','{}','{}','{}',0,'{}',1,1,'{}','{}','{}','{}')".format(
                                userId,pd[0][2],userPwd,deviceId,model,brand,os_type,os_edition,login_time,login_time,update_time,update_by,update_time,update_by)
                            sqlc.exec(sql)
                        elif len(deviceId_l)==2:
                            sql = "update DASHBOARD_APP_USER set DEVICE_ID='{}',MODEL='{}',BRAND='{}',OS_TYPE='{}',OS_EDITION='{}',LAST_LOGIN='{}',UPDATE_DATE='{}',UPDATE_BY='{}' where ID in (select top 1 ID " \
                                  "from DASHBOARD_APP_USER where USER_ID='{}' order by LAST_LOGIN)".format(deviceId,model,brand,os_type,os_edition,login_time,update_time,update_by,userId)
                            sqlc.exec(sql)
                    result_d={}
                    result_d['userId']=userId
                    result_d['userName'] = pd[0][2]
                    result_d['campus'] = '龍華'
                    result_d['organization'] = '海納智聯SMT工業互聯網研究院'
                    res['result'] = result_d
                    response = json.dumps(res, ensure_ascii=False)
                    self.write(response)
                else:
                    res={"resultCode":0,"result":"False","errorMessage":"密码错误！","errorCode":"ER033"}
                    self.write(res)
        # 如果参数不全
        except Exception as e:
            res = {"resultCode": 0, "result": None, "errorMessage": "缺少必要參數", "errorCode": "ER001"}
            # response = json.dumps(res, ensure_ascii=False)
            self.write(res)
        finally:
            sqlc.close()

'''
MIND012  PPConsumedSpoiled 提供IDB及APP 调用所需的抛料率排行统计数据
'''
class PPConsumedSpoiled(BaseHandler):
    @run_on_executor
    @record_http_request
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")
        self.set_header("Content-Type", "application/json; charset=utf-8")
        # sqlc = Mssql()  # 创建SQL连接实例
        try:
            rec = json.loads(urllib.parse.unquote(self.request.body.decode('utf-8')))
            print(rec)
            action=rec["action"]    # 查询场景
            action_v = rec["action_value"]
            flag = rec["flag"]  # 查询参数，0为整体、1为料轨、2为料号、3为Feeder
            day_now = time.localtime()
            startTime =rec["startTime"] if rec["startTime"] else '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
            wday, monthRange = calendar.monthrange(day_now.tm_year,
                                                   day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
            endTime =rec["endTime"] if rec["endTime"] else '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)    # 月末日期
            theLimit=rec["theLimit"] if rec["theLimit"] else 5 #排名取前N，默认前5
            res = {}    # API response
            sqlc = Mysqlpython(host="10.134.103.247", db="smt_mind")
            '''查询场景1：某机台当月 料轨(或抛料率、或Feeder) 抛料率排行前N'''
            if action==1:
                sql_total=""
                if flag==0:
                    pass
                else:
                    sql_total = "select equipmentSN,flag,flagValue,sum(qtyUsed) qtyUsed_sum,sum(qtySpoiled) qtySpoiled_sum,sum(qtySpoiled)/sum(qtyUsed) attrition_rate from pp_consumedmaterials where " \
                                "equipmentSN='{}' and flag={} and intime>='{}' and intime<='{}' GROUP BY flagValue order by attrition_rate desc LIMIT 5".format(action_v,flag,startTime,endTime,theLimit)
                t_data = sqlc.all(sql_total)
                res["action"] = action
                res["action_value"] = action_v
                result_l = []
                number=0
                for i in t_data:
                    number+=1
                    redusl_d={}
                    redusl_d["number"] = number
                    redusl_d["flag"] = i[1]
                    redusl_d["flagValue"] = i[2]
                    redusl_d["qtyUsed"] = int(i[3])
                    redusl_d["qtySpoiled"] = int(i[4])
                    redusl_d["attrition_rate"] = float(i[5])
                    result_l.append(redusl_d)
                res["result"] = result_l
            # '''查询场景2：各机台当月抛料率排行前N'''
            elif action==2:
                sql_total = "select equipmentSN,sum(qtyUsed) qtyUsed_sum,sum(qtySpoiled) qtySpoiled_sum,sum(qtySpoiled)/sum(qtyUsed) attrition_rate from pp_consumedmaterials " \
                            "where flag=1 and intime>='{}' and intime<='{}' GROUP BY equipmentSN order by attrition_rate desc LIMIT {}".format(startTime,endTime,theLimit)
                t_data = sqlc.all(sql_total)
                res["action"] = action
                res["action_value"] = action_v
                result_l = []
                number=0
                for i in t_data:
                    number+=1
                    redusl_d={}
                    redusl_d["number"] = number
                    redusl_d["flag"] = 0
                    redusl_d["flagValue"] = i[0]
                    redusl_d["qtyUsed"] = int(i[1])
                    redusl_d["qtySpoiled"] = int(i[2])
                    redusl_d["attrition_rate"] = float(i[3])
                    result_l.append(redusl_d)
                res["result"] = result_l
            '''查询场景5：各线体当月抛料率排行前N'''
            '''查询场景6：某产线当月 料轨 抛料率排行前N'''
            '''查询场景7：某产线当月 料号 抛料率排行前N'''
            '''查询场景8：某产线当月 Feeder 抛料率排行前N'''
            '''查询场景9：当月 料轨 抛料率排行前N'''
            '''查询场景10：当月 料号 抛料率排行前N'''
            '''查询场景11：当月 Feeder 抛料率排行前N'''
            sqlc.close()
            res["resultCode"]=1
            res["errorCode"] = None
            res["errorMessage"] = None
            self.response_value=json.dumps(res, ensure_ascii=False)
            print(self.response_value)
            self.write(self.response_value)
        # 如果参数不全
        except:
            traceback.print_exc()
            res = {"resultCode": 0, "result": None,"statistic": None, "errorMessage": "参数错误", "errorCode": "ERR001"}
            self.response_value = json.dumps(res, ensure_ascii=False)
            self.write(self.response_value)

    def options(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST,GET")#,OPTIONS
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.set_status(204)
        self.finish()


# 专门用于测试，API
class GetTestAPI(BaseHandler):
    @run_on_executor
    @record_http_request
    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")
        self.set_header("Content-Type", "application/json; charset=utf-8")
        # sqlc = Mssql()  # 创建SQL连接实例
        try:
            rec = json.loads(urllib.parse.unquote(self.request.body.decode('utf-8')))
            print(rec)
            res={}
            res["resultCode"]=1
            self.response_value=json.dumps(res, ensure_ascii=False)
            print(self.response_value)
            self.write(self.response_value)
        # 如果参数不全
        except:
            traceback.print_exc()
            res = {"resultCode": 0, "result": None,"statistic": None, "errorMessage": "参数错误", "errorCode": "ERR001"}
            self.response_value = json.dumps(res, ensure_ascii=False)
            self.write(self.response_value)

    def options(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "*")
        self.set_header("Access-Control-Allow-Methods", "POST,GET")#,OPTIONS
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.set_status(204)
        self.finish()