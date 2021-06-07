# -*- coding:utf-8 -*-
import cx_Oracle

class baseUtilsX():
    def __init__(self):
        self.connectObj = ""
        self.connCnt = 0
        self.cursorCnt = 0

    def initOracleConnect(self):
        oracle_tns = cx_Oracle.makedsn('XXX.XXX.XXX.XXX', 1521, 'XX')
        if self.connCnt == 0:
            self.connectObj = cx_Oracle.connect('oracleUserName', 'password', oracle_tns)
            self.connCnt += 1

    def getOracleConnect(self):
        self.initOracleConnect()
        return self.connectObj

    def closeOracleConnect(self, connectObj):
        connectObj.close()
        self.connCnt -= 1

    def getOracleCursor(self):
        self.initOracleConnect()
        self.cursorCnt += 1
        return self.connectObj.cursor()

    def closeOracleCursor(self, cursorObj):
        cursorObj.close()
        self.cursorCnt -= 1
        if self.cursorCnt == 0:
            print
            "will close conn"
            self.closeOracleConnect(self.connectObj)

    def selectFromDbTable(self, sql, argsDict):
        # 将查询结果由tuple转为list
        queryAnsList = []
        selectCursor = self.getOracleCursor()
        selectCursor.prepare(sql)
        queryAns = selectCursor.execute(None, argsDict)
        for ansItem in queryAns:
            queryAnsList.append(list(ansItem))

        self.closeOracleCursor(selectCursor)
        return queryAnsList