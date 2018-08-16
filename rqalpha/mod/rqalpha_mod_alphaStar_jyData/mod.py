#coding=utf-8

"""
@author: evilXu
@file: mod.py
@time: 2017/6/27 10:47
@description: 
"""

from rqalpha.interface import AbstractMod
from rqalpha.mod.rqalpha_mod_alphaStar_jyData.jy_data_source import JYDataSource
# from rqalpha.mod.rqalpha_mod_sys_alphaH.moke_data_source import MokeDataSource
from rqalpha.environment import Environment

class JYDataMode(AbstractMod):
    def __init__(self):
        self._inject_api()

    def start_up(self, env, mod_config):
        # 设置 data_source 为 JYDataSource 类的对象
        # print(">>> AlphaHDataMode.start_up,url:",mod_config.url)
        env.set_data_source(JYDataSource(mod_config.url))

    def tear_down(self, code, exception=None):
        pass
        # print(">>> AlphaHDataMode.tear_down")

    def _inject_api(self):
        from rqalpha import export_as_api
        from rqalpha.execution_context import ExecutionContext
        from rqalpha.const import EXECUTION_PHASE

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def get_all_instruments():
            return Environment.get_instance().data_proxy.get_all_instruments()

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def get_factor(code_list = None, tdate = None, factor_list=[]):
            return Environment.get_instance().data_proxy.get_factor(code_list, tdate, factor_list)

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def get_factor_index(code_list = None, tdate = None, factor_list=[],name_list = None):
            return Environment.get_instance().data_proxy.get_factor_index(code_list, tdate, factor_list,name_list)

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def index_components(date=None,code = None,name = None):
            return Environment.get_instance().data_proxy.index_components(date,code,name)

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def industry_components(date=None,code = None,name = None,level = None,standard = None):
            return Environment.get_instance().data_proxy.industry_components(date,code,name,level,standard)

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def margin_components(date = None):
            return Environment.get_instance().data_proxy.margin_components(date)

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def st_components(date = None):
            return Environment.get_instance().data_proxy.st_components(date)


