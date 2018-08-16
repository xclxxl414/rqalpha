#coding=utf-8

"""
@author: evilXu
@file: jy_data_source.py
@time: 2017/6/14 9:46
@description: 
"""

# import numpy as np
import pandas as pd
from rqalpha.data.base_data_source import BaseDataSource
from rqalpha.data.adjust import *
from rqalpha.utils.datetime_func import *
from rqalpha.model.instrument import Instrument
from rqalpha.utils.py2 import lru_cache
from datetime import *
from rqalpha.utils.logger import system_log, user_print

class JYDSError(Exception):
    def __init__(self,value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)


class JYDataSource(BaseDataSource):
    def __init__(self, path):
        # super(AlphaHDataSource, self).__init__(path)
        self._secumain =  dict([(i.symbol,i)for i in self._initSecuMain()])
        self._indexmainRaw = self._initIndexMain()
        self._indexmain = dict([(i.symbol,i)for i in self._indexmainRaw])
        self._industryMain = {"__".join([i["name"],str(i['level']),i["standard"]]):i for i in self._initIndustry()}
        # print([item for item in self._industryMain.values() if item['standard'] == "CITIC" and item['level']==1] )

    @lru_cache(None)
    def get_dividend(self, order_book_id):
        '''
        :param order_book_id:
        :return: 分红记录[(信息发布日，登记日，除权日，到账日，金额，基准股数),],没有分过红的返回None
        '''
        _dtype = np.dtype([('announcement_date', '<u4'), ('book_closure_date', '<u4')
                              , ('ex_dividend_date', '<u4'), ('payable_date', '<u4')
                              , ('dividend_cash_before_tax', '<f8'), ('round_lot', '<u4')])

        _res = self._dataServer.post(suburl="/v/dividend",
                                     data={"codes": [order_book_id]})
        try:
            if _res.get("status") != 1:
                raise JYDSError("get_dividend failed:" + str(_res.get("status")) + _res.get("msg"))
            _midRes = []
            if _res.get("datas")[0] is None:
                return None
            for item in _res.get("datas")[0]:
                try:
                    _midRes.append(
                        (item['impPubDate'].replace("-","") if item['impPubDate'] is not None else "00000000"
                         , item['rightRegDate'].replace("-","") if item['rightRegDate'] is not None else "00000000"
                         , item['exDiviDate'].replace("-","") if item['exDiviDate'] is not None else "00000000"
                         , item['toAccountDate'].replace("-","") if item['toAccountDate'] is not None else "00000000"
                         , item['cash'], 10))
                except Exception as e:
                    # system_log.debug(_(u"strategy run successfully, normal exit"))
                    system_log.warn("get_dividend for {} error:{},{}",order_book_id,e, item)
            x = np.array(_midRes, dtype=_dtype)
            return x
        except Exception as e:
            raise JYDSError("get_dividend failed:" + str(e))

    @lru_cache(None)
    def get_split(self, order_book_id):
        _dtype = np.dtype([('ex_date', '<u8'), ('split_factor', '<f8')])

        _res = self._dataServer.post(suburl="/v/split",
                                     data={"codes": [order_book_id]})
        try:
            if _res.get("status") != 1:
                raise JYDSError("get_split failed:" + str(_res.get("status")) + _res.get("msg"))
            _midRes = []
            if _res.get("datas")[0] is None:
                return None
            for item in _res.get("datas")[0]:
                try:
                    # print (item)
                    _midRes.append((item['exDiviDate'].replace("-", "")+"000000" if item['exDiviDate'] is not None else "00000000000000"
                                    , item['value']))
                except Exception as e:
                    system_log.warn("get_split for {} error:{},{}", order_book_id, e, item)
            x = np.array(_midRes, dtype=_dtype)
            return x
        except Exception as e:
            raise JYDSError("get_split failed:" + str(e))

    def get_trading_minutes_for(self, order_book_id, trading_dt):
        raise NotImplementedError

    def get_trading_calendar(self):
        '''
        交易日列表
        :return: DatetimeIndex(['2005-01-04', '2005-01-05', '2005-01-06', '2005-01-07',
               ...
               '2017-12-28', '2017-12-29'],
              dtype='datetime64[ns]', length=3159, freq=None)
        '''
        # _res = pd.DatetimeIndex([datetime(2015,1,1),datetime(2016,1,1)])
        dateb = datetime(1990, 11, 26)
        datee = datetime.now()
        _res = self._dataServer.post(suburl="/test/getrading_dt",data={"dateB": dateb.strftime("%Y-%m-%d"), "dateE": datee.strftime("%Y-%m-%d")})
        try:
            # print(_res)
            if _res.get("status") != 1:
                raise JYDSError("get_trading_calendar failed:" + str(_res.get("status")) + _res.get("msg"))
            return pd.DatetimeIndex(_res.get("datas"))
        except Exception as e:
            raise JYDSError("get_trading_calendar failed:" + str(e))

    def _initSecuMain(self):
        '''
        初始化secumain, indexmain.industrymain
        :return:
        '''
        _res = self._dataServer.post(suburl="/main/getsecu",data = {})
        try:
            # print(_res)
            if _res.get("status") != 1:
                raise JYDSError("init secumain failed:%s,%s" % (_res.get("status"), _res.get("msg")))
            _ret = []
            # print(len(_res.get("datas")))
            for item in _res.get("datas"):
                _ret.append(Instrument({"symbol":item.get("abbr"), "type":"CS","abbrev_symbol":item.get("abbrspelling")
                                           ,"listed_date":item.get("listeddate").split(" ")[0]
                                           ,"de_listed_date":item.get("delisteddate").split(" ")[0] if item.get("delisteddate") is not None else "2099-12-31"
                                           , "board_type":item.get('listedsector'),"order_book_id":item.get("code")
                                           , "exchange":item.get("market")
                                           , "status":self._secuStatus(item.get("listedtstate"))
                                           , "round_lot":100.0}))
            return _ret
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Exception("init secumain failed:%s,%s, exception:%s"%(_res.get("status"),_res.get("msg"),e))

    def _secuStatus(self,status = 1):
        if 1 == status:
            return "Active"
        else:
            return "Delisted"

    def _initIndexMain(self):
        '''
        初始化secumain, indexmain.industrymain
        :return:
        '''
        _res = self._dataServer.post(suburl="/main/getindex",data = {})
        try:
            if _res.get("status") != 1:
                raise JYDSError("init indexmain failed:%s,%s" % (_res.get("status"), _res.get("msg")))
            _ret = []
            # print(len(_res.get("datas")))
            for item in _res.get("datas"):
                _listedDate =  item.get("pubdate") if item.get("pubdate") is not None else item.get("listeddate")
                # if item.get("code") == "000300.SH":
                #     print(item.get("code"))
                _ret.append(Instrument({"symbol":item.get("abbr"), "type":"INDX","abbrev_symbol":""
                                           ,"listed_date":_listedDate.split(" ")[0] if _listedDate is not None else "0000-00-00"
                                           , "board_type":'MainBoard',"order_book_id":item.get("code")
                                           , "exchange":item.get("code").split(".")[1]
                                           , "status":"Active"
                                            ,"de_listed_date":item.get("enddate").split(" ")[0] if item.get("enddate") is not None else "0000-00-00"
                                           , "round_lot":100.0}))
            return _ret
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Exception("init indexmain failed:%s,%s, exception:%s"%(_res.get("status"),_res.get("msg"),e))

    def _initIndustry(self):
        '''
        初始化secumain, indexmain.industrymain
        :return:
        '''
        _res = self._dataServer.post(suburl="/main/getindustry",data = {})
        try:
            if _res.get("status") != 1:
                raise JYDSError("init industry failed:%s,%s" % (_res.get("status"), _res.get("msg")))
            _ret = []
            for item in _res.get("datas"):
                _ret.append(item)
            return _ret
        except JYDSError as aE:
            raise aE
        except Exception as e:
            raise JYDSError("init industry failed:%s,%s, exception:%s" % (_res.get("status"), _res.get("msg"), e))

    def get_all_instruments(self):
        '''
        :return: list of Instruments
        '''
        # print(len(self._secumain),len(self._indexmain))
        return list(self._secumain.values()) + self._indexmainRaw

    def is_suspended(self, order_book_id, dates):
        # return [False for i in dates]
        _res = []
        for dt in dates:
            _suspendedADay = self._all_suspendeds().get(dt.strftime("%y-%m-%d"))
            if _suspendedADay is None:
                _res.append(False)
            else:
                _set = set([i.get("code") for i in _suspendedADay])
                _res.append(True if order_book_id in _set else False)
        return _res

    def is_st_stock(self, order_book_id, dates):
        _res = []
        for dt in dates:
            _set = set(self.st_components(dt))
            _res.append(True if order_book_id in _set else False)
        return _res

    @DeprecationWarning
    #只用于history_bars
    def get_ex_cum_factor(self, order_book_id):
        '''
        累计复权因子，基类base_data_source该方法没有考虑分红
        :param order_book_id:
        :return:<class 'numpy.ndarray'> [(20100303000000, 1.0) (20110428000000, 2.0)] [('start_date', '<u8'), ('ex_cum_factor', '<f8')]
        '''
        data = {"code": order_book_id}
        _res = self._dataServer.post(suburl="/adjustactor", data=data)
        _dtype = np.dtype([('start_date', '<u8'), ('ex_cum_factor', '<f8')])

        try:
            x = np.array([() for item in _res], dtype=_dtype)
            return x
        except Exception as e:
            return None

    @lru_cache(None)
    def _all_day_bars_of_CS(self,instrument,adjust = "none"):
        if adjust == "none":
            _type = "normal"
        elif adjust == "post":
            _type = "after"
        else:
            raise NotImplementedError
        data = {"codes": [instrument.order_book_id], "dateB": instrument.listed_date.strftime("%Y-%m-%d")
            , "dateE": (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d"), "type": _type}
        _dtype = np.dtype([('datetime', '<u8'), ('open', '<f8'), ('close', '<f8'), ('high', '<f8')
                              , ('low', '<f8'), ('volume', '<f8'), ('total_turnover', '<u8')
                              , ('limit_up', '<f8'), ('limit_down', '<f8')])
        data.update({"fields": ["open", "close", "high", "low", "volume", "amount", "preclose"]})
        _res = self._dataServer.post(suburl="/history/getbar", data=data)
        if _res.get("status") != 1:
            raise JYDSError("get_bar for %s failed,status:%s,%s" % (
            instrument.order_book_id, _res.get("status"), _res.get("msg")))
        _datas = _res.get("datas")
        _midRes = []
        for i in range(len(_res.get("dates"))):
            _dt = datetime.strptime(_res.get("dates")[i], "%Y-%m-%d")
            _gap = 0.1 if not self.is_st_stock(instrument.order_book_id, [_dt])[0] else 0.05
            # a = [_datas[j][i] for j in range(7)]
            # print(_dt, a)
            try:
                _midRes.append((
                               _dt.strftime("%Y%m%d%H%M%S"), _datas[0][i], _datas[1][i], _datas[2][i], _datas[3][i],
                               _datas[4][i], _datas[5][i]
                               , round((1.0 + _gap) * _datas[6][i], 2), round((1.0 - _gap) * _datas[6][i], 2)))
            except Exception as e:
                system_log.warn("_all_day_bars data error,code:{},date:{},ochlvap:{} {} {} {} {} {}"
                                , instrument.order_book_id, _dt
                                , _datas[0][i], _datas[1][i], _datas[2][i], _datas[3][i], _datas[4][i],
                                _datas[5][i], _datas[6][i])
        x = np.array(_midRes, dtype=_dtype)
        return x

    @lru_cache(None)
    def _all_day_bars_of_INDX(self,instrument):
        data = {"codes": [instrument.order_book_id], "dateB": instrument.listed_date.strftime("%Y-%m-%d")
            , "dateE": (datetime.now() + timedelta(days=-1)).strftime("%Y-%m-%d"), "type": "normal"}
        _dtype = np.dtype([('datetime', '<u8'), ('open', '<f8'), ('close', '<f8'), ('high', '<f8')
                              , ('low', '<f8'), ('volume', '<f8'), ('total_turnover', '<u8')])
        data.update({"fields": ["open", "close", "high", "low", "volume", "amount"]})
        _res = self._dataServer.post(suburl="/history/getindexbar", data=data)
        if _res.get("status") != 1:
            raise JYDSError("getindexbar for %s failed,status:%s,%s" % (
            instrument.order_book_id, _res.get("status"), _res.get("msg")))
        # print(_res)
        _datas = _res.get("datas")
        # print(_res)
        _midRes = []
        for i in range(len(_res.get("dates"))):
            _dt = datetime.strptime(_res.get("dates")[i], "%Y-%m-%d")
            if _datas[0][i] is None or _datas[1][i] is None or _datas[2][i] is None \
                    or _datas[3][i] is None or _datas[4][i] is None or _datas[5][i] is None:
                system_log.warn("_all_day_bars data error,code:{},date:{},ochlvap:{} {} {} {} {}"
                                , instrument.order_book_id, _dt
                                , _datas[0][i], _datas[1][i], _datas[2][i], _datas[3][i], _datas[4][i],
                                _datas[5][i])
                continue
            _midRes.append((_dt.strftime("%Y%m%d%H%M%S"), _datas[0][i], _datas[1][i], _datas[2][i], _datas[3][i],
                            _datas[4][i], _datas[5][i]))
        x = np.array(_midRes, dtype=_dtype)
        return x

    # @lru_cache(None)
    def _all_day_bars_of(self, instrument):
        if "CS" == instrument.type:
            return self._all_day_bars_of_CS(instrument)
        elif "INDX" == instrument.type:
            return self._all_day_bars_of_INDX(instrument)
        else:
            raise NotImplementedError

    #暂时用不上
    def history_bars(self, instrument, bar_count, frequency, fields, dt,
                     skip_suspended=True, include_now=False,
                     adjust_type='pre', adjust_orig=None):
        if frequency != '1d':
            raise NotImplementedError
        system_log.debug("history_bars:",instrument.order_book_id,bar_count,frequency,fields,dt,skip_suspended,include_now,adjust_type,adjust_orig)
        if instrument.type == "CS":
            if adjust_type == "none":
                if skip_suspended:
                    bars = self._filtered_day_bars(instrument)
                else:
                    bars = self._all_day_bars_of(instrument)
            else:
                bars = self._all_day_bars_of_CS(instrument,adjust_type)
                if skip_suspended:
                    bars = bars[bars['volume'] > 0]
        else:
            bars = self._all_day_bars_of(instrument)

        if bars is None or not self._are_fields_valid(fields, bars.dtype.names):
            return None

        dt = np.uint64(convert_date_to_int(dt))
        i = bars['datetime'].searchsorted(dt, side='right')
        left = i - bar_count if i >= bar_count else 0
        bars = bars[left:i]
        return bars if fields is None else bars[fields]

    def available_data_range(self, frequency):
        if frequency == '1d':
            _instrument = self._indexmain.get("上证指数")
            _bars = self._filtered_day_bars(_instrument)
            s, e = _bars[0]['datetime'],_bars[-1]['datetime']
            return convert_int_to_date(s).date(), convert_int_to_date(e).date()
        raise NotImplementedError

    def get_factor(self,code_list = None, tdate = None, factor_list=[]):
        '''
        :param code_list:股票代码列表，若为None,表示全部股票
        :param tdate:交易日， 表示取哪一天的指标数据
        :param factor_list:指标列表，包含指标及其参数信息
        :return:
        '''
        _data = {"name":"getfactor",
                 "codes":code_list,
                 "dateB":tdate.strftime("%Y-%m-%d"),
                 "factors":[{"name":item.get("name"),"params":item.get("parameters")} for item in factor_list]
                 }
        _res_data = self._dataServer.post(suburl="/test/getfactor",data=_data)
        try:
            if 1 != _res_data.get("status"):
                system_log.error("getfactors failed,status:{}",_res_data.get("status"))
                return None
            _d = _res_data.get("datas")
            _res = []
            # print(_res_data)
            for i in range(0,len(code_list)):
                _res.append(dict([(k,_d[k][i]) for k in range(0,len(factor_list))]))
            # print(_res)
            return pd.DataFrame(data=_res,index=code_list)
        except Exception as e:
            system_log.error("get_factor failed:{}",e)
            return None

    def get_factor_index(self,code_list = None, tdate = None, factor_list=[],name_list = None):
        '''
        :param code_list:股票代码列表，若为None,表示全部股票
        :param tdate:交易日， 表示取哪一天的指标数据
        :param factor_list:指标列表，包含指标及其参数信息
        :return:
        '''
        if code_list is not None:
            _codes = code_list
        elif name_list is not None:
            _codes = [self._indexmain.get(i).order_book_id for i in name_list]
        else:
            return None
        _data = {"name":"getfactor",
                 "codes":_codes,
                 "dateB":tdate.strftime("%Y-%m-%d"),
                 "factors":[{"name":item.get("name"),"params":item.get("parameters")} for item in factor_list]
                 }
        _res_data = self._dataServer.post(suburl="/test/getindexfactor",data=_data)
        try:
            if 1 != _res_data.get("status"):
                system_log.error("get_factor_index failed,status:{}",_res_data.get("status"))
                return None
            _d = _res_data.get("datas")
            _res = []
            # print(_res_data)
            for i in range(0,len(_res_data.get("codes"))):
                _res.append(dict([(k,_d[k][i]) for k in range(0,len(factor_list))]))
            # print(_res)
            return pd.DataFrame(data=_res,index=code_list)
        except Exception as e:
            system_log.error("get_factor_index failed:{}",e)
            return None

    def index_components(self,date=None,code = None,name = None):
        if code is not None:
            _indCode = code
        else:
            _indCode = self._indexmain.get(name)
            if _indCode is None:
                raise JYDSError("index not exist:%s" % (name))
            _indCode = _indCode.order_book_id
        _data = {"codes":[_indCode],"dateB":date.strftime("%Y-%m-%d"),"dateE":date.strftime("%Y-%m-%d")}
        _res_data = self._dataServer.post(suburl="/component/getindex", data=_data)
        try:
            # print("index_components:",_res_data)
            if 1 != _res_data.get("status"):
                raise JYDSError("index_components failed,status:%s" % (_res_data.get("status")))
            return _res_data.get("datas")[0][0]
        except JYDSError as aE:
            raise aE
        except Exception as e:
            raise JYDSError("index_components failed,get exception:%s" % (str(e)))

    def industry_components(self,date=None,code = None,name = None,level = None,standard = None):
        if code is not None:
            _indCode = code
        else:
            if standard == "SW_2014" and date < datetime(2014,1,1):
                _std = "SW"
            else:
                _std = standard
            # print (self._industryMain.keys())
            _indCode = self._industryMain.get("__".join([name,str(level),_std]))
            if _indCode is None:
                raise JYDSError("industry not exist,name:%s,level:%s,standard:%s" % (name, level, standard))
            _indCode = _indCode['industrycode']
        _data = {"codes":[_indCode],"dateB":date.strftime("%Y-%m-%d"),"dateE":date.strftime("%Y-%m-%d")}
        _res_data = self._dataServer.post(suburl="/component/getind", data=_data)
        try:
            # print(_res_data)
            if 1 != _res_data.get("status"):
                raise JYDSError("industry_components failed,status:%s" % (_res_data.get("status")))
            return _res_data.get("datas")[0][0]
        except JYDSError as aE:
            raise aE
        except Exception as e:
            raise JYDSError("industry_components failed,get exception:%s" % (str(e)))

    #TODO
    def margin_components(self,date = None):#融资融券票
        import random
        return [i.order_book_id for i in self.get_all_instruments() if i.type == "CS" and random.random() < 0.5]

    def st_components(self, date=None):
        # print("st_components:",date)
        _res = self._all_st().get(date.strftime("%Y-%m-%d"))
        if _res is None:
            return []
        return [i.get("code") for i in _res]

    @lru_cache(None)
    def _all_st(self):
        _data = {"dateB": datetime(1990,1,1).strftime("%Y-%m-%d"), "dateE": datetime.now().strftime("%Y-%m-%d")}
        _res_data = self._dataServer.post(suburl="/v/ST", data=_data)
        try:
            if 1 != _res_data.get("status"):
                raise JYDSError("st_components failed,status:%s" % (_res_data.get("status")))
            _datas = _res_data.get("datas")
            _res = {}
            # print(_res_data)
            for i in _datas:
                if i.get("value") is None or i.get('value') == 0:
                    continue
                if i.get("date") not in _res:
                    _res[i.get("date")] = []
                _res[i.get("date")].append(i)
            return _res
        except JYDSError as aE:
            raise aE
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise JYDSError("st_components failed,get exception:%s" % (str(e)))

    @lru_cache(None)
    def _all_suspendeds(self):
        _data = {"dateB": datetime(1990, 1, 1).strftime("%Y-%m-%d"), "dateE": datetime.now().strftime("%Y-%m-%d")}
        _res_data = self._dataServer.post(suburl="/v/suspended", data=_data)
        try:
            if 1 != _res_data.get("status"):
                raise JYDSError("_suspended_components failed,status:%s" % (_res_data.get("status")))
            _datas = _res_data.get("datas")
            _res = {}
            # print(_res_data)
            for i in _datas:
                if i.get("value") is None or i.get('value') != 1:
                    continue
                if i.get("date") not in _res:
                    _res[i.get("date")] = []
                _res[i.get("date")].append(i)
            return _res
        except JYDSError as aE:
            raise aE
        except Exception as e:
            raise JYDSError("_suspendeds failed,get exception:%s" % (str(e)))

    #TODO
    def get_risk_free_rate(self, start_date, end_date):
        return 0.015
