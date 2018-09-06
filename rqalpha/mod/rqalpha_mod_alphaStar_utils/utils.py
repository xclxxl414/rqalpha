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

def neutralize(factor = None,size = None,industry = None,beta = None):
    newData = pd.DataFrame(columns=factor.columns)
    if size is None and industry is None and beta is None:
        return newData
    #TODO index校验
    _size = size.apply(lambda x: (x - x.mean()) / x.std(),axis=1)
    _sec = industry
    _beta = beta
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