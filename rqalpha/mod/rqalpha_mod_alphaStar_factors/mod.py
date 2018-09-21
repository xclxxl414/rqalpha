#coding=utf-8

"""
@author: evilXu
@file: mod.py
@time: 2017/11/14 16:07
@description: 
"""

from rqalpha.interface import AbstractMod
from .factor_data import FactorDataInterface
from rqalpha.utils.logger import system_log
import pandas as pd

class FactorDataMod(AbstractMod):
    def __init__(self):
        self._iData = None
        self._inject_api()

    def start_up(self, env, mod_config):
        system_log.debug("FactorDataMod.start_up,config:{0}",mod_config)
        _initDate = pd.Timestamp(mod_config.factor_data_init_date).date() if mod_config.factor_data_init_date is not None else None
        self._iData = FactorDataInterface(path = mod_config.factor_data_path,defaultInitDate=_initDate)

    def tear_down(self, code, exception=None):
        pass
        # print(">>> AlphaHDataMode.tear_down")

    def _inject_api(self):
        from rqalpha import export_as_api
        from rqalpha.execution_context import ExecutionContext
        from rqalpha.const import EXECUTION_PHASE

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.GLOBAL,
                                        EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def get_factors(fname= "",sdate=None,eDate = None):
            '''
            数据结构参考get_fundamentals
            pandas + sqlalchemy
            numpy + sqlalchemy
            hdf5 + sqlalchemy
            :param fname:
            :param sdate:
            :param eDate:
            :return:
            '''
            '''
             <class 'pandas.core.frame.DataFrame'>
    2017-10-09 INFO                 601766.XSHG 601898.XSHG  600998.XSHG  600887.XSHG  601992.XSHG  \
                            revenue   8.8717e+10  3.7104e+10  3.62284e+10  3.34935e+10  2.94658e+10   
                            pe_ratio     27.6174     26.5919       25.741      29.0545      25.0025 
            '''
            '''3x6x0_1
            '''
            return self._iData.getData(fname,sdate,eDate)