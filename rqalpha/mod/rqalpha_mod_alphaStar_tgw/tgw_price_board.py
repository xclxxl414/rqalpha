#coding=utf-8

"""
@author: evilXu
@file: tgw_price_board.py
@time: 2018/5/16 15:00
@description: 
"""

import numpy as np

from rqalpha.interface import AbstractPriceBoard
from rqalpha.environment import Environment
from .tgw_broker import TgwTick

class TGWPriceBoard(AbstractPriceBoard):
    def __init__(self):
        self._env = Environment.get_instance()
        mod_config = self._env.config.mod.alphaStar_tgw
        self._tgwTick = TgwTick(tickUrl=mod_config.tickurl, secretId_TICK=mod_config.secretId_TICK
                                , secretKey_TICK=mod_config.secretKey_TICK)

    @property
    def _bar_dict(self):
        return self._env.bar_dict

    def get_last_price(self, order_book_id):
        res = self._tgwTick.getTick([order_book_id])
        if res is None or len(res) < 1:
            return 0
        res = res[0]
        return res['NowPrice'] if res['NowPrice'] > 0 else res['PrevClose']

    def get_limit_up(self, order_book_id):
        return np.nan if self._bar_dict.dt is None else self._bar_dict[order_book_id].limit_up

    def get_limit_down(self, order_book_id):
        return np.nan if self._bar_dict.dt is None else self._bar_dict[order_book_id].limit_down

    def get_a1(self, order_book_id):
        return np.nan

    def get_b1(self, order_book_id):
        return np.nan
