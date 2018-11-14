#coding=utf-8

"""
@author: evilXua
@file: demo.py
@time: 2018/5/4 10:27
@description: 
"""

import IPython
from matplotlib import rcParams, gridspec, ticker, image as mpimg, pyplot as plt
import os

#ipynbpath = "E:\\evilAlpha\\staralpha\\ipynbs\\"
ipynbpath = "/home/online/pre_ipynbs/"
conf_file = os.path.join(ipynbpath, "config.yml")
conf_file_factor = os.path.join(ipynbpath, "config_factor.yml")
conf_file_taskmgr = os.path.join(ipynbpath, "config_taskmgr.yml")

def testRunFile():
    from rqalpha import run_file
    config = {
        "base": {
            "start_date": "2018-01-01",
            "end_date": "2018-01-31",
        },
        "mod": {
            "sys_analyser": {
                "enabled": True,
                "plot": True
            }
        }
    }
    # config = None
    file_path = os.path.join(ipynbpath,"strategys/testStrategy.ipynb")
    run_file(file_path, config, config_file=conf_file)

def testEvaluateFile():
    from rqalpha.mod.rqalpha_mod_alphaStar_factors import evaluate_file
    factor_file = "E:\\evilAlpha\\staralpha\\rqalpha\\examples\\pe.py"
    evaluate_file(factor_file_path=factor_file, config=None, config_file=conf_file_factor)

def testCallFactor():
    from rqalpha.mod.rqalpha_mod_alphaStar_mgr import _callFactors
    _callFactors(config_path=conf_file_taskmgr, base__end_date="2018-08-14")

def testCallStrategys():
    from rqalpha.mod.rqalpha_mod_alphaStar_mgr import _callStrategys
    _callStrategys(config_path=conf_file_taskmgr, base__end_date="2018-05-16")

def testDailyProcess():
    from rqalpha.mod.rqalpha_mod_alphaStar_mgr import _dailyProcess
    _dailyProcess(config_path=conf_file_taskmgr)

def testMonitor():
    from rqalpha.mod.rqalpha_mod_alphaStar_mgr import _monitor
    _monitor(config_path=conf_file_taskmgr)

if __name__ == "__main__":
    testCallFactor()


