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

class FactorData():
    def __init__(self,fname,path="",defaultInitDate = date(1990,1,1)):
        '''
        每年一个文件
        path， 因子数据文件目录
        '''
        # print("FactorData",path,fname)
        self._factorPath = os.path.join(path,fname)
        self._name = fname
        self._defaultInitDate = defaultInitDate if defaultInitDate is not None else date(1990,1,1)
        self.create()

    @property
    def name(self):
        return self._name

    def create(self):
        if not os.path.exists(self._factorPath):
            os.mkdir(self._factorPath)

    def reset(self):
        if os.path.exists(self._factorPath):
            shutil.rmtree(self._factorPath)
            os.mkdir(self._factorPath)

    def getLatestDate(self):
        df = pd.DataFrame()
        _fileList = []
        for i in os.listdir(self._factorPath):
            _absPath = os.path.join(self._factorPath, i)
            if os.path.isfile(_absPath):
                _fileList.append(_absPath)
        _fileList = sorted(_fileList)  # 按时间顺序取数据
        if len(_fileList) > 0:
            df1 = pd.read_hdf(_fileList[-1])
            return df1.index[-1].date()
        else:
            return self._defaultInitDate

    def load(self,startDt = None,endDt = None):
        df = pd.DataFrame()
        if startDt is None or endDt is None:
            return df
        _fileList = []
        _startDt = startDt
        _endDt = endDt
        _startYear = str(_startDt.year)
        _endYear = str(_endDt.year)
        for i in os.listdir(self._factorPath):
            _absPath = os.path.join(self._factorPath, i)
            if os.path.isfile(_absPath) and i >= _startYear and i<= _endYear:
                _fileList.append(_absPath)
        _fileList = sorted(_fileList) # 按时间顺序取数据
        for _file in _fileList:
            df1 = pd.read_hdf(_file)
            df = df.append(df1)
        return df.loc[_startDt:_endDt]

    def append(self,datas=pd.DataFrame()):
        if len(datas) < 1:
            return
        a = datas.index
        _lastYear = a[0].year
        years = [_lastYear]
        idxs = [0]
        _idx = 0
        for day in a[1:]:
            _idx += 1
            if day.year != _lastYear:
                idxs.append(_idx)
                years.append(day.year)
                _lastYear = day.year
        idxs.append(len(a))
        # print(idxs, years)
        for i in range(len(years)):
            self._appendAyear(years[i],datas.iloc[idxs[i]:idxs[i + 1]])

    def _appendAyear(self, year, datas=pd.DataFrame()):
        if len(datas) < 1:
            return
        _file = os.path.join(self._factorPath, str(year))
        if os.path.exists(_file):
            df = pd.read_hdf(_file)
            df = df.append(datas, verify_integrity=True)
            df.to_hdf(_file,key="root", mode='w')
        else:
            datas.to_hdf(_file,key="root", mode='w')
        return

class DependingData():
    def __init__(self,ucontext):
        self._ucontext = ucontext
        self.dependency = set(ucontext.dependency)

    def getDependingData(self,fname,startdt,enddt):
        if fname not in self.dependency:
            raise NotImplementedError(" not regiester as dependency")
        modconfig = self._ucontext.modconfig
        return FactorData(fname=fname,path=modconfig.factor_data_path,defaultInitDate=modconfig.factor_data_init_date)\
            .load(startdt,enddt)

class FactorDataInterface():
    '''
    API getFactor的实现
    '''
    def __init__(self,path="",defaultInitDate=datetime(2017, 1, 1).date(),endDt = datetime.now().date()):
        self._path = path
        self._defaultInitDate = defaultInitDate
        self._startDt_cache = self._defaultInitDate
        self._endDt_cache = endDt
        self._datas = {}

    def getData(self,fname="",startDt=None,endDt=None):
        if fname in self._datas:
            return self._datas.get(fname).loc[startDt:endDt]
        else:
            datas = FactorData(fname,self._path,self._defaultInitDate).load(self._startDt_cache, self._endDt_cache)
            self._datas[fname] = datas
            return datas.loc[startDt:endDt]

if __name__ == "__main__":
    obj = FactorData("pe", "Z:\\factor_datas")#"E:\\evilAlpha\\test")
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