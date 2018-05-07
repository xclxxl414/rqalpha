#coding=utf-8

"""
@author: evilXu
@file: demo.py
@time: 2018/5/4 10:27
@description: 
"""

conf_file = "E:\\evilAlpha\\staralpha\\ipynbs\config.yml"
conf_file_factor = "E:\\evilAlpha\\staralpha\\ipynbs\config_factor.yml"
conf_file_taskmgr = "E:\\evilAlpha\\staralpha\\ipynbs\config_taskmgr.yml"

def testRunFile():
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
    # config = None
    file_path = "E:\\evilAlpha\\staralpha\\ipynbs\\strategys\\testStrategy.ipynb"
    run_file(file_path, config, config_file=conf_file)

def testEvaluateFile():
    from rqalpha.mod.rqalpha_mod_alphaStar_factors import evaluate_file
    factor_file = "E:\\evilAlpha\\staralpha\\rqalpha\\examples\\pe.py"
    evaluate_file(factor_file_path=factor_file, config=None, config_file=conf_file_factor)

def testCallFactor():
    from rqalpha.mod.rqalpha_mod_alphaStar_mgr import _callFactors
    _callFactors(config_path="E:\\evilAlpha\\staralpha\\ipynbs\config_taskmgr.yml", base__end_date="2018-05-04")

def testCallStrategys():
    from rqalpha.mod.rqalpha_mod_alphaStar_mgr import _callStrategys
    _callStrategys(config_path="E:\\evilAlpha\\staralpha\\ipynbs\config_taskmgr.yml", base__end_date="2018-05-07")

if __name__ == "__main__":
    testCallStrategys()


