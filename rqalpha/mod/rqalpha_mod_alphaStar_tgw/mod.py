#coding=utf-8

"""
@author: evilXu
@file: mod.py
@time: 2018/1/4 16:38
@description: 
"""

import six

from rqalpha.interface import AbstractMod
from rqalpha.utils.i18n import gettext as _
from .tgw_broker import TgwBroker
from .tgw_event_source import TGWEventSource
from .tgw_price_board import TGWPriceBoard

class TGWMod(AbstractMod):
    def __init__(self):
        pass

    def start_up(self, env, mod_config):
        # print("TGWMod",mod_config)
        if env.config.base.frequency != "1d":
            raise NotImplementedError(_("Frequency {} is not support.").format(env.config.base.frequency))

        env.set_broker(TgwBroker(env,mod_config))
        event_source = TGWEventSource(env)
        env.set_event_source(event_source)
        env.set_price_board(TGWPriceBoard())

    def tear_down(self, code, exception=None):
        pass
