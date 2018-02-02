#coding=utf-8

"""
@author: evilXu
@file: factor.py
@time: 2017/11/6 18:11
@description:  因子基类
"""

from rqalpha.events import EVENT, Event
from rqalpha.utils import run_when_strategy_not_hold
from rqalpha.utils.logger import user_system_log
from rqalpha.utils.i18n import gettext as _
from rqalpha.utils.exception import ModifyExceptionFromType
from rqalpha.execution_context import ExecutionContext
from rqalpha.const import EXECUTION_PHASE, EXC_TYPE
from rqalpha.environment import Environment

class Factor():
    def __init__(self, scope):

        self._init = scope.get('init', None)
        self._compute = scope.get('compute',None)

    def init(self):
        if not self._init:
            return

        with ModifyExceptionFromType(EXC_TYPE.USER_EXC):
            self._init()

    def compute(self, startdt,enddt):
        '''
        左右闭区间，
        return 示例：
        code_cnt = 4
        day_cnt = 60
        df = pd.DataFrame([[random.random() for j in range(code_cnt)] for i in range(day_cnt)],
                      columns=list(["code" + str(i) for i in range(code_cnt)]),
                      index=[datetime(2015, 12, 1) + timedelta(days=i) for i in range(day_cnt)])
        '''
        with ModifyExceptionFromType(EXC_TYPE.USER_EXC):
            return self._compute(startdt, enddt)

