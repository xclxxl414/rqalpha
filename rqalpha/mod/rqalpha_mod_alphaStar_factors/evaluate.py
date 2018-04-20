#coding=utf-8

"""
@author: evilXu
@file: evaluate.py
@time: 2017/11/6 18:11
@description:  因子评价
"""

from rqalpha.utils import create_custom_exception, run_with_user_log_disabled
from rqalpha.utils.exception import CustomException
from rqalpha.utils.i18n import gettext as _
from rqalpha.main import set_loggers,_adjust_start_date,create_base_scope,_exception_handler
from rqalpha.api import *
import os
import sys
import datetime
from pprint import pformat
from rqalpha import const
from rqalpha.api import helper as api_helper
from rqalpha.core.strategy_loader import FileStrategyLoader, SourceCodeStrategyLoader, UserFuncStrategyLoader
from rqalpha.core.global_var import GlobalVars
from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.data.data_proxy import DataProxy
from rqalpha.environment import Environment
from rqalpha.mod import ModHandler
from rqalpha.model.bar import BarMap
import pandas as pd
import rqalpha.utils.config as configpk
from rqalpha.utils.logger import system_log, basic_system_log, user_system_log, user_detail_log
import simplejson as json
import six
from .factor import  Factor
from rqalpha.utils import RqAttrDict, logger
from rqalpha.utils.dict_func import deep_update
import numpy as np
from matplotlib import rcParams, gridspec, ticker, image as mpimg, pyplot as plt
from rqalpha.mod.rqalpha_mod_alphaStar_factors.factor_context import FactorContext

def evaluateRun(fname,config):
    '''
    按临时定义计算数据评估, 用 stock_account计算收益率，每个票一个stock_account,或只用一个stock_account,一个票一个position,佣金、滑点
    先按天取得全部结果，用向量计算
    '''
    system_log.debug(_("evaluateRun"))
    env = Environment(config)
    mod_handler = ModHandler()

    try:
        set_loggers(config)
        basic_system_log.debug("\n" + pformat(config.convert_to_dict()))

        mod_handler.set_env(env)
        mod_handler.start_up()

        if not env.data_source:
            env.set_data_source(BaseDataSource(config.base.data_bundle_path))
        env.set_data_proxy(
            DataProxy(env.data_source))

        _adjust_start_date(env.config, env.data_proxy)
        start_dt = datetime.datetime.combine(config.base.start_date, datetime.datetime.min.time())
        env.calendar_dt = start_dt
        env.trading_dt = start_dt

        bar_dict = BarMap(env.data_proxy, config.base.frequency)
        env.set_bar_dict(bar_dict)
        if config.base.run_type == "p":
            fValue = getFactorsPre(start_dt=start_dt,end_dt=config.base.end_date,fname = fname,fDataPath=config.mod.alphaStar_factors.factor_data_path)
        else:
            fValue = getFactorsTmp(env,config=config)
        system_log.info("get factor value success")
        # BVs = BookValues(env)
        BVs = Prices( env)

        groupCnt  =10
        win = 5
        dates,ICs,group_yields = calc(BVs,fValue,groupCnt,win)
        ICIR = np.mean(ICs)/np.std(ICs)
        res = {"dates":dates,"ICs":ICs,"ICIR":ICIR,"groups":group_yields}
        # print(res)
        plot_result(fname, res)
    except CustomException as e:
        code = _exception_handler(e)
        mod_handler.tear_down(code, e)
    except Exception as e:
        import traceback
        traceback.print_exc()
        exc_type, exc_val, exc_tb = sys.exc_info()
        user_exc = create_custom_exception(exc_type, exc_val, exc_tb, config.base.factor_file)

        code = _exception_handler(user_exc)
        mod_handler.tear_down(code, user_exc)
    else:
        exitInfo = mod_handler.tear_down(const.EXIT_CODE.EXIT_SUCCESS)
        system_log.debug(_(u"strategy run successfully, normal exit:" + str(exitInfo)))
        return

def calc(bookValues, fValue, groupCnt = 10, win = 5):
    system_log.debug(_("calc"))

    dates = []
    ics = []
    group_AccuYields = [[] for i in range(groupCnt)] #累计收益率
    for idx in range(0, len(fValue), win):
        if idx + 1 + win >= len(bookValues):
            break
        _fValue_aDay = fValue.iloc[idx]
        _yield_nextWin = bookValues.iloc[idx + 1 + win] / bookValues.iloc[idx + 1] - 1
        dates.append(fValue.index[idx])
        ics.append(_fValue_aDay.corr(_yield_nextWin, method='spearman', min_periods=100))

        system_log.info("%s, factorValue len:%d, yieldData len:%d"%(dates[-1],len(_fValue_aDay),len(_yield_nextWin)))
        gRes = group(_yield_nextWin,_fValue_aDay,groupCnt)
        # print(len(gRes),_yield_nextWin)
        for i in range(groupCnt):
            group_AccuYields[i].append((1+gRes[i]) * (1 + group_AccuYields[i][-1] if len(group_AccuYields[i]) > 0 else 1) - 1.0)

    return dates,ics,group_AccuYields

def plot_result(fname,result,show_windows=True, savefile=None):
    title = fname
    ICs = result.get('ICs')
    ICIR = result.get('ICIR')
    group = result.get("groups")
    group_cnt = len(group)
    dates = result.get('dates')#[dt.strftime("%Y-%m-%d") for dt in result.get('dates')]

    plt.style.use('ggplot')

    red = "#aa4643"
    black = "#000000"
    cmap = plt.get_cmap('gnuplot')
    colors = [cmap(i) for i in np.linspace(0, 1, group_cnt)]

    plots_area_size = 10
    width = 16
    figsize = (width, plots_area_size)
    plt.figure(title, figsize=figsize)
    max_height = 3 * plots_area_size
    gs = gridspec.GridSpec(max_height, width)

    #ICs
    ax1 = plt.subplot(gs[:plots_area_size-1, :])
    ax1.set_title("IC")
    ax1.get_xaxis().set_minor_locator(ticker.AutoMinorLocator())
    ax1.get_yaxis().set_minor_locator(ticker.AutoMinorLocator())
    ax1.grid(b=True, which='minor', linewidth=.2)
    ax1.grid(b=True, which='major', linewidth=1)
    ax1.plot(dates,ICs, label="IC", alpha=1, linewidth=2, color=red)
    txt = ("ICIR : %0.2f") % (ICIR)
    ax1.text(0.05, 0.95, txt, fontsize=14,color=red, transform=ax1.transAxes)#,horizontalalignment='center',verticalalignment='center')
    # place legend
    leg = plt.legend(loc="best")
    leg.get_frame().set_alpha(0.5)
    # manipulate axis
    vals = ax1.get_yticks()
    ax1.set_yticklabels(['{:3.2f}'.format(x) for x in vals])

    # Groups
    if len(group) > 0:
        ax2 = plt.subplot(gs[plots_area_size:2 * plots_area_size,: ])
        ax2.set_title("Group of "+ str(group_cnt))
        ax2.get_xaxis().set_minor_locator(ticker.AutoMinorLocator())
        ax2.get_yaxis().set_minor_locator(ticker.AutoMinorLocator())
        ax2.grid(b=True, which='minor', linewidth=.2)
        ax2.grid(b=True, which='major', linewidth=1)
        for i in range(len(group)):
            ax2.plot(dates,group[i], label="group "+str(i), alpha=1, linewidth=2, color=colors[i])
        # place legend
        leg = plt.legend(loc="best")
        leg.get_frame().set_alpha(0.5)
        # manipulate axis
        vals = ax2.get_yticks()
        ax2.set_yticklabels(['{:3.2f}'.format(x) for x in vals])

        #group 横向柱状图
        ax3 = plt.subplot(gs[2*plots_area_size:3 * plots_area_size,: ])
        Y = np.arange(len(group))
        Y_Str = ["Group " + str(i) for i in range(len(group))]
        X = [group[i][-1] for i in range(len(group))]
        ax3.set_title("Group of "+ str(group_cnt))
        ax3.barh(Y, X,color=red)
        ax3.set_yticks(Y)
        ax3.set_ylabel("groups")
        # 绘制文字，显示柱状图形的值
        for x, y in zip(X,Y):
            ax3.text(x + np.sign(x) * 0.01, y, '%.2f' % x,horizontalalignment='center',verticalalignment='center')#, ha='center', va='bottom'

    if show_windows:
        # plt.tight_layout()
        plt.show()

def group(_yields, fValue, groupCnt):
    '''
    当期分组收益率
    '''
    _yield_dropNa = _yields.dropna()
    _fvalue_Sorted = fValue.sort_values(ascending=True)
    _res = []
    _yields = [_yield_dropNa.get(_code) for _code,_value in _fvalue_Sorted.items() if _yield_dropNa.get(_code)]
    _groupSize = round(len(_yields) / groupCnt)
    a= [_yields[i:i + _groupSize] for i in range(0, len(_yields), _groupSize)]
    if len(a) > groupCnt:
        a[-2] += a[-1]
        del a[-1]
    for subyield in a:
        _res.append(np.average(subyield))
    return _res

def getFactorsPre(start_dt,end_dt,fname,fDataPath):
    system_log.debug(_("getFactorsPre"))
    from .factor_data import FactorDataInterface
    return FactorDataInterface(path=fDataPath,defaultInitDate=start_dt,endDt=end_dt).getData(fname=fname,startDt=start_dt,endDt=end_dt)

def getFactorsTmp(env,config):
    system_log.debug(_("getFactorsTmp"))
    env.set_global_vars(GlobalVars())
    scope = create_base_scope()
    scope.update({
        "g": env.global_vars
    })

    apis = api_helper.get_apis()
    scope.update(apis)
    env.set_strategy_loader(FileStrategyLoader(config.base.factor_file))

    scope = env.strategy_loader.load(scope)
    user_factor = Factor(scope,FactorContext(config.mod.alphaStar_factors))

    res = user_factor.compute(env.trading_dt,config.base.end_date)
    return res

def Prices(env):
    '''
    输出价格以计算收益率
    '''
    config = env.config
    _tradingDays = env.data_proxy.get_trading_dates(config.base.start_date, config.base.end_date)
    _len = len(_tradingDays)
    _alInstruments = [item for item in env.data_proxy.get_all_instruments() if item.type == 'CS']
    _bars = {}
    _startDt = int(_tradingDays[0].date().strftime("%Y%m%d")) * 1000000
    for _instrument in _alInstruments:
        _abar = env.data_proxy.history_bars(_instrument.order_book_id, _len, '1d', field = ['datetime',config.base.price], dt = config.base.end_date,
                     skip_suspended=False, include_now=True,
                     adjust_type='post')
        if _abar is None:
            continue
        _abar = dict((int(date/1000000),value) for date,value in _abar if date >= _startDt)
        _bars[_instrument.order_book_id]= _abar
    res = pd.DataFrame(_bars)
    return res

def parse_config(config_args, config_path=None, click_type=False, source_code=None, user_funcs=None):
    conf = configpk.load_config(config_path)
    if 'base__factor_file' in config_args and config_args['base__factor_file']:
        # FIXME: ugly, we need this to get code
        conf['base']['factor_file'] = config_args['base__factor_file']
    elif ('base' in config_args and 'factor_file' in config_args['base'] and
          config_args['base']['factor_file']):
        conf['base']['factor_file'] = config_args['base']['factor_file']

    if user_funcs is None:
        for k, v in six.iteritems(configpk.code_config(conf, source_code,file_key="factor_file")):
            if k in conf['whitelist']:
                configpk.deep_update(v, conf[k])

    mod_configs = config_args.pop('mod_configs', [])
    for k, v in mod_configs:
        key = 'mod__{}'.format(k.replace('.', '__'))
        config_args[key] = configpk.mod_config_value_parse(v)
    if click_type:
        for k, v in six.iteritems(config_args):
            if v is None:
                continue
            if k == 'base__accounts' and not v:
                continue

            key_path = k.split('__')
            sub_dict = conf
            for p in key_path[:-1]:
                if p not in sub_dict:
                    sub_dict[p] = {}
                sub_dict = sub_dict[p]
            sub_dict[key_path[-1]] = v
    else:
        deep_update(config_args, conf)
    config = RqAttrDict(conf)
    configpk.set_locale(config.extra.locale)

    def _to_date(v):
        return pd.Timestamp(v).date()

    config.base.start_date = _to_date(config.base.start_date)
    config.base.end_date = _to_date(config.base.end_date)

    if config.base.data_bundle_path is None:
        rqalpha_path = "~/../.rqalpha"
        config.base.data_bundle_path = os.path.join(os.path.expanduser(rqalpha_path), "bundle")
    logger.DATETIME_FORMAT = "%Y-%m-%d"

    return config

'''
def code_config(config, source_code=None,file_key="factor_file"):
    try:
        if source_code is None:
            _file = config["base"]["factor_file"]
            if os.path.basename(_file).split(".")[1] == "ipynb":
                import io
                from nbformat import read
                from IPython.core.interactiveshell import InteractiveShell
                with io.open(_file, 'r', encoding='utf-8') as f:
                    nb = read(f, 4)
                try:
                    for cell in nb.cells:
                        if cell.cell_type == 'code':
                            source_code = InteractiveShell.instance().input_transformer_manager.transform_cell(cell.source)
                            # print(type(source_code),source_code)
                            # print(type(cell.source),cell.source)
                            break  # 只取第一个cell,
                except Exception as e:
                    system_log.error(_(u"load ipynb {file} failed, exception: {e}").format(file=_file,e=e))
            else:
                with codecs.open(_file, encoding="utf-8") as f:
                    source_code = f.read()
                    # print(source_code)

        # FIXME: hardcode for parametric mod
        def noop(*args, **kwargs):
            pass
        scope = {'define_parameter': noop}

        code = compile(source_code,config["base"]["factor_file"] , 'exec')
        print(code)
        six.exec_(code, scope)

        return scope.get('__config__', {})
    except Exception as e:
        system_log.error(_(u"in parse_user_config, exception: {e}").format(e=e))
        return {}
'''