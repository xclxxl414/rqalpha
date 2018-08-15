#coding=utf-8

"""
@author: evilXu
@file: factor_context.py
@time: 2018/3/6 14:53
@description: 
"""

import six

class FactorContext(object):
    def __repr__(self):
        items = ("%s = %r" % (k, v)
                 for k, v in six.iteritems(self.__dict__)
                 if not callable(v) and not k.startswith("_"))
        return "Context({%s})" % (', '.join(items),)

    def __init__(self,config):
        self._config = config
        self._dependency = []

    @property
    def modconfig(self):
        return self._config

    @property
    def config(self):
        return self._config.extra

    def registerDepending(self,dependFactors=[]):
        self._dependency = dependFactors

    @property
    def dependency(self):
        return self._dependency

    def __setstate__(self, state):
        self._config = state.get("conf")
        self._dependency = state.get("dependency")

    def __getstate__(self):
        state = {"conf":self._config,"dependency":self._dependency}
        return state
