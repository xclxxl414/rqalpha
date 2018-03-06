#coding=utf-8

"""
@author: evilXu
@file: JYUtils.py
@time: 2018/3/6 11:21
@description: 
"""
from .singleton import singleton

@singleton
class JYUtils():
    def __init__(self,dbConnStr="DRIVER={MYSQL};SERVER=172.18.44.231,3306;DATABASE=JYDB;UID=quant1;PWD=quant1@591"):
        self._dbConnStr = dbConnStr
        #TODO create connection
        #TODO load secuCode

    def codeConvert(self,innercode):
        #TODO
        pass

if __name__ == "__main__":
    #usage
    dbConnStr = ""
    JYUtils(dbConnStr).codeConvert()
