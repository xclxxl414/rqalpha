#coding=utf-8

"""
@author: evilXu
@file: mod.py
@time: 2018/2/28 16:59
@description: 
"""

from rqalpha.interface import AbstractMod
from rqalpha.utils.logger import system_log
import pandas as pd
from rqalpha.api import *

class UtilsMod(AbstractMod):
    def __init__(self):
        self._inject_api()

    def start_up(self, env, mod_config):
        system_log.debug("UtilsMod.start_up,config:{0}",mod_config)

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
        def equalWeight_order(tobe_holding_codes=[], context=None):
            if len(tobe_holding_codes) < 1:
                for code, pos in context.portfolio.positions.items():
                    if pos.sellable > 0:
                        order_shares(code, -1 * pos.sellable)
                return
                #     print("positions",context.portfolio.positions)
            _target_percent = round(1.0 / len(tobe_holding_codes), 2)
            _targets = set(tobe_holding_codes)
            _tobe_sell = [pos for code, pos in context.portfolio.positions.items() if code not in _targets]
            for pos in _tobe_sell:
                if pos.sellable > 0:
                    order_shares(pos.order_book_id, -1 * pos.sellable)
            for code in tobe_holding_codes:
                _acount = context.portfolio.stock_account
                _cash_percent = round(_acount.cash / _acount.total_value, 2)
                _real_percent = min(_cash_percent, _target_percent)
                #         print(_acount.cash,_acount.total_value,_cash_percent,_real_percent)
                if _real_percent > 0:
                    order_target_percent(code, _real_percent)
            return