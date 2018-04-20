#coding=utf-8

"""
@author: evilXu
@file: pe.py
@time: 2018/4/20 10:03
@description: 
"""

# coding=utf-8

from rqalpha.api import *
import traceback
from datetime import *
from sqlalchemy import create_engine
import pandas as pd
from rqalpha.utils.logger import user_log


def dependency():
    return []


def compute(startdt, enddt, context):
    '''
    PE
    :param startdt:
    :param enddt:
    :return:
    '''
    user_log.info("pe compute")
    # context.config 对应配置的extra部分
    #     jydbConf = context.config.jydb
    #     _jyConnStr = "mysql://%s:%s@%s:%s/%s"%(jydbConf.user,jydbConf.passwd,jydbConf.ip,jydbConf.port,jydbConf.db)
    _jyConnStr = "mysql+pymysql://liangh:huaxun!@#db@172.18.44.5:3306/jydb"
    engine = create_engine(_jyConnStr)

    _category = [1, ]
    _sectors = [1, 2, 6]
    _sql = "SELECT p.TradingDay,p.PE,a.SecuCode,a.SecuMarket" \
           " FROM LC_DIndicesForValuation as p inner join secumain as a " \
           "on a.innerCode=p.innerCode where a.SecuMarket in (83,90) " \
           "and a.SecuCategory in (%s) and a.ListedSector in (%s) " \
           "and a.ListedState!=9 and p.TradingDay between '%s' and '%s' order by p.TradingDay asc" % (
               ",".join([str(i) for i in _category]), ",".join([str(i) for i in _sectors])
               , startdt.strftime('%Y-%m-%d'),
               enddt.strftime('%Y-%m-%d'))
    print(_sql)
    _res = pd.read_sql(sql=_sql, con=engine)
    market = {90: "XSHE", 83: "XSHG"}
    _res.SecuCode = _res.SecuCode + "." + _res.SecuMarket.apply(lambda x: market.get(x))
    _res = _res.drop(['SecuMarket'], axis=1).set_index(['TradingDay', 'SecuCode']).unstack(level=-1)
    _res.columns = _res.columns.droplevel(level=0)
    return _res