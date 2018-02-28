#coding=utf-8

"""
@author: evilXu
@file: testS.py
@time: 2018/2/28 17:33
@description: 
"""

from rqalpha.api import *

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")


def before_trading(context):
    pass


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    print("haha")
    _fvalue = get_factors("testFactor", context.now.date(), context.now.date()).iloc[0]
    _fvalue = _fvalue[_fvalue > 0]
    #     print(context.now,_fvalue.sort_values())
    # 买入低估值排名前10的票
    buy_codes = list(_fvalue.sort_values().index[:10])
    #     holdings = [code for code in context.portfolio.positions]
    print(buy_codes)
    equalWeight_order(buy_codes, context)


if __name__ == "__main__":
    from rqalpha import run_file
    config = {
      "base": {
        "start_date": "2017-01-01",
        "end_date": "2017-01-31",
      },
    }

    file_path = "./testStrategy.ipynb"
    run_file(file_path, config,config_file = "../config.yml")