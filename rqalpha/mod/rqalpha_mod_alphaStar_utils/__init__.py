#coding=utf-8

"""
@author: evilXu
@file: __init__.py.py
@time: 2018/2/28 16:58
@description: 
"""

def load_mod():
    from .mod import UtilsMod
    return UtilsMod()

import datetime as dt
import pandas as pd

class BaseClass_Factor():
    def __init__(self):
        self.datetostr = lambda x: dt.datetime.strftime(x, '%Y-%m-%d')

    def getDBengine(self):
        import sqlalchemy
        cnnConf = {"host": "172.18.44.231", "port": 3306, "db": "jydb", "user": "quant1", "passwd": "quant1@591"}
        connStr = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (
        cnnConf.get("user"), cnnConf.get("passwd"), cnnConf.get("host"), cnnConf.get("port"), cnnConf.get("db"))
        engine = sqlalchemy.create_engine(connStr)
        self.engine=engine



    def getTradingDay(self):
        print('loading tradingdate')
        rawdata = pd.read_sql("select * from qt_tradingdaynew", self.engine)
        tradingday = rawdata[(rawdata.IfTradingDay == 1) & (rawdata.SecuMarket == 83)]
        # tradingday.to_pickle(rawdatapath + 'tradingdate.pkl')
        tradingdate = tradingday.TradingDate.sort_values()
        self.tradingdate = pd.Series(data=tradingdate.values, index=tradingdate.values)
        self.dateTrans = lambda x, offset=0: self.tradingdate.index[
            self.tradingdate.index.get_loc(x) + offset] if x in self.tradingdate.index else self.tradingdate.index[
            self.tradingdate.index.get_loc(x, method='bfill')]

    def getSecID(self):
        print('loading sec id')
        rawdata = pd.read_sql("select * from secumain", self.engine)
        AshareData = rawdata[(rawdata.SecuCategory == 1) & (rawdata.ListedSector.isin([1, 2, 6])) & (
            rawdata.ListedState.isin([1, 3, 5]))]
        self.codeRef = AshareData[['InnerCode', 'CompanyCode', 'SecuCode']].set_index('InnerCode')
        self.innercodeTrans = lambda x: self.codeRef.loc[x, 'SecuCode']+'.XSHG' if int(
            self.codeRef.loc[x, 'SecuCode']) >= 600000 else self.codeRef.loc[x, 'SecuCode']+'.XSHE'
        self.innercodeTransInv = lambda x: self.codeRef.loc[self.codeRef.SecuCode == x[-6:]].index[0]
        self.cmpycodeTrans = lambda x: (self.codeRef.loc[self.codeRef.CompanyCode == x, 'SecuCode']+'.XSHG' if int(
            self.codeRef.loc[self.codeRef.CompanyCode == x, 'SecuCode']) >= 600000 else self.codeRef.loc[
            self.codeRef.CompanyCode == x, 'SecuCode']+'.XSHE').values[0]
        self.innercode = self.codeRef.index
        self.secucode = self.codeRef.SecuCode.values
        self.cmpycode = self.codeRef.CompanyCode.values

