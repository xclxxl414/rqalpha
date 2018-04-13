#coding=utf-8

"""
@author: evilXu
@file: demo.py
@time: 2018/3/14 10:09
@description: 
"""

# -*- coding: utf-8 -*-

from rqalpha import run_file

config = {
  "base": {
    "data_bundle_path":"E:\\evilAlpha\\bundle",
    "start_date": "2018-01-05",
    "end_date": "2018-02-28",
    "benchmark": "000300.XSHG",
    "accounts": {
      "stock": 100000
    },
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": False,
      "output_file":"./test.pkl"
    },
    "sys_simulation": {
      "enabled": True,
      "matching_type": "next_bar",
    },
    "alphaStar_factors": {
      "enabled": False
    },
    "alphaStar_mgr": {
      "enabled": False
    },
    "alphaStar_tgw": {
      "enabled": False
    },
    "alphaStar_utils": {
      "enabled": False
    }
  }
}


if __name__ == "__main__":
  strategy_file_path = "./rqalpha/examples/MarketValue.py"
  run_file(strategy_file_path, config)