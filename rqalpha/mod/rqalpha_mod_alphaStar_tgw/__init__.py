#coding=utf-8

"""
@author: evilXu
@file: __init__.py.py
@time: 2018/1/4 15:30
@description: 
"""

import click
from rqalpha import cli

__config__ = {
    # 淘股王调仓借口url
    "tgwurl": "http://www.tgwtest.com/tgwapi/myapp/Trade",
    "secretId": "commonkey",
    "secretKey": "TGW_COMMONKEY",
    #淘股王实时行情接口url
    "tickurl": "http://tgw360.com/webapi/myapp/WxInterface/GetQueInfo",
    "secretId_TICK": "dianziqianzhang",
    "secretKey_TICK": "B123456789",

    # 账户信息
    "uid": 15154,
    "combid": 665,
    "accountid":665,
    "starting_cash": 10000000,
}

def load_mod():
    from .mod import TGWMod
    return TGWMod()
