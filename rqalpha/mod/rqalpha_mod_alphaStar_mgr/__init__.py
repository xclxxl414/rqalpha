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
@click.option('-s', '--start-date', 'start_date', type=Date())
@click.option('-e', '--end-date', 'end_date', type=Date())
@click.option( '--fname', 'fname')
@click.option( '--adminDB', 'adminDB')
@click.option( '--ipyPath', 'ipyPath')
@click.option( '--fDataPath', 'fDataPath')
def callAFactor(**kwargs):
    obj = TaskMgr(db=kwargs.get('adminDB', None),ipynbPath=kwargs.get('ipyPath', None),fdataPath=kwargs.get('fDataPath', None))
    _startDt = kwargs.get('start_date', None)
    _endDt = kwargs.get('end_date', None)
    # _endDt = _startDt if _endDt is None else _endDt
    obj.runAFactor(fname=kwargs.get('fname', None),startDt =_to_date(_startDt),endDt=_to_date(_endDt))

@cli.command()
@click.help_option('-h', '--help')
@click.option('-s', '--start-date', 'start_date', type=Date())
@click.option('-e', '--end-date', 'end_date', type=Date())
@click.option( '--adminDB', 'adminDB')
@click.option( '--ipyPath', 'ipyPath')
@click.option( '--fDataPath', 'fDataPath')
def callFactors(**kwargs):
    obj = TaskMgr(db=kwargs.get('adminDB', None),ipynbPath=kwargs.get('ipyPath', None),fdataPath=kwargs.get('fDataPath', None))
    _startDt = kwargs.get('start_date', None)
    _endDt = kwargs.get('end_date', None)
    # _endDt = _startDt if _endDt is None else _endDt
    obj.runFactors(startdt =_to_date(_startDt),enddt=_to_date(_endDt))

@cli.command()
@click.help_option('-h', '--help')
# -- Base Configuration
@click.option('-e', '--end-date', 'base__end_date', type=Date())
@click.option( '--sname', 'base__sname')
@click.option( '--tgw-account', 'base__tgw_account')
@click.option( '--adminDB', 'base__adminDB')
@click.option( '--ipyPath', 'base__ipyPath')
# @click.option( '--fDataPath', 'base__fDataPath')
# -- Extra Configuration
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callAStrategy(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    obj = TaskMgr(db=config.base.adminDB, ipynbPath=config.base.ipyPath, fdataPath=config.mod.alphaStar_factors.factor_data_path)
    obj.runAStrategy(sname=config.base.sname,config=config)

@cli.command()
@click.help_option('-h', '--help')
# -- Base Configuration
@click.option('-e', '--end-date', 'base__end_date', type=Date())
@click.option( '--tgw-account', 'base__tgw_account')
@click.option( '--adminDB', 'base__adminDB')
@click.option( '--ipyPath', 'base__ipyPath')
# @click.option( '--fDataPath', 'base__fDataPath')
# -- Extra Configuration
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
def callStrategys(**kwargs):
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')

    config = _parse_config(kwargs, config_path)
    obj = TaskMgr(db=config.base.adminDB, ipynbPath=config.base.ipyPath, fdataPath=config.mod.alphaStar_factors.factor_data_path)
    obj.runStrategys(config=config)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--uname', 'uname')
@click.option( '--passwd', 'passwd')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def addUser(**kwargs):
    ret = Admin(db = kwargs.get('adminDB', None))\
        .addUser(uname=kwargs.get('uname', None),passwd=kwargs.get('passwd', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def addAdminUser(**kwargs):
    ret = Admin(db = kwargs.get('adminDB', None)) \
        .addAdminUser(passwd=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--uname', 'uname')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def delUser(**kwargs):
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
    ret = Admin(db = kwargs.get('adminDB', None))\
        .registerFactor(fname = kwargs.get('fname', None),uname=kwargs.get('uname', None), adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--fname', 'fname')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def delFactor(**kwargs):
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
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .publishFactor(fname=kwargs.get('fname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--fname', 'fname')
@click.option('--admin-passwd', 'admin_passwd')
@click.option('--adminDB', 'adminDB')
def unPublishFactor(**kwargs):
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .unPublishFactor(fname=kwargs.get('fname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--adminDB', 'adminDB')
def getPublishedFactors(**kwargs):
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
    ret = Admin(db = kwargs.get('adminDB', None))\
        .registerStrategy(sname = kwargs.get('sname', None),uname=kwargs.get('uname', None), adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option( '--sname', 'sname')
@click.option( '--admin-passwd', 'admin_passwd')
@click.option( '--adminDB', 'adminDB')
def delStrategy(**kwargs):
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
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .publishStrategy(sname=kwargs.get('sname', None),adminPass=kwargs.get('admin_passwd', None),accountID=kwargs.get('tgw_account', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--sname', 'sname')
@click.option('--admin-passwd', 'admin_passwd')
@click.option('--adminDB', 'adminDB')
def unPublishStrategy(**kwargs):
    ret = Admin(db=kwargs.get('adminDB', None)) \
        .unPublishStrategy(sname=kwargs.get('sname', None),adminPass=kwargs.get('admin_passwd', None))
    print(ret)

@cli.command()
@click.help_option('-h', '--help')
@click.option('--adminDB', 'adminDB')
def getPublishedStrategys(**kwargs):
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
