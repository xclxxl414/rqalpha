#coding=utf-8

"""
@author: evilXu
@file: utils.py
@time: 2018/9/6 14:20
@description: 
"""
import pandas as pd
import numpy as np
from tqdm import tqdm
import statsmodels.api as sm
from scipy.stats.mstats import winsorize

def neutralize(factor = None,size = None,industry = None,beta = None):
    newData = pd.DataFrame(columns=factor.columns)
    if size is None and industry is None and beta is None:
        return newData
    #TODO index校验
    _size = size.dropna(how='all',axis=1).apply(lambda x: (x - x.mean()) / x.std(),axis=1) if size is not None else None
    _sec = industry.dropna(how='all',axis=1) if industry is not None else None
    _beta = beta.dropna(how='all',axis=1) if beta is not None else None
    getSec = lambda dt:(_sec.loc[dt].apply(lambda x: 1 if x==v else 0).rename(str(v)) for v in set(_sec.loc[dt].values) \
                        if not np.isnan(v)) if _sec is not None and dt in _sec.index else ()
    getBeta = lambda dt:_beta.loc[dt].rename("beta") if _beta is not None and dt in _beta.index else None
    getSize = lambda dt:_size.loc[dt].rename("size") if _size is not None and dt in _size.index else None
    loopindex = factor.dropna(how='all').index
    for dt in tqdm(loopindex):
        if _size is not None and dt not in _size.index:
            newData.loc[dt] = None
            continue
        if _sec is not None and dt not in _sec.index:
            newData.loc[dt] = None
            continue
        if _beta is not None and dt not in _beta.index:
            newData.loc[dt] = None
            continue
        x = pd.concat([*getSec(dt),getSize(dt),getBeta(dt)],axis=1)
        resid = sm.OLS(factor.loc[dt].replace(-np.inf,np.nan).replace(np.inf,np.nan).fillna(0)\
               ,x.reindex(index=factor.columns).replace(-np.inf,np.nan).replace(np.inf,np.nan).fillna(0).values,missing='drop').fit().resid
        newData.loc[dt] = resid
    newData = newData.reindex(index=factor.index, columns=factor.columns)
    return newData

def winsorized(df,limit=(0.01,0.01)):
    df=df.dropna(how='all')
    col=df.columns
    newdf=df.apply(lambda x: pd.Series(winsorize(x.dropna().values,limit),index=x.dropna().index),axis=1)
    newdf=newdf.reindex(columns=col)
    return newdf

standardize = lambda x: x.sub(x.mean(axis=1), axis=0).divide(x.std(axis=1), axis=0)


def orth_schmidt(df, orders=[]):
    '''
    df.index：因子s，df.columns:codes; orders正交化顺序:df.index的某个排列
    '''
    res = pd.DataFrame(columns=df.columns)
    if len(orders) < 1:
        return res
    res.loc[orders[0]] = df.loc[orders[0]]
    dots = {orders[0]: res.loc[orders[0]].dot(res.loc[orders[0]])}
    for idx in orders[1:]:
        a = res.apply(lambda x: x.dot(df.loc[idx]) * x / dots[x.name], axis=1)
        b = df.loc[idx] - a.sum().T
        res.loc[idx] = b
        dots[idx] = b.dot(b)
    return res