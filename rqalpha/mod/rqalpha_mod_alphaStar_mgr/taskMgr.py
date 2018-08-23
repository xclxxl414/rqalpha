#coding=utf-8

"""
@author: evilXu
@file: taskMgr.py
@time: 2018/1/2 14:33
@description: 
"""
from .admin import Admin
from rqalpha.mod.rqalpha_mod_alphaStar_factors.factor import Factor
from rqalpha.mod.rqalpha_mod_alphaStar_factors.factor_context import FactorContext
from rqalpha.mod.rqalpha_mod_alphaStar_factors.factor_data import FactorData
from datetime import *
import os
import sys
import pytz
import datetime
from pprint import pformat
import six
from rqalpha import const
from rqalpha.api import helper as api_helper
from rqalpha.core.strategy_loader import FileStrategyLoader
from rqalpha.core.strategy import Strategy
from rqalpha.core.strategy_universe import StrategyUniverse
from rqalpha.core.global_var import GlobalVars
from rqalpha.core.strategy_context import StrategyContext
from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.data.data_proxy import DataProxy
from rqalpha.environment import Environment
from rqalpha.events import EVENT, Event
from rqalpha.execution_context import ExecutionContext
from rqalpha.mod import ModHandler
from rqalpha.model.bar import BarMap
from rqalpha.utils import create_custom_exception, run_with_user_log_disabled, scheduler as mod_scheduler
from rqalpha.utils.exception import CustomException
from rqalpha.utils.i18n import gettext as _
from rqalpha.utils.scheduler import Scheduler
from rqalpha.utils.logger import system_log, basic_system_log
from rqalpha.main import create_base_scope,set_loggers,_adjust_start_date,_validate_benchmark,create_benchmark_portfolio,_exception_handler
import multiprocessing
from multiprocessing import cpu_count
import threading
import time

def getFactorObj(sourcePath, fname, modconf):
    _file = os.path.join(sourcePath, "factors/" + fname + ".ipynb")
    scope = create_base_scope()
    scope.update({
        "g": GlobalVars(),
        "name": fname,
    })
    apis = api_helper.get_apis()
    scope.update(apis)

    scope = FileStrategyLoader(_file).load(scope)
    user_factor = Factor(scope, FactorContext(modconf))
    return user_factor


class TaskMgr():
    def __init__(self, db= None, sourcePath ="", fdataPath =""):
        '''
        '''
        self.adminConsole = Admin(db)
        self.sourcePath = sourcePath
        self.factorDataPath = fdataPath

    def runFactors(self, dataInitDt = None, enddt = None, modconf = None):
        '''
        run all Published Factors
        '''
        _fobjs = []
        for fname, user in self.adminConsole.getPublishedFactors():
            try:
                _fobjs.append(getFactorObj(self.sourcePath,fname,modconf))
            except Exception as e:
                system_log.error("runAFactor failed,create facor obj failed:fname;{0},error:{1}", fname, e)
        #不做优先队列，直接轮询查询依赖序列更能利用多核，优先队列不适用以下情形：高优先级有一个极慢因子且没有被依赖。
        _taskRunner = FactorMultiProcessRunner()  # 每个优先级先完成
        while len(_taskRunner.finished_set) >= len(_fobjs):
            for _fobj in _fobjs:
                time.sleep(0.001) #
                if _fobj.name in _taskRunner.finished_set:
                    continue
                elif len(set(_fobj.dependency()) - _taskRunner.finished_set) > 0:
                    #has unfinished dependency
                    continue
                else:
                    _taskRunner.addTaskFactorRun(_fobj.name,self.sourcePath,modconf,self.factorDataPath,dataInitDt,enddt)
            time.sleep(1)
        _taskRunner.wait()

        #version priQueue
        # priQueue = self._priQueueFactor(_fobjs)
        # for listPi in priQueue:
        #     _taskRunner = FactorMultiProcessRunner()  # 每个优先级先完成
        #     for fobj in listPi:
        #         _taskRunner.addTaskFactorRun(fobj.name,self.sourcePath,modconf,self.factorDataPath,dataInitDt,enddt)
        #     _taskRunner.wait()
        system_log.info("runFactors Finshed for: {0},{1}", dataInitDt, enddt)
        return

    @DeprecationWarning
    def _priQueueFactor(self,factorObjs):
        '''
        因子任务优先队列
        :return: [[p0,p0,p0],[p1,p1,p1]]
        '''
        _child2parents = {}
        _name2Factors = {}
        for factor in factorObjs:
            fname = factor.name
            if len(factor.dependency()) > 0:
                _child2parents[fname] = factor.dependency()
            _name2Factors[fname] = factor
        _res = []
        #最高优先级，没有父因子的
        _pi = 0
        for fname in _name2Factors.keys():
            if fname not in _child2parents:
                _res.append((fname,_pi))

        # print(len(_cid2pids))
        while True:
            # print("cids:",_cid2pids,_res)
            _alreadyIn = set([id for id,pi in _res])
            _pi += 1
            for cid,pids in _child2parents.items():
                if cid in _alreadyIn:
                    continue
                _pidsFilished = True # 所有父因子都已在高优先级？
                for _pid in pids:
                    if _pid not in _alreadyIn:
                        _pidsFilished = False
                        break
                if _pidsFilished:
                    _res.append((cid, _pi))
            if len(_res) <= len(_alreadyIn): # 没有新增
                break
        # print(_res,_id2Name)
        _ret = []
        _lastPi = 0
        _lastRes = []
        _handleNames = set({})
        for fname,pi in _res:
            if pi != _lastPi:
                if len(_lastRes) > 0:
                    # print(_lastRes)
                    _ret.append(_lastRes)
                    _handleNames.add(fname)
                    _lastRes = [_name2Factors.get(fname)]
                _lastPi = pi
            else:
                _handleNames.add(fname)
                _lastRes.append(_name2Factors.get(fname))
        if len(_lastRes) > 0:
            # print(_lastRes)
            _ret.append(_lastRes)
        if len(_name2Factors) > len(_handleNames):
            system_log.error("missing pre factors:{}",_name2Factors.keys()-_handleNames)
        return _ret

    def runStrategys(self,config):
        '''
        run all Published Strategys
        '''
        try:
            runner = StrategyRunner(config)
            for sname, user,accountid in self.adminConsole.getPublishedStrategys():
                try:
                    self._runAStrategy(sname, accountid,config,runner)
                    system_log.info("strategy {} run Finshed till {}", sname, config.base.end_date)
                except  Exception as e:
                    system_log.error("_runAStrategy failed,fname;{0},error:{1}", sname, e)
                    import traceback
                    traceback.print_exc()
            system_log.info("runStrategys Finshed for: {0}", config.base.end_date)
            runner.clear()
        except Exception as e:
            system_log.error("runStrategys failed:{0}",e)
        return

    def runAFactor(self, fname, dataInitDt, endDt, modconf):
        sinfo = self.adminConsole.getFactor(fname)
        if not sinfo:
            system_log.info("factor {0} not exist", fname)
            return
        if sinfo[2] != "published":
            system_log.info("factor {0} has not published", fname)
            return
        self._runAFactor(fname, dataInitDt, endDt, modconf)
        system_log.info("factor {0} run Finshed till {1}", fname, endDt)

    def _runAFactor(self, fname, dataInitDt, endDt, modconf):
        _dataObj = FactorData(fname, self.factorDataPath, defaultInitDate=dataInitDt)
        _latestUpdt = _dataObj.getLatestDate()
        if _latestUpdt >= endDt:
            return
        _startDt = _latestUpdt + timedelta(days=1)

        user_factor = getFactorObj(self.sourcePath,fname,modconf)
        res = user_factor.compute(_startDt,endDt)
        if len(res) > 0:
            _dataObj.append(res)
        return

    def runAStrategy(self, sname, config):
        sinfo = self.adminConsole.getStrategy(sname)
        if not sinfo:
            system_log.info("strategy {0} not exist", sname)
            return
        if sinfo[3] != "published":
            system_log.info("strategy {0} has not published",sname)
            return
        try:
            obj = StrategyRunner(config)
            self._runAStrategy(sname,sinfo[2],config,obj)
            system_log.info("strategy {} run Finshed till {}", sname, config.base.end_date)
            obj.clear()
        except Exception as e:
            import traceback
            traceback.print_exc()
            system_log.error("runAStrategy failed:{0},{1}",sname,e)

    def _runAStrategy(self, sname,accountid,config,runner):
        # print(type(sname),sname)
        config.base.strategy_file = os.path.join(self.sourcePath, "strategys/"+ sname + ".ipynb")

        for name,account in six.iteritems(config.base.accounts):
            account.update({"combid":accountid,"accountid":accountid})
        orders = runner.run(config)
        self.adminConsole.dumpStrategyLog(sname,config.base.end_date,str(orders))
        return orders

class StrategyRunner():
    '''
    策略运行，向淘股王账号发送调仓信息
    '''
    def __init__(self,config):
        self._config = config
        env = Environment(config)
        mod_handler = ModHandler()

        try:
            # avoid register handlers everytime
            # when running in ipython
            set_loggers(config)
            basic_system_log.debug("\n" + pformat(config.convert_to_dict()))


            env.set_global_vars(GlobalVars())
            mod_handler.set_env(env)
            mod_handler.start_up()

            if not env.data_source:
                env.set_data_source(BaseDataSource(config.base.data_bundle_path))
            env.set_data_proxy(DataProxy(env.data_source))

            # TODO 校验交易日
            config.base.start_date,config.base.end_date = self.adjustTradingDay(env.data_proxy, config)
            config.base.start_date = config.base.end_date
            config.base.trading_calendar = env.data_proxy.get_trading_dates(config.base.start_date, config.base.end_date)
            config.base.timezone = pytz.utc

            Scheduler.set_trading_dates_(env.data_source.get_trading_calendar())
            scheduler = Scheduler(config.base.frequency)
            mod_scheduler._scheduler = scheduler

            env._universe = StrategyUniverse()

            bar_dict = BarMap(env.data_proxy, config.base.frequency)
            env.set_bar_dict(bar_dict)

            if env.price_board is None:
                from rqalpha.core.bar_dict_price_board import BarDictPriceBoard
                env.price_board = BarDictPriceBoard()
            self.env = env
            self.mod_handler = mod_handler
            self.scheduler = scheduler
            self.bar_dict = bar_dict
        except CustomException as e:
            code = _exception_handler(e)
            mod_handler.tear_down(code, e)
        except Exception as e:
            exc_type, exc_val, exc_tb = sys.exc_info()
            user_exc = create_custom_exception(exc_type, exc_val, exc_tb, config.base.strategy_file)

            code = _exception_handler(user_exc)
            mod_handler.tear_down(code, user_exc)

    @classmethod
    def adjustTradingDay(cls, dataproxy, config):
        _start = config.base.end_date + timedelta(days = -20)
        b = dataproxy.get_trading_dates(_start, config.base.end_date)
        if b[-1].date() != config.base.end_date:
            raise CustomException("enddate is not TradingDay")
        return b[-2].date(),b[-1].date()

    def clear(self):
        result = self.mod_handler.tear_down(const.EXIT_CODE.EXIT_SUCCESS)
        system_log.debug(_(u"strategy run successfully, normal exit"))
        return result

    def run(self,config):
        env = self.env
        env.set_strategy_loader(FileStrategyLoader(config.base.strategy_file))
        _validate_benchmark(env.config, env.data_proxy)

        # FIXME
        start_dt = datetime.datetime.combine(config.base.start_date, datetime.datetime.min.time())
        env.calendar_dt = start_dt
        env.trading_dt = start_dt

        broker = env.broker
        assert broker is not None
        env.portfolio = broker.get_portfolio()
        env.benchmark_portfolio = create_benchmark_portfolio(env)

        event_source = env.event_source
        assert event_source is not None

        ctx = ExecutionContext(const.EXECUTION_PHASE.GLOBAL)
        ctx._push()

        env.event_bus.publish_event(Event(EVENT.POST_SYSTEM_INIT))

        scope = create_base_scope()
        scope.update({
            "g": env.global_vars
        })

        apis = api_helper.get_apis()
        scope.update(apis)

        scope = env.strategy_loader.load(scope)
        ucontext = StrategyContext()
        user_strategy = Strategy(env.event_bus, scope, ucontext)
        self.scheduler.set_user_context(ucontext)

        if not config.extra.force_run_init_when_pt_resume:
            with run_with_user_log_disabled(disabled=config.base.resume_mode):
                user_strategy.init()

        if config.extra.context_vars:
            for k, v in six.iteritems(config.extra.context_vars):
                setattr(ucontext, k, v)

        # When force_run_init_when_pt_resume is active,
        # we should run `init` after restore persist data
        if config.extra.force_run_init_when_pt_resume:
            assert config.base.resume_mode == True
            with run_with_user_log_disabled(disabled=False):
                user_strategy.init()

        from rqalpha.core.executor import Executor
        Executor(env).run(self.bar_dict)
        return env.broker.get_open_orders()


class FactorMultiProcessRunner(object):

    finished_set = set()

    def __init__(self):
        _cpu_cnt = cpu_count()
        _cnt = _cpu_cnt - 4 if _cpu_cnt >=8 else _cpu_cnt
        self._procs = multiprocessing.Pool(_cnt)  # 默认个数与cpu数相同
        self._lock = threading.Lock()  # 对象锁，任务只能依次添加

    def wait(self):
        with self._lock:
            self._procs.close()
            self._procs.join()
            print("LocalTaskMgr finished")

    @staticmethod
    def factorRun(fname,sourcepath,modconf,factorDataPath,dataInitDt,enddt):
        try:
            _dataObj = FactorData(fname, factorDataPath, defaultInitDate=dataInitDt)
            _latestUpdt = _dataObj.getLatestDate()
            if _latestUpdt >= enddt:
                system_log.info("factor {0} already uptodate: {1}", fname, enddt)
                return fname
            _startDt = _latestUpdt + timedelta(days=1)
            fobj = getFactorObj(sourcepath,fname,modconf)
            res = fobj.compute(_startDt, enddt)
            if len(res) > 0:
                _dataObj.append(res)
            system_log.info("factor {0} run Finshed till {1}", fname, enddt)
        except  Exception as e:
            system_log.error("runFactor failed,fname;{0},error:{1}", fname, e)
            import traceback
            traceback.print_exc()
        finally:
            return fname

    @staticmethod
    def factorRunCallBack(res=()):
        FactorMultiProcessRunner.add(res)
        # _LOG = LogMgr.getLog("server")
        # _LOG.info("factorRunCallBack:%s", res)

    def addTaskFactorRun(self, fname,sourcepath,modconf,factorDataPath,dataInitDt,enddt):
        '''
        Args:
            fname: factor name
            tradingDt:  交易日
            enddt: 交易日因子值可以去数据的截止时间，一般是下个交易日0点
        Returns:
        '''
        with self._lock:
            _res = self._procs.apply_async(
                self.factorRun
                , args=(fname,sourcepath,modconf,factorDataPath,dataInitDt,enddt)
                , callback=self.factorRunCallBack)
            return True

if __name__ == "__main__":
    pass