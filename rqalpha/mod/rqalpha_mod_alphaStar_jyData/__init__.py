#coding=utf-8

"""
@author: evilXu
@file: __init__.py.py
@time: 2017/6/8 15:44
@description: 
"""

__config__ = {
    #dataServerUrl
    "url": "",
}

#unimplement
#TODO implement
def load_mod():
    from .mod import JYDataMode
    return JYDataMode()
