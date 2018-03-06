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
@click.option('-i', '--data-init-date', 'base__data_init_date', type=Date(),help="The init date to calculate and persist factor data")
@click.option('-e', '--end-date', 'base__end_date', type=Date())
@click.option( '--adminDB', 'base__adminDB')
@click.option( '--sourcePath', 'base__sourcePath',help="path where factor code files exist")
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def dailyProcess(**kwargs):
    '''
    [alphaStar_mgr] dailyProcess
    '''
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    obj = TaskMgr(db=config.base.adminDB, sourcePath=config.base.sourcePath,
                  fdataPath=config.mod.alphaStar_factors.factor_data_path)
    _pPath = config.base.data_bundle_path.replace("\\bundle","")
    update_bundle(data_bundle_path=_pPath,confirm=False)
    obj.runFactors(dataInitDt=_to_date(config.base.data_init_date),enddt=config.base.end_date)
    obj.runStrategys(config=config)

@cli.command()
@click.help_option('-h', '--help')
@click.option('-i', '--data-init-date', 'mod__alphaStar_factors__factor_data_init_date', type=Date(),help="The init date to calculate and persist factor data")
@click.option('-e', '--end-date', 'base__end_date', type=Date())
@click.option( '--fname', 'base__fname')
@click.option( '--adminDB', 'base__adminDB')
@click.option( '--sourcePath', 'base__sourcePath',help="path where factor code files exist")
@click.option( '--fDataPath', 'mod__alphaStar_factors__factor_data_path',help="path where factor data files exist")
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callAFactor(**kwargs):
    '''
    [alphaStar_mgr] callAFactor
    '''
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    obj = TaskMgr(db=config.base.adminDB, sourcePath=config.base.sourcePath, fdataPath=config.mod.alphaStar_factors.factor_data_path)
    _dataInitDt = config.mod.alphaStar_factors.factor_data_init_date
    _endDt = config.base.end_date
    # _endDt = _dataInitDt if _endDt is None else _endDt
    obj.runAFactor(fname=config.base.fname, dataInitDt=_to_date(_dataInitDt), endDt=_to_date(_endDt),fconf = config.mod.alphaStar_factors.extra)

@cli.command()
@click.help_option('-h', '--help')
@click.option('-i', '--data-init-date', 'data_init_date', type=Date(),help="The init date to calculate and persist factor data")
@click.option('-e', '--end-date', 'end_date', type=Date())
@click.option( '--adminDB', 'adminDB')
@click.option( '--sourcePath', 'sourcePath',help="path where factor code files exist")
@click.option( '--fDataPath', 'fDataPath',help="path where factor data files exist")
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callFactors(**kwargs):
    '''
    [alphaStar_mgr] callFactors
    '''
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    obj = TaskMgr(db=config.base.adminDB, sourcePath=config.base.sourcePath, fdataPath=config.mod.alphaStar_factors.factor_data_path)
    _dataInitDt = config.mod.alphaStar_factors.factor_data_init_date
    _endDt = config.base.end_date
    # _endDt = _dataInitDt if _endDt is None else _endDt
    obj.runFactors(dataInitDt=_to_date(_dataInitDt), enddt=_to_date(_endDt),fconf = config.mod.alphaStar_factors.extra)

@cli.command()
@click.help_option('-h', '--help')
# -- Base Configuration
@click.option('-e', '--end-date', 'base__end_date', type=Date())
@click.option( '--sname', 'base__sname')
# @click.option( '--tgw-account', 'base__tgw_account')
@click.option( '--adminDB', 'base__adminDB')
@click.option( '--sourcePath', 'base__sourcePath',help="path where factor code files exist")
# -- Extra Configuration
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callAStrategy(**kwargs):
    '''
    [alphaStar_mgr] callAStrategy
    '''
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
@click.option( '--adminDB', 'base__adminDB')
@click.option( '--sourcePath', 'base__sourcePath',help="path where factor code files exist")
# -- Extra Configuration
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callStrategys(**kwargs):
    '''
    [alphaStar_mgr] callStrategys
    '''
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
@click.option( '--adminDB', 'adminDB')
def addUser(**kwargs):
    '''
    [alphaStar_mgr] addUser
    '''
    ret = Admin(db = kwargs.get('adminDB', None))\
        .addUser(uname=kwargs.get('uname', None),passwd=kwargs.get('passwd', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def addAdminUser(**kwargs):
    '''
    [alphaStar_mgr] addAdminUser
    '''
    ret = Admin(db = kwargs.get('adminDB', None)) \
        .addAdminUser(passwd=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--uname', 'uname')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def delUser(**kwargs):
    '''
    [alphaStar_mgr] delUser
    '''
    ret = Admin(db = kwargs.get('adminDB', None))\
        .delUser(uname=kwargs.get('uname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--uname', 'uname')
@click.option( '--fname', 'fname')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def registerFactor(**kwargs):
    '''
    [alphaStar_mgr] registerFactor
    '''
    ret = Admin(db = kwargs.get('adminDB', None))\
        .registerFactor(fname = kwargs.get('fname', None),uname=kwargs.get('uname', None), adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--fname', 'fname')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def delFactor(**kwargs):
    '''
    [alphaStar_mgr] delFactor
    '''
    ret = Admin(db = kwargs.get('adminDB', None))\
        .delFactor(fname = kwargs.get('fname', None), adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--uname', 'uname')
@click.option('--fname', 'fname')
@click.option('--admin-passwd', 'admin_passwd')
@click.option('--adminDB', 'adminDB')
def registerAndPublishFactor(**kwargs):
    '''
    [alphaStar_mgr] registerAndPublishFactor
    '''
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .registerAndPublishFactor(fname=kwargs.get('fname', None), uname=kwargs.get('uname', None),
                        adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--fname', 'fname')
@click.option('--admin-passwd', 'admin_passwd')
@click.option('--adminDB', 'adminDB')
def publishFactor(**kwargs):
    '''
    [alphaStar_mgr] publishFactor
    '''
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .publishFactor(fname=kwargs.get('fname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--fname', 'fname')
@click.option('--admin-passwd', 'admin_passwd')
@click.option('--adminDB', 'adminDB')
def unPublishFactor(**kwargs):
    '''
    [alphaStar_mgr] unPublishFactor
    '''
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .unPublishFactor(fname=kwargs.get('fname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--adminDB', 'adminDB')
def getPublishedFactors(**kwargs):
    '''
    [alphaStar_mgr] getPublishedFactors
    '''
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .getPublishedFactors()
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--uname', 'uname')
@click.option( '--sname', 'sname')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def registerStrategy(**kwargs):
    '''
    [alphaStar_mgr] registerStrategy
    '''
    ret = Admin(db = kwargs.get('adminDB', None))\
        .registerStrategy(sname = kwargs.get('sname', None),uname=kwargs.get('uname', None), adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--sname', 'sname')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def delStrategy(**kwargs):
    '''
    [alphaStar_mgr] delStrategy
    '''
    ret = Admin(db = kwargs.get('adminDB', None))\
        .delStrategy(sname = kwargs.get('sname', None), adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--uname', 'uname')
@click.option('--sname', 'sname')
@click.option('--account', 'tgw_account')
@click.option('--admin-passwd', 'admin_passwd')
@click.option('--adminDB', 'adminDB')
def registerAndPublishStrategy(**kwargs):
    '''
    [alphaStar_mgr] registerAndPublishStrategy
    '''
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .registerAndPublishStrategy(sname=kwargs.get('sname', None), uname=kwargs.get('uname', None),
                        adminPass=kwargs.get('admin_passwd', None),accountID=kwargs.get('tgw_account', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--sname', 'sname')
@click.option('--account', 'tgw_account')
@click.option('--admin-passwd', 'admin_passwd')
@click.option('--adminDB', 'adminDB')
def publishStrategy(**kwargs):
    '''
    [alphaStar_mgr] publishStrategy
    '''
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .publishStrategy(sname=kwargs.get('sname', None),adminPass=kwargs.get('admin_passwd', None),accountID=kwargs.get('tgw_account', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--sname', 'sname')
@click.option('--admin-passwd', 'admin_passwd')
@click.option('--adminDB', 'adminDB')
def unPublishStrategy(**kwargs):
    '''
    [alphaStar_mgr] unPublishStrategy
    '''
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .unPublishStrategy(sname=kwargs.get('sname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--adminDB', 'adminDB')
def getPublishedStrategys(**kwargs):
    '''
    [alphaStar_mgr] getPublishedStrategys
    '''
    ret = Admin(db=kwargs.get('adminDB', None)).getPublishedStrategys()
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
