#coding=utf-8

"""
@author: xuchunlin
@file: singleton.py
@time: 2016/11/23 15:40
@description: 
"""

def singleton(cls):
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton