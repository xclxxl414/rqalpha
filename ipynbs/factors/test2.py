#coding=utf-8

"""
@author: evilXu
@file: test2.py
@time: 2018/5/24 13:57
@description: 
"""

from rqalpha.api import *
import traceback
from datetime import *
import pymysql
import pandas as pd
from rqalpha.utils.logger import user_log


def dependency():
    return []


def market(market=90):
    if market == 83:
        return 'XSHG'
    elif market == 90:
        return 'XSHE'
    else:
        return ""


def compute(startdt, enddt, context):
    '''
    PE
    :param startdt:
    :param enddt:
    :return:
    '''
    # context.config 对应配置的extra部分
    jydbConf = context.config.jydb
    conn = pymysql.connect(host=jydbConf.host,port= jydbConf.port,user=jydbConf.user
                           ,passwd = jydbConf.passwd,db=jydbConf.db,cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    _category = [1, ]
    _sectors = [1, 2, 6]
    _sql = "SELECT p.TradingDay as date,p.TurnoverRate as value,a.SecuCode as code,a.SecuMarket" \
           " FROM QT_Performance as p join " \
           "(SELECT innerCode,SecuCode,SecuMarket FROM secumain WHERE SecuMarket IN (83,90) " \
           "AND SecuCategory =1 AND ListedSector IN (%s) AND ListedState != 9) as a " \
           "on a.innerCode=p.innerCode where p.TradingDay between '%s' and '%s' order by p.TradingDay asc" % (
        ",".join([str(i) for i in _sectors]),startdt.strftime('%Y-%m-%d'),enddt.strftime('%Y-%m-%d'))
    print(_sql)
    cursor.execute(_sql)
    _res = pd.DataFrame(cursor.fetchall())
    # _res.code = _res.code + "." + _res.SecuMarket.apply(market)
    # _res = _res.drop(['SecuMarket'], axis=1).set_index(['date', 'code']).unstack(level=-1)
    # _res.columns = _res.columns.droplevel(level=0)
    return _res

if __name__ == "__main__":
    # test
    config = {"extra": {
        "jydb": {"host": "172.18.44.5", "port": 3306, "user": "liangh", "passwd": "huaxun!@#db", "db": "jydb"}}}
    from rqalpha.utils import RqAttrDict

    conf = RqAttrDict(config)
    from rqalpha.mod.rqalpha_mod_alphaStar_factors.factor_context import FactorContext

    context = FactorContext(conf)
    context.registerDepending(dependency())
    res = compute(datetime(2018, 5, 1), datetime(2018, 5, 24), context)
    print(res.head(10))