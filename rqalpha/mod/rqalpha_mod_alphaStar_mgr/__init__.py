#coding=utf-8

"""
@author: evilXu
@file: __init__.py
@time: 2017/12/28 17:45
@description:
"""

import click
from rqalpha import cli
from rqalpha.utils.click_helper import Date
import os
import rqalpha.utils.config as configpk
from rqalpha.utils import RqAttrDict
from rqalpha.utils.dict_func import deep_update
import six
import pandas as pd
from .admin import Admin
from .taskMgr import TaskMgr
from datetime import *
from rqalpha.interface import AbstractMod
from rqalpha.main import update_bundle

class MgrMod(AbstractMod):
    '''
    do nothing
    '''
    def __init__(self):
        pass

    def start_up(self, env, mod_config):
        pass

    def tear_down(self, code, exception=None):
        pass

def load_mod():
    return MgrMod()

@cli.command()
@click.help_option('-h', '--help')
# @click.option('-i', '--data-init-date', 'mod__alphaStar_factors__factor_data_init_date', type=Date(),help="The init date to calculate and persist factor data")
# @click.option('-e', '--end-date', 'base__end_date', type=Date())
# @click.option( '--adminDB', 'base__adminDB')
# @click.option( '--sourcePath', 'base__sourcePath',help="path where factor code files exist")
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def dailyProcess(**kwargs):
    '''
    [alphaStar_mgr] dailyProcess,update_bundle and callFactors
    '''
    _dailyProcess(**kwargs)

def _dailyProcess(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    _now = datetime.now()

    #verify tradingday
    config.base.end_date = _now.date()
    from rqalpha.data.base_data_source import BaseDataSource
    from rqalpha.data.data_proxy import DataProxy
    from .taskMgr import StrategyRunner
    _dp = DataProxy(BaseDataSource(config.base.data_bundle_path))
    StrategyRunner.verifyLatestTradingDay(_dp,config)

    #check bundle update
    _file = os.path.join(config.base.data_bundle_path,"stocks.bcolz")
    mtime_bundle = datetime.fromtimestamp(os.stat(_file).st_mtime)
    _now = datetime.now()
    _now_base = _now.replace(hour=19,minute=15,second=0,microsecond=0)
    _delta = _now - mtime_bundle
    if _delta.days < 0:
        pass
    elif _delta.days < 1:
        if (_now-_now_base).total_seconds() > 600 and mtime_bundle.day != _now.day:
            _pPath = config.base.data_bundle_path.replace("bundle", "")
            update_bundle(data_bundle_path=_pPath, confirm=False)
        else:
            pass
    else:
        _pPath = config.base.data_bundle_path.replace("bundle","")
        update_bundle(data_bundle_path=_pPath,confirm=False)

    #run factor
    obj = TaskMgr(db=config.base.adminDB, sourcePath=config.base.sourcePath,
                  fdataPath=config.mod.alphaStar_factors.factor_data_path)

    obj.runFactors(dataInitDt=_to_date(config.mod.alphaStar_factors.factor_data_init_date),enddt=config.base.end_date,modconf= config.mod.alphaStar_factors)
    # obj.runStrategys(config=config)

@cli.command()
@click.help_option('-h', '--help')
@click.option('-i', '--data-init-date', 'mod__alphaStar_factors__factor_data_init_date', type=Date(),help="The init date to calculate and persist factor data")
@click.option('-e', '--end-date', 'base__end_date', type=Date())
@click.option( '--fname', 'base__fname')
# @click.option( '--adminDB', 'base__adminDB')
# @click.option( '--sourcePath', 'base__sourcePath',help="path where factor code files exist")
# @click.option( '--fDataPath', 'mod__alphaStar_factors__factor_data_path',help="path where factor data files exist")
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callAFactor(**kwargs):
    '''
    [alphaStar_mgr] callAFactor
    '''
    _callAFactor(**kwargs)

def _callAFactor(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    obj = TaskMgr(db=config.base.adminDB, sourcePath=config.base.sourcePath, fdataPath=config.mod.alphaStar_factors.factor_data_path)
    _dataInitDt = config.mod.alphaStar_factors.factor_data_init_date
    _endDt = config.base.end_date
    # _endDt = _dataInitDt if _endDt is None else _endDt
    obj.runAFactor(fname=config.base.fname, dataInitDt=_to_date(_dataInitDt), endDt=_to_date(_endDt),
                   modconf= config.mod.alphaStar_factors)

@cli.command()
@click.help_option('-h', '--help')
@click.option('-i', '--data-init-date', 'mod__alphaStar_factors__factor_data_init_date', type=Date(),help="The init date to calculate and persist factor data")
@click.option('-e', '--end-date', 'base__end_date', type=Date())
# @click.option( '--adminDB', 'base__adminDB')
# @click.option( '--sourcePath', 'base__sourcePath',help="path where factor code files exist")
# @click.option( '--fDataPath', 'mod__alphaStar_factors__factor_data_path',help="path where factor data files exist")
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callFactors(**kwargs):
    '''
    [alphaStar_mgr] callFactors
    '''
    _callFactors(**kwargs)

def _callFactors(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    obj = TaskMgr(db=config.base.adminDB, sourcePath=config.base.sourcePath, fdataPath=config.mod.alphaStar_factors.factor_data_path)
    _dataInitDt = config.mod.alphaStar_factors.factor_data_init_date
    _endDt = config.base.end_date
    # _endDt = _dataInitDt if _endDt is None else _endDt
    obj.runFactors(dataInitDt=_to_date(_dataInitDt), enddt=_to_date(_endDt),
                   modconf= config.mod.alphaStar_factors)

@cli.command()
@click.help_option('-h', '--help')
# -- Base Configuration
@click.option('-e', '--end-date', 'base__end_date', type=Date())
@click.option( '--sname', 'base__sname')
# @click.option( '--tgw-account', 'base__tgw_account')
# @click.option( '--adminDB', 'base__adminDB')
# @click.option( '--sourcePath', 'base__sourcePath',help="path where factor code files exist")
# -- Extra Configuration
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callAStrategy(**kwargs):
    '''
    [alphaStar_mgr] callAStrategy
    '''
    _callAStrategy(**kwargs)

def _callAStrategy(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    obj = TaskMgr(db=config.base.adminDB, sourcePath=config.base.sourcePath, fdataPath=config.mod.alphaStar_factors.factor_data_path)
    obj.runAStrategy(sname=config.base.sname,config=config)

@cli.command()
@click.help_option('-h', '--help')
# -- Base Configuration
@click.option('-e', '--end-date', 'base__end_date', type=Date())
# @click.option( '--tgw-account', 'base__tgw_account')
# @click.option( '--adminDB', 'base__adminDB')
# @click.option( '--sourcePath', 'base__sourcePath',help="path where factor code files exist")
# -- Extra Configuration
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callStrategys(**kwargs):
    '''
    [alphaStar_mgr] callStrategys
    '''
    _callStrategys(**kwargs)

def _callStrategys(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    obj = TaskMgr(db=config.base.adminDB, sourcePath=config.base.sourcePath, fdataPath=config.mod.alphaStar_factors.factor_data_path)
    obj.runStrategys(config=config)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--uname', 'uname')
@click.option( '--passwd', 'passwd')
@click.option( '--admin-passwd', 'admin_passwd')
# @click.option( '--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def addUser(**kwargs):
    '''
    [alphaStar_mgr] addUser
    '''
    _addUser(**kwargs)

def _addUser(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db = config.base.adminDB)\
        .addUser(uname=kwargs.get('uname', None),passwd=kwargs.get('passwd', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--admin-passwd', 'admin_passwd')
# @click.option( '--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def addAdminUser(**kwargs):
    '''
    [alphaStar_mgr] addAdminUser
    '''
    _addAdminUser(**kwargs)

def _addAdminUser(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db = config.base.adminDB) \
        .addAdminUser(passwd=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--uname', 'uname')
@click.option( '--admin-passwd', 'admin_passwd')
# @click.option( '--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def delUser(**kwargs):
    '''
    [alphaStar_mgr] delUser
    '''
    _delUser(**kwargs)

def _delUser(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db = config.base.adminDB)\
        .delUser(uname=kwargs.get('uname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--uname', 'uname')
@click.option( '--fname', 'fname')
@click.option( '--admin-passwd', 'admin_passwd')
# @click.option( '--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def registerFactor(**kwargs):
    '''
    [alphaStar_mgr] registerFactor
    '''
    _registerFactor(**kwargs)

def _registerFactor(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db = config.base.adminDB)\
        .registerFactor(fname = kwargs.get('fname', None),uname=kwargs.get('uname', None), adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--fname', 'fname')
@click.option( '--admin-passwd', 'admin_passwd')
# @click.option( '--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def delFactor(**kwargs):
    '''
    [alphaStar_mgr] delFactor
    '''
    _delFactor(**kwargs)

def _delFactor(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db = config.base.adminDB)\
        .delFactor(fname = kwargs.get('fname', None), adminPass=kwargs.get('admin_passwd', None),datapath=config.mod.alphaStar_factors.factor_data_path)
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--uname', 'uname')
@click.option('--fname', 'fname')
@click.option('--admin-passwd', 'admin_passwd')
# @click.option('--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def registerAndPublishFactor(**kwargs):
    '''
    [alphaStar_mgr] registerAndPublishFactor
    '''
    _registerAndPublishFactor(**kwargs)

def _registerAndPublishFactor(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db=config.base.adminDB) \
        .registerAndPublishFactor(fname=kwargs.get('fname', None), uname=kwargs.get('uname', None),
                        adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--fname', 'fname')
@click.option('--admin-passwd', 'admin_passwd')
# @click.option('--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def publishFactor(**kwargs):
    '''
    [alphaStar_mgr] publishFactor
    '''
    _publishFactor(**kwargs)

def _publishFactor(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db=config.base.adminDB) \
        .publishFactor(fname=kwargs.get('fname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--fname', 'fname')
@click.option('--admin-passwd', 'admin_passwd')
# @click.option('--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def unPublishFactor(**kwargs):
    '''
    [alphaStar_mgr] unPublishFactor
    '''
    _unPublishFactor(**kwargs)

def _unPublishFactor(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db=config.base.adminDB) \
        .unPublishFactor(fname=kwargs.get('fname', None),adminPass=kwargs.get('admin_passwd', None),datapath=config.mod.alphaStar_factors.factor_data_path)
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
# @click.option('--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def getPublishedFactors(**kwargs):
    '''
    [alphaStar_mgr] getPublishedFactors
    '''
    _getPublishedFactors(**kwargs)

def _getPublishedFactors(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db=config.base.adminDB) \
        .getPublishedFactors()
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--uname', 'uname')
@click.option( '--sname', 'sname')
@click.option( '--admin-passwd', 'admin_passwd')
# @click.option( '--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def registerStrategy(**kwargs):
    '''
    [alphaStar_mgr] registerStrategy
    '''
    _registerStrategy(**kwargs)

def _registerStrategy(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db = config.base.adminDB)\
        .registerStrategy(sname = kwargs.get('sname', None),uname=kwargs.get('uname', None), adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--sname', 'sname')
@click.option( '--admin-passwd', 'admin_passwd')
# @click.option( '--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def delStrategy(**kwargs):
    '''
    [alphaStar_mgr] delStrategy
    '''
    _delStrategy(**kwargs)

def _delStrategy(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db = config.base.adminDB)\
        .delStrategy(sname = kwargs.get('sname', None), adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--uname', 'uname')
@click.option('--sname', 'sname')
@click.option('--account', 'tgw_account')
@click.option('--admin-passwd', 'admin_passwd')
# @click.option('--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def registerAndPublishStrategy(**kwargs):
    '''
    [alphaStar_mgr] registerAndPublishStrategy
    '''
    _registerAndPublishStrategy(**kwargs)

def _registerAndPublishStrategy(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db=config.base.adminDB) \
        .registerAndPublishStrategy(sname=kwargs.get('sname', None), uname=kwargs.get('uname', None),
                        adminPass=kwargs.get('admin_passwd', None),accountID=kwargs.get('tgw_account', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--sname', 'sname')
@click.option('--account', 'tgw_account')
@click.option('--admin-passwd', 'admin_passwd')
# @click.option('--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def publishStrategy(**kwargs):
    '''
    [alphaStar_mgr] publishStrategy
    '''
    _publishStrategy(kwargs)

def _publishStrategy(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db=config.base.adminDB) \
        .publishStrategy(sname=kwargs.get('sname', None),adminPass=kwargs.get('admin_passwd', None),accountID=kwargs.get('tgw_account', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--sname', 'sname')
@click.option('--admin-passwd', 'admin_passwd')
# @click.option('--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def unPublishStrategy(**kwargs):
    '''
    [alphaStar_mgr] unPublishStrategy
    '''
    _unPublishStrategy(kwargs)

def _unPublishStrategy(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db=config.base.adminDB) \
        .unPublishStrategy(sname=kwargs.get('sname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
# @click.option('--adminDB', 'adminDB')
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def getPublishedStrategys(**kwargs):
    '''
    [alphaStar_mgr] getPublishedStrategys
    '''
    _getPublishedStrategys(kwargs)

def _getPublishedStrategys(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    ret = Admin(db=config.base.adminDB).getPublishedStrategys()
    print(ret)

def _parse_config(config_args, config_path=None, click_type = True):
    conf = configpk.load_config(config_path)

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

    config.base.start_date = _to_date(config.base.start_date)
    config.base.end_date = _to_date(config.base.end_date)

    return config

def _to_date(v):
    return pd.Timestamp(v).date() if v is not None else None

if __name__ == '__main__':
    cli(obj={})
