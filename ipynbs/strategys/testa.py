#coding=utf-8

"""
@author: evilXu
@file: testa.py
@time: 2018/3/5 18:19
@description: 
"""

from rqalpha import run_file

config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
        "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

strategy_file_path = "../../rqalpha/examples/buy_and_hold.py"
# strategy_file_path = "./testS.py"
run_file(strategy_file_path, config,config_file = "../config.yml")