#coding=utf-8

"""
@author: evilXu
@file: factor_data.py
@time: 2017/11/14 16:12
@description: 
"""

import pandas as pd
from datetime import datetime,date,timedelta
import shutil
import os

class JYData():
    def __init__(self,path="",jydb="", defaultInitDate = date(2010, 1, 1)):
        '''
        path，数据文件目录
        '''
        self._path = path
        self.jydb = jydb
        self._defaultInitDate = defaultInitDate
        self._create()
        self._names = set(['open','close','low','high','volume','amount'])

    def _create(self):
        if not os.path.exists(self._dataPath):
            os.mkdir(self._dataPath)

    def get_price(self,name):
        pass

    def updt_price(self):
        pass

    def updt_adj_price(self):
        pass


if __name__ == "__main__":
    obj = JYData("pe","E:\\evilAlpha\\test" )#)"Z:\\factor_datas"
    data = obj.load(datetime(2017, 1,25), datetime(2018, 12, 31))
    print(data)

    # obj = FactorData("testF1","E:\\evilAlpha\\rqalpha\\test")
    # print(obj.name)
    # import random
    # code_cnt = 3000
    # day_cnt = 20
    # df = pd.DataFrame([[random.random() for j in range(code_cnt)] for i in range(day_cnt)],
    #                   columns=list(["%06d.XSHE"%i for i in range(code_cnt)]),
    #                   index=[datetime(2015, 12, 1) + timedelta(days=i) for i in range(day_cnt)])
    # print(df.info())
    # # obj.reset()
    # obj.append(df)
    # # data = obj.load(datetime(2014,1,15),datetime(2017,12,31))
    # # print(data)