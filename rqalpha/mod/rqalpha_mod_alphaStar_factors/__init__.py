#coding=utf-8

"""
@author: evilXu
@file: __init__.py.py
@time: 2017/10/10 15:42
@description: 
"""

import click
from rqalpha import cli
from .evaluate import  *
from rqalpha.utils.click_helper import Date

__config__ = {
    #因子数据路径
    "factor_data_path": None,
    #因子数据起始日
    "factor_data_init_date": "2017-01-01",
}

def load_ipython_extension(ipython):
    """call by ipython"""
    ipython.register_magic_function(evaluate_ipython_cell, 'line_cell', 'evaluate')

def load_mod():
    from .mod import FactorDataMod
    return FactorDataMod()

@cli.command()
@click.help_option('-h', '--help')
# -- Base Configuration
@click.option('-d', '--data-bundle-path', 'base__data_bundle_path', type=click.Path(exists=True))
@click.option('-f', '--factor_file', 'base__factor_file', type=click.Path(exists=True))
@click.option('-s', '--start-date', 'base__start_date', type=Date())
@click.option('-e', '--end-date', 'base__end_date', type=Date())
@click.option('-rt', '--run-type', 'base__run_type', type=click.Choice(['p', 'r']))#, default="r") # realtime compute data or precompute data
@click.option('--source-code', 'base__source_code')
@click.option( '--fname', 'base__factor_name')
# -- Extra Configuration
@click.option('-l', '--log-level', 'extra__log_level', type=click.Choice(['verbose', 'debug', 'info', 'error', 'none']))
@click.option('--disable-user-system-log', 'extra__user_system_log_disabled', is_flag=True, help='disable user system log stdout')
@click.option('--disable-user-log', 'extra__user_log_disabled', is_flag=True, help='disable user log stdout')
@click.option('--logger', 'extra__logger', nargs=2, multiple=True, help='config logger, e.g. --logger system_log debug')
# @click.option("--dividend-reinvestment", "extra__dividend_reinvestment", is_flag=True, help="enable dividend reinvestment")
@click.option('--config', 'config_path', type=click.STRING, help="config file path")
# -- Mod Configuration
@click.option('-mc', '--mod-config', 'mod_configs', nargs=2, multiple=True, type=click.STRING, help="mod extra config")
def evaluate(**kwargs):
    '''
    [alphaStar_factors] evaluate factors
    '''
    config_path = kwargs.get('config_path', None)
    if config_path is not None:
        config_path = os.path.abspath(config_path)
        kwargs.pop('config_path')
    if not kwargs.get('base__securities', None):
        kwargs.pop('base__securities', None)

    source_code = kwargs.get("base__source_code")
    cfg = parse_config(kwargs, config_path=config_path, click_type=True, source_code=source_code)
    if hasattr(cfg.base, 'name'):
        fname = cfg.base.fname
    elif hasattr(cfg.base, 'factor_file'):
        fname = os.path.basename(cfg.base.factor_file).split(".")[0]
    results = evaluateRun(fname, cfg)

def evaluate_ipython_cell(line, cell=None):
    from rqalpha.utils.py2 import clear_all_cached_functions
    clear_all_cached_functions()
    args = line.split()
    try:
        # It raise exception every time
        evaluate.main(args, standalone_mode=True)
    except SystemExit as e:
        pass

G_defaultConfig = os.path.join(os.path.dirname(__file__), '../../', 'config_factor.yml')
def evaluate_file(factor_file_path="", config=None,config_file = G_defaultConfig):
    from .evaluate import evaluateRun
    from rqalpha.utils.py2 import clear_all_cached_functions

    if config is None:
        config = {
            "base": {
                "factor_file": factor_file_path
            }
        }
    else:
        assert isinstance(config, dict)
        if "base" in config:
            config["base"]["factor_file"] = factor_file_path
        else:
            config["base"] = {
                "factor_file": factor_file_path
            }
    config = parse_config(config,config_path=config_file)
    fname = os.path.basename(factor_file_path).split(".")[0]
    clear_all_cached_functions()
    evaluateRun(fname,config)


if __name__ == '__main__':
    cli(obj={})