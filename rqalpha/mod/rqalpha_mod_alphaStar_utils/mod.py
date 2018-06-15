#coding=utf-8

"""
@author: evilXu
@file: mod.py
@time: 2018/2/28 16:59
@description: 
"""

from rqalpha.interface import AbstractMod
from rqalpha.utils.logger import system_log,user_system_log
import pandas as pd
from rqalpha.api import *
import pandas as pd
import statsmodels.api as sm
from scipy.stats.mstats import winsorize
import numpy as np
from tqdm import tqdm
from scipy.linalg import eigh
from sklearn.covariance import ledoit_wolf

class UtilsMod(AbstractMod):
    def __init__(self):
        self._inject_api()

    def start_up(self, env, mod_config):
        system_log.debug("UtilsMod.start_up,config:{0}",mod_config)

    def tear_down(self, code, exception=None):
        pass
        # print(">>> AlphaHDataMode.tear_down")

    def _inject_api(self):
        from rqalpha import export_as_api
        from rqalpha.execution_context import ExecutionContext
        from rqalpha.const import EXECUTION_PHASE

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def equalWeight_order(tobe_holding_codes=[], context=None,accountname= None):
            user_system_log.info("equalWeight_order:{}",str(tobe_holding_codes))
            account = context.get_account(accountname)
            if len(tobe_holding_codes) < 1:
                for code, pos in context.portfolio.positions.items():
                    if pos.sellable > 0:
                        account.order_shares(code, -1 * pos.sellable)
                return
                #     print("positions",context.portfolio.positions)
            _target_percent = round(1.0 / len(tobe_holding_codes), 2)
            _targets = set(tobe_holding_codes)
            _tobe_sell = [pos for code, pos in context.portfolio.positions.items() if code not in _targets]
            for pos in _tobe_sell:
                if pos.sellable > 0:
                    account.order_shares(pos.order_book_id, -1 * pos.sellable)
            for code in tobe_holding_codes:
                _cash_percent = round(account.cash / account.total_value, 2)
                _real_percent = min(_cash_percent, _target_percent)
                #         print(_acount.cash,_acount.total_value,_cash_percent,_real_percent)
                if _real_percent > 0:
                    account.order_pct_to(code, _real_percent)
            return

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def winsorized(df, limit=(0.01, 0.01)):
            '''
            winsorize input dataframe by the upper and lower limit percent
            :param df: feature  in the format of pandas-Dataframe
            :param limit: pct that will be cut at both sides
            :return: winsorized dataframe
            '''
            df = df.dropna(how='all')
            col = df.columns
            newdf = df.apply(lambda x: pd.Series(winsorize(x.dropna().values, limit), index=x.dropna().index), axis=1)
            newdf = newdf.reindex(columns=col)
            return newdf

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def orthogonalize(pn):
            '''
            orthogonalize features in the order of input Panel items
            :param pn: features in the format of pandas-Panel; items:feature name,major_axis: datetime,minor_axis:stock name
            :return: orthogonalized features
            '''
            newpn = pd.Panel(items=pn.items, major_axis=pn.major_axis, minor_axis=pn.minor_axis)
            factorlist = pn.items
            newpn.iloc[0] = pn.iloc[0]
            for i in range(1, len(factorlist)):
                factor = pn.iloc[i].dropna(how='all')
                prefactor = newpn.iloc[:i]
                prefactor = prefactor.loc[:, (prefactor.count(axis=0) == i).sum(axis=1) > 0, :]
                factor, prefactor = getSameIdx(factor, prefactor)
                orghFunc = lambda x: sm.OLS(x, prefactor.loc[:, x.name], missing='drop', hasconst=False).fit().resid
                newfactor = factor.apply(orghFunc, axis=1)
                newpn.iloc[i] = newfactor

            return newpn

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def neutralized(df, formatted_path, useLFLO=True, useSec=True, useBeta=False):
            '''
            neutralize the input feature by LFLO/Sector/Beta (optional),defalt using LFLO and Sector to neutralize
            :param df: feature  in the format of pandas-Dataframe to be neutralized
            :param formatted_path: the path that save the LFLO/Sector/Beta data
            :param useLFLO: if use LFLO to neutralize, set to True
            :param useSec: if use Sector to neutralize, set to True
            :param useBeta: if use Beta to neutralize, set to True
            :return: neutralized dataframe
            '''
            swSec = pd.read_pickle(formatted_path + 'eqSec_10303.pkl').astype('float32').reindex(minor_axis=df.index)
            LFLO = pd.read_pickle(formatted_path + 'LFLO.pkl').reindex(df.index).dropna(how='all')
            beta = pd.read_pickle(formatted_path + 'beta_40_all.pkl').reindex(df.index).dropna(how='all')
            newdf = df.copy().dropna(how='all')
            resdf = pd.DataFrame(columns=df.columns)
            validindex = swSec.minor_axis.intersection(LFLO.index).intersection(newdf.index).intersection(beta.index)
            betaxfunc = lambda date: np.vstack((beta.loc[date, newdf.columns].values))
            LFLOxfunc = lambda date: np.vstack((LFLO.loc[date, newdf.columns].values))
            secxfunc = lambda date: swSec.loc[:, newdf.columns, date].fillna(0).values
            xfunclist = list(filter(None, [betaxfunc if useBeta else None, LFLOxfunc if useLFLO else None,
                                           secxfunc if useSec else None]))
            xfunc = lambda date: np.hstack((func(date) for func in xfunclist))
            for date in tqdm(validindex):
                x = xfunc(date)
                resid = sm.OLS(newdf.loc[date], x, missing='drop').fit().resid
                resdf.loc[date] = resid
            resdf = resdf.reindex(index=df.index, columns=df.columns)
            return resdf

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def getSameIdx(a, b):
            '''
            get a,b with index that a/b both have
            :param a: dataframe/panel
            :param b: dataframe/panel
            :return: a,b with same index
            '''

            def _gettype(x):
                if isinstance(x, pd.DataFrame):
                    return 'df'
                elif isinstance(x, pd.Panel):
                    return 'pn'
                else:
                    raise ValueError

            atype = _gettype(a)
            btype = _gettype(b)

            def _getidx(type, x):
                if type == 'df':
                    return x.index
                elif type == 'pn':
                    return x.major_axis

            compindex1 = _getidx(atype, a)
            compindex2 = _getidx(btype, b)
            valididx = compindex1.intersection(compindex2)

            def _getnewx(type, idx, x):
                if type == 'df':
                    return x.loc[idx]
                elif type == 'pn':
                    return x.loc[:, idx, :]

            newa = _getnewx(atype, valididx, a)
            newb = _getnewx(btype, valididx, b)
            return newa, newb

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def getRiskRet_barra(excessret, riskfactor, perffilepath, formatted_path):
            '''
            get risk factor return using Barra model
            :param excessret: stock excess daily return in the format of Pandas-Datafraem
            :param riskfactor: risk factors in the format of pandas-Panel;items:feature name,major_axis: datetime,minor_axis:stock name
            :param perffilepath: path to save risk factor return and specific return
            :param formatted_path: path to load marketvalue data
            :return: risk factor return, specifit return, original riskfactor
            '''
            try:
                riskRet = pd.read_pickle(perffilepath + 'riskRet.pkl')
                specificRet = pd.read_pickle(perffilepath + 'specificRet.pkl')
                newriskfactor = pd.read_pickle(perffilepath + 'newriskfactor.pkl')
            except FileNotFoundError:
                riskRet = pd.DataFrame(columns=list(riskfactor.items))
                specificRet = pd.Panel(items=list(riskfactor.items), minor_axis=excessret.columns)
                newriskfactor = pd.DataFrame(columns=excessret.columns)
            if riskRet.index.max() < excessret.index.max():
                MV = pd.read_pickle(formatted_path + 'LFLO.pkl')
                updateriskRet = pd.DataFrame(columns=list(riskfactor.items))
                updatenewriskfactor = pd.Panel(items=list(riskfactor.items), minor_axis=excessret.columns)
                updatespecificRet = pd.DataFrame(columns=excessret.columns)
                shiftriskfactor = riskfactor.shift(1, axis=1)
                shareidx = excessret.index.intersection(shiftriskfactor.major_axis)
                for date in tqdm(shareidx):
                    y = excessret.loc[date]
                    x = shiftriskfactor.loc[:, date, :].dropna(how='all')
                    wgt = MV.loc[date].fillna(0)
                    if x.dropna().empty:
                        continue
                    sharestock = y.index.intersection(x.index).intersection(wgt.index)
                    model = sm.WLS(y.loc[sharestock], x.loc[sharestock], wgt.loc[sharestock], missing='drop').fit()
                    updateriskRet.loc[date] = model.params
                    updatespecificRet.loc[date] = model.resid
                    updatenewriskfactor.loc[:, date, :] = x
                riskRet = pd.concat([riskRet, updateriskRet]).groupby(level=0).first()
                specificRet = pd.concat([specificRet, updatespecificRet]).groupby(level=0).first()
                newriskfactor = pd.concat(
                    [newriskfactor, updatenewriskfactor.loc[:, newriskfactor.major_axis.max():, :].iloc[:, 1:, :]],
                    axis=1)
                riskRet.to_pickle(perffilepath + 'riskRet.pkl')
                specificRet.to_pickle(perffilepath + 'specificRet.pkl')
                newriskfactor.to_pickle(perffilepath + 'newriskfactor.pkl')
            return riskRet, specificRet, newriskfactor

        @export_as_api
        @ExecutionContext.enforce_phase(EXECUTION_PHASE.ON_INIT,
                                        EXECUTION_PHASE.BEFORE_TRADING,
                                        EXECUTION_PHASE.ON_BAR,
                                        EXECUTION_PHASE.AFTER_TRADING,
                                        EXECUTION_PHASE.SCHEDULED)
        def getEstCov(dailyret, limit=0.99):
            '''
            estimate covariance by shrinkage(ledoit wolf method) and eigenvalue compression

            :param dailyret: dailyret in the format of pandas-Dataframe(index:datetime, columns:stock names)
            :param limit: perchange of info to be kept during the eigenvalue compression
            :return: estimatd covariance
            '''
            T, N = dailyret.shape
            shrinkSigma, _ = ledoit_wolf(dailyret, assume_centered=False, block_size=int(N / 5))  # LS-lediot
            # shrinkSigma=dailyret.cov().values # empirical cov
            stddiag_I = 1. / np.sqrt(np.diag(shrinkSigma + 1e-10))
            corr = shrinkSigma * stddiag_I * stddiag_I.reshape(-1, 1)
            ewmastd = dailyret.ewm(alpha=0.90).std().iloc[-1].values
            estCov = corr * ewmastd * (ewmastd.reshape(-1, 1))
            e, v = eigh(estCov, eigvals=(N - 100, N - 1))
            e, v = e[::-1], v[::, ::-1]
            e = pd.Series(e).astype(np.float64)
            v = pd.DataFrame(v).astype(np.float64)
            selected_e = (e.pow(2).cumsum() / e.pow(2).sum()) <= limit
            part1idx = selected_e.replace(False, np.nan).dropna().index
            part2idx = selected_e.replace(True, np.nan).dropna().index
            if len(part1idx) == 0:
                part1idx = [0]
                part2idx = part2idx[1:]
            selectedeigenVector = v.loc[:, part1idx]
            eigenValueCov = np.diag(e.loc[part1idx].values)
            residcov = v.loc[:, part2idx].pow(2).mul(e.loc[part2idx]).sum(axis=1)
            # estCov_spec=selectedeigenVector.dot(eigenValueCov).dot(selectedeigenVector.T)+residcov
            return selectedeigenVector, eigenValueCov, residcov