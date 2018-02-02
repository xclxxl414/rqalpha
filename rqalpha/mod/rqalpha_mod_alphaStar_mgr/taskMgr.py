#coding=utf-8

"""
@author: evilXu
@file: taskMgr.py
@time: 2018/1/2 14:33
@description: 
"""
from .admin import Admin
from rqalpha.mod.rqalpha_mod_alphaStar_factors.factor import Factor
from rqalpha.mod.rqalpha_mod_alphaStar_factors.factor_data import FactorData
from datetime import *
import os
import sys
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


class TaskMgr():
    def __init__(self,db= None,ipynbPath = "",fdataPath = ""):
        '''
        '''
        self.adminConsole = Admin(db)
        self.ipyPath = ipynbPath
        self.factorDataPath = fdataPath

    def runFactors(self,startdt = None,enddt = None):
        '''
        run all Published Factors
        '''
        for fname,user in self.adminConsole.getPublishedFactors():
            try:
                self._runAFactor(fname,startdt, enddt)
            except  Exception as e:
                system_log.error("runAFactor failed,fname;{0},error:{1}",fname,e)
        system_log.info("runFactor Finshed for: {0},{1}",startdt,enddt)
        return

    def runStrategys(self,config):
        '''
        run all Published Strategys
        '''
        try:
            runner = StrategyRunner(config)
            for sname, user,accountid in self.adminConsole.getPublishedStrategys():
                try:
                    self._runAStrategy(sname, accountid,config,runner)
                except  Exception as e:
                    system_log.error("runAStrategy failed,fname;{0},error:{1}", sname, e)
            system_log.info("runStrategys Finshed for: {0}", config.base.end_date)
            runner.clear()
        except Exception as e:
            system_log.error("runStrategys failed:{0}",e)
        return

    def runAFactor(self, fname,startDt, endDt):
        sinfo = self.adminConsole.getFactor(fname)
        if not sinfo:
            system_log.info("factor {0} not exist", fname)
            return
        if sinfo[2] != "published":
            system_log.info("factor {0} has not published", fname)
            return
        self._runAFactor(fname,startDt,endDt)

    def _runAFactor(self, fname,startDt, endDt):
        _dataObj = FactorData(fname, self.factorDataPath,defaultInitDate=startDt)
        _latestUpdt = _dataObj.getLatestDate()
        if _latestUpdt >= endDt:
            return
        _startDt = _latestUpdt + timedelta(days=1)

        _file = os.path.join(self.ipyPath,fname + ".ipynb")
        system_log.debug("_runAFactor")
        scope = create_base_scope()
        scope.update({
            "g": GlobalVars()
        })
        apis = api_helper.get_apis()
        scope.update(apis)

        scope = FileStrategyLoader(_file).load(scope)
        user_factor = Factor(scope)

        with run_with_user_log_disabled(disabled=False):
            user_factor.init()

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
            obj.clear()
        except Exception as e:
            import traceback
            traceback.print_exc()
            system_log.error("runAStrategy failed:{0},{1}",sname,e)

    def _runAStrategy(self, sname,accountid,  config,runner):
        # print(type(sname),sname)
        config.base.strategy_file = os.path.join(self.ipyPath,sname+".ipynb")
        config.mod.alphaStar_tgw.combid = accountid
        config.mod.alphaStar_tgw.accountid = accountid
        config.base.start_date = config.base.end_date

        config.base.accounts ={"STOCK":config.mod.alphaStar_tgw.starting_cash}
        config.base.init_positions = {}
        runner.run(config)

class StrategyRunner():
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

    def clear(self):
        result = self.mod_handler.tear_down(const.EXIT_CODE.EXIT_SUCCESS)
        system_log.debug(_(u"strategy run successfully, normal exit"))
        return result

    def run(self,config):
        env = self.env
        env.set_strategy_loader(FileStrategyLoader(config.base.strategy_file))
        _adjust_start_date(env.config, env.data_proxy)
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