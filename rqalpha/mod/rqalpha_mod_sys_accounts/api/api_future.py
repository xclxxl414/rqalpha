# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division
import six
import numpy as np

from rqalpha.api.api_base import decorate_api_exc, instruments, cal_style
from rqalpha.execution_context import ExecutionContext
from rqalpha.environment import Environment
from rqalpha.model.order import Order, MarketOrder, LimitOrder, OrderStyle
from rqalpha.const import EXECUTION_PHASE, SIDE, POSITION_EFFECT, ORDER_TYPE, RUN_TYPE
from rqalpha.model.instrument import Instrument
from rqalpha.utils.exception import RQInvalidArgument
from rqalpha.utils.logger import user_system_log
from rqalpha.utils.i18n import gettext as _
from rqalpha.utils.arg_checker import apply_rules, verify_that

__all__ = [
]

def export_as_api(func):
    __all__.append(func.__name__)

    func = decorate_api_exc(func)

    return func

@export_as_api
@ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                EXECUTION_PHASE.BEFORE_TRADING,
                                EXECUTION_PHASE.ON_BAR,
                                EXECUTION_PHASE.ON_TICK,
                                EXECUTION_PHASE.AFTER_TRADING,
                                EXECUTION_PHASE.SCHEDULED)
@apply_rules(verify_that('underlying_symbol').is_instance_of(str))
def get_future_contracts(underlying_symbol):
    """
    获取某一期货品种在策略当前日期的可交易合约order_book_id列表。按照到期月份，下标从小到大排列，返回列表中第一个合约对应的就是该品种的近月合约。

    :param str underlying_symbol: 期货合约品种，例如沪深300股指期货为'IF'

    :return: list[`str`]

    :example:

    获取某一天的主力合约代码（策略当前日期是20161201）:

        ..  code-block:: python

            [In]
            logger.info(get_future_contracts('IF'))
            [Out]
            ['IF1612', 'IF1701', 'IF1703', 'IF1706']
    """
    env = Environment.get_instance()
    return env.data_proxy.get_future_contracts(underlying_symbol, env.trading_dt)
