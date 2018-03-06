#coding=utf-8

"""
@author: evilXu
@file: factor.py
@time: 2017/11/6 18:11
@description:  因子基类
"""

from rqalpha.utils.exception import ModifyExceptionFromType
from rqalpha.const import EXC_TYPE

class Factor():
    def __init__(self, scope,ucontext):
        self._ucontext = ucontext
        self._dependency = scope.get('dependency', None)
        self._compute = scope.get('compute',None)
        self._ucontext.registerDepending(self.dependency())

    def dependency(self):
        if not self._dependency:
            return []

        with ModifyExceptionFromType(EXC_TYPE.USER_EXC):
            return self._dependency()

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
            return self._compute(startdt, enddt,self._ucontext)

