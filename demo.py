#coding=utf-8

"""
@author: evilXu
@file: demo.py
@time: 2018/3/14 10:09
@description: 
"""

# -*- coding: utf-8 -*-

from rqalpha import run_file
from rqalpha.mod.rqalpha_mod_alphaStar_factors import evaluate_file
from rqalpha.mod.rqalpha_mod_alphaStar_mgr import callFactors

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
      "plot": True,
      # "output_file":"./test.pkl"
    },
    "sys_simulation": {
      "enabled": True,
      "matching_type": "next_bar",
    },
    "alphaStar_factors": {
      "enabled": True
    },
    "alphaStar_mgr": {
      "enabled": False
    },
    "alphaStar_tgw": {
      "enabled": False
    },
    "alphaStar_utils": {
      "enabled": True
    }
  }
}

config_factor = {
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
      "enabled": False,
    },
    "sys_simulation": {
      "enabled": False,
    },
    "alphaStar_factors": {
      "enabled": True,
      "factor_data_path": "E:\\evilAlpha\\test",
      "factor_data_init_date": "2010-01-01",
      "extra":{
        "jydb":{
            "host": "172.18.44.5",
            "port": 3306,
            "db": "jydb",
            "user": "liangh",
            "passwd": "huaxun!@#db"
        }
      }
    },
    "alphaStar_accounts": {
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

config_taskmgr = {
  "--config": "./ipynbs/config_taskmgr.yml",
}

if __name__ == "__main__":
  from rqalpha import run_file

  config = {
    "base": {
      "start_date": "2017-01-01",
      "end_date": "2017-01-31",
    },
    "mod": {
      "sys_analyser": {
        "enabled": True,
        "plot": True
      }
    }
  }
  file_path = "./ipynbs/strategys/testStrategy.ipynb"
  run_file(file_path, config,config_file="./ipynbs/config.yml")


  # factor_file = "./rqalpha/examples/pe.py"
  # evaluate_file(factor_file_path=factor_file,config=config_factor,config_file="./ipynbs/config_factor.yml")

  # a=config_taskmgr.copy()
  # a.update({"--end-date":"2018-02-01","--adminDB":"./ipynbs/admin.db"})
  # callFactors(base__end_date = "2018-02-01",base__adminDB="./ipynbs/admin.db",config_path="./ipynbs/config_taskmgr.yml")
