#coding=utf-8

"""
@author: evilXu
@file: tgw_broker.py
@time: 2018/1/4 16:44
@description: 
"""

import numpy as np
from copy import copy
from rqalpha.interface import AbstractBroker
from rqalpha.utils.logger import system_log
from rqalpha.events import EVENT, Event
from rqalpha.const import BAR_STATUS, SIDE, ORDER_TYPE,POSITION_EFFECT
from rqalpha.const import DEFAULT_ACCOUNT_TYPE
from rqalpha.model.base_position import Positions
from rqalpha.model.portfolio import Portfolio
from datetime import *
from rqalpha.model.trade import Trade
from rqalpha.utils.i18n import gettext as _
import requests
import json
import base64
import time
import hmac
from enum import Enum

class TgwBroker(AbstractBroker):
    def __init__(self, env, mod_config):
        self._env = env
        self.mod_config = mod_config
        self._tgwAccont = None
        self._env.event_bus.add_listener(EVENT.AFTER_TRADING, self.afterTrading)

    def setAccount(self,mod_config):
        self.mod_config = mod_config
        self._tgwAccont = TgwAccount(tradeUrl=mod_config.tgwurl, tickUrl=mod_config.tickurl
                                     , secretId_TICK=mod_config.secretId_TICK, secretKey_TICK=mod_config.secretKey_TICK
                                     , secretId=mod_config.secretId, secretKey=mod_config.secretKey,uid=mod_config.uid,accountid = mod_config.accountid)

    def afterTrading(self,event):
        self._tgwAccont.afterTrading()

    def get_portfolio(self):
        accounts = {}
        config = self._env.config
        units = 0

        account_type = "STOCK"
        starting_cash = self.mod_config.starting_cash

        account_model = self._env.get_account_model(account_type)
        position_model = self._env.get_position_model(account_type)
        positions = Positions(position_model)

        _hodings = self._tgwAccont.getHoldsList(holdingType=HoldingType.Holding)
        for item in _hodings:
            code = self._tgwAccont.codeConvert_Oddly2Rqalpha(item['secucode'],item['Market'])
            instrument = self._env.get_instrument(code)
            if instrument is None:
                raise RuntimeError(_(u'invalid order book id {} in initial positions').format(code))
            if not instrument.listing:
                raise RuntimeError(
                    _(u'instrument {} in initial positions is not listing').format(code))

            price = self._getLatestPrice(code)
            # trade = self._fake_trade(code, item['HoldingVolume'], price)
            if code not in positions:
                obj = position_model(code)
                obj.set_state({"order_book_id":code,"quantity":item['HoldingVolume']
                    ,"avg_price":item['HoldingCost'],"non_closable":0
                    ,"frozen":item['HoldingVolume'] - item['CanSellVolume'],"transaction_cost":0})
                positions[code] = obj
                # positions[code].apply_trade(trade)
            else:
                system_log.error("tgw position err,duplicate,account:{},code:{}",self.mod_config.combid,code)
            # FIXME
            positions[code]._last_price = price

        _earning = self._tgwAccont.earningsData()
        _availableCash = _earning.get("BalanceAmount")
        account = account_model(_availableCash, positions)
        accounts[account_type] = account
        # print("get_portfolio",account.cash,account.total_value,positions)
        return Portfolio(config.base.start_date, account.total_value/starting_cash, starting_cash, accounts)

    def _getLatestPrice(self,code = ""):
        _res = self._tgwAccont.getTick(codeList=[code])
        return _res[0]['NowPrice']

    def _fake_trade(self,order_book_id, quantity, price):
        return Trade.__from_create__(0, price, abs(quantity),
                                     SIDE.BUY if quantity > 0 else SIDE.SELL,
                                     POSITION_EFFECT.OPEN, order_book_id)

    def get_open_orders(self, order_book_id=None):
        return []

    def submit_order(self, order):
        account = self._env.get_account(order.order_book_id)
        self._env.event_bus.publish_event(Event(EVENT.ORDER_PENDING_NEW, account=account, order=copy(order)))
        if order.is_final():
            return
        order.active()
        self._env.event_bus.publish_event(Event(EVENT.ORDER_CREATION_PASS, account=account, order=copy(order)))
        self._tgwAccont.orderPending(order.order_book_id, order.quantity if order.side == SIDE.BUY else -1 * order.quantity)

    def cancel_order(self, order):
        system_log.error(_(u"cancel_order function is not supported in signal mode"))
        return None

class HoldingType(Enum):
    All = 1
    Holding = 2
    History = 3

class TgwAccount():
    def __init__(self, tradeUrl = "http://www.tgwtest.com/tgwapi/myapp/Trade"
                 ,tickUrl = "http://tgw360.com/webapi/myapp/WxInterface/GetQueInfo"
                 ,secretId_TICK="dianziqianzhang",secretKey_TICK="B123456789",secretId="commonkey"
                 ,secretKey="TGW_COMMONKEY",uid = None,accountid = None): #):
        # print(tradeUrl,tickUrl,secretId_TICK,secretKey_TICK,secretId,secretKey)
        self._tradeRootUrl = tradeUrl
        self._apiInfo = {"secretId": secretId, "secretKey": secretKey}
        self._uid = uid
        self._accountid = accountid
        self._tickUrl = tickUrl
        self._tickApiInfo = {"secretId": secretId_TICK, "secretKey": secretKey_TICK}
        # 市场类型  65537【上海】  131073【深圳】  65545【上证指数】  131081【深证，创业】
        self._marketMap_oddly_STD = {65537: "XSHG", 131073: "XSHE",131075:"OF"}
        self._marketMap_STD_oddly = {v: k for k, v in self._marketMap_oddly_STD.items()}
        self._openOrders = []

    def codeConvert_Oddly2Rqalpha(self,code,market):
        # print(code,market)
        return "%06d"%(code)+"."+ self._marketMap_oddly_STD.get(market)

    def codeConvert_Rqalpha2Oddly(self,code):
        a = code.split(".")
        return a[0],self._marketMap_STD_oddly.get(a[1])

    def _post(self,url,_param = None):
        r = requests.post(url=url, data=_param)
        if r.status_code != requests.codes.ok:
            print("api: %s ,not 200!"%(_param,r))
            return None
        _res = r.json()
        if _res.get("errno") != 0:
            print("api: %s ,failed,msg:%s,%s" % (_param, _res.get("errno"),_res.get("errmsg")))
            return None
        return r.json().get("data")

    def _get(self,url,params=None):
        try:
            r = requests.get(url=url,params=params,timeout=5)
            if r.status_code != requests.codes.ok:
                print("api: %s ,not 200!:%s" % (params, r))
                return None
            return r.json()
        except requests.exceptions.Timeout as et:
            print("api: %s ,timeout" % (params))
            return None
        except Exception as e:
            print("api: %s ,error:%s" % (params, e))
            return None

    def getTick(self,codeList = []):
        _param = {"secretId":self._tickApiInfo.get("secretId"), "time":str(round(time.time()))}
        _codeList = [{"SecuCode":code.split(".")[0],"MarketType":self._marketMap_STD_oddly.get(code.split(".")[1])} for code in codeList]
        _param.update({"SecuCodeList":json.dumps(_codeList)})
        _secretStr = "&".join([str(k)+"="+str(v) for k,v in sorted(_param.items(),key=lambda x:x[0])])
        ss = hmac.new(key = bytes(self._tickApiInfo['secretKey'], "utf8"), msg=bytes(_secretStr, "utf8"), digestmod="sha1").digest()
        s1 = base64.b64encode(ss)
        _param.update({"sign":s1})
        _res = self._get(self._tickUrl,_param)
        a = _res.get('data').get("info").get("GridDataList")
        for item in a:item.update({"SecuCode":self.codeConvert_Oddly2Rqalpha(item['SecuCode'],item['MarketType']),"MarketType":self._marketMap_oddly_STD.get(item['MarketType'])})
        return a

    def _getHoldsList_APage(self, holdingType = 1, uid=None, combid = None, pageNo = 0, perPage = 10):
        _param = {"secretId":self._apiInfo.get("secretId")
                     ,"time":str(round(time.time()))
                     ,"ServiceID":uid
                     ,"CombID":combid
                     ,"HoldsType":holdingType
                     ,"BeginIndex": perPage * pageNo, "RecordCount":perPage}
        _secretStr = "&".join([str(k)+"="+str(v) for k,v in sorted(_param.items(),key=lambda x:x[0])])
        ss = hmac.new(key = bytes(self._apiInfo['secretKey'], "utf8"), msg=bytes(_secretStr, "utf8"), digestmod="sha1").digest()
        s1 = base64.b64encode(ss)
        _param.update({"sign":s1})
        try:
            _res = self._get(self._tradeRootUrl + "/GetHoldsList",_param)
            if _res is None or _res['data']["code"] != 0:
                system_log.error("GetHoldsList failed:{0},{1},pageInfo:{2},{3},return code：{4}", uid, combid, pageNo, perPage,_res['data']["code"])
                return None
            return _res["data"]["info"]
        except Exception as e:
            system_log.error("GetHoldsList failed:{0},{1},pageInfo:{2},{3},info:{4}",uid,combid,pageNo,perPage,e)
            return None

    def getHoldsList(self,holdingType = HoldingType.Holding):
        perPage = 100
        idx = 0
        _res = []
        while True:
            try:
                _resAPage = self._getHoldsList_APage(holdingType = holdingType.value, uid=self._uid, combid=self._accountid, pageNo=idx, perPage=perPage)
                if _resAPage is None:
                    break
                # print(_resAPage)
                _res += _resAPage.get("PositionList")
                if len(_resAPage.get("PositionList")) < perPage:
                    # all result return
                    break
                idx += 1
            except Exception as e:
                import traceback
                traceback.print_exc()
                break
        return _res

    def earningsData(self):
        _param = {"secretId":self._apiInfo.get("secretId")
                     ,"time":str(round(time.time()))
                     ,"ServiceID":self._uid
                     ,"CombID":self._accountid}
        _secretStr = "&".join([str(k)+"="+str(v) for k,v in sorted(_param.items(),key=lambda x:x[0])])
        ss = hmac.new(key = bytes(self._apiInfo['secretKey'], "utf8"), msg=bytes(_secretStr, "utf8"), digestmod="sha1").digest()
        s1 = base64.b64encode(ss)
        _param.update({"sign":s1})
        try:
            _res = self._get(self._tradeRootUrl + "/EarningsData", _param)
            if _res is None or _res['data']["code"] != 0:
                system_log.error("EarningsData failed:{0},{1},return code：{2}", self._uid, self._accountid, _res['date']["code"])
                return None
            return _res["data"]["info"]
        except Exception as e:
            system_log.error("EarningsData failed:{0},{1},info:{2}",self._uid,self._accountid,e)
            return None

    def _BatchDelteGateOrder(self, userType = 2, uid=None, accountid = None, combid = None, DeltegateList = None, Periods = 1): #
        _param = {"UserType":userType,
                 "UserID":uid,
                  "AccountID":accountid,
                  "DeltegateList":DeltegateList,
                  "Periods":Periods,
                 "secretId":self._apiInfo.get("secretId")
                     ,"time":str(round(time.time()))
                     ,"CombD":combid}
        _secretStr = "&".join([str(k)+"="+str(v) for k,v in sorted(_param.items(),key=lambda x:x[0])])
        ss = hmac.new(key = bytes(self._apiInfo['secretKey'], "utf8"), msg=bytes(_secretStr, "utf8"), digestmod="sha1").digest()
        s1 = base64.b64encode(ss)
        _param.update({"sign":s1})
        try:
            _res = self._get(self._tradeRootUrl + "/BatchDelteGateOrder", _param)
            # print(_res)
            if _res is None or _res['data']["code"] != 0:
                system_log.error("BatchDelteGateOrder failed:{},{},return ：{},{}", uid, combid, _res['data']["code"],_res)
                return None
            return _res["data"]["info"]
        except Exception as e:
            system_log.error("BatchDelteGateOrder failed:{},{},info:{}",uid,combid,e)
            import traceback
            traceback.print_exc()
            return None

    def orderPending(self,code,volume):
        self._openOrders.append((code,volume))

    def afterTrading(self):
        system_log.info("push order:{} to TGW account:{} ", str(self._openOrders),self._accountid)
        self._orderShare(self._openOrders)
        self._openOrders = []

    def _orderShare(self, code_Cnt=[]):
        _orderList = []
        _ticks = self.getTick([code for code,volume in code_Cnt])
        _code2Ticks = dict((item['SecuCode'],item) for item in _ticks)
        for code,volume in code_Cnt:
            _tgwcode,market = self.codeConvert_Rqalpha2Oddly(code)
            _orderList.append({"SecuCode": _tgwcode, "Market": market, "Volume": abs(volume)
                            , "Price": _code2Ticks.get(code)['NowPrice'], "Direct": 1 if volume > 0 else 2,"EntrustType": 2})
        return self._BatchDelteGateOrder(uid=self._uid, accountid=self._accountid, combid=self._accountid,
                                         DeltegateList=json.dumps(_orderList))

    @DeprecationWarning
    def orderToPercent(self,code_weights=[]):  #
        '''[{"SecuCode":"股票代码","Market":"市场类型","Volume":"委托数量","Price":"委托价格","Direct":"买卖方向,1-买入，2-卖出","EntrustType":"委托类型,1-限价 2-市价","ItemExtend":"扩展字段"}]'''
        _account = self.earningsData()
        _totalBalance = _account.get("BalanceAmount") + _account.get("marketValue")
        _avalableBalance = _account.get("BalanceAmount")
        _holding = self.getHoldsList(holdingType=HoldingType.Holding)
        _positions = {}
        for item in _holding:
            _positions[self.codeConvert_Oddly2Rqalpha(item['secucode'],item['Market'])] = item
        _orderList = []

        _code_2_weight_target = {k: v for k, v in code_weights}
        _ticks = self.getTick(list(set([k for k, v in code_weights] + list(_positions.keys()))))
        _code_ticks = {item['SecuCode']: item for item in _ticks}
        # for sale
        for code, item in _positions.items():
            if item['CanSellVolume'] <=0:
                continue
            elif code not in _code_2_weight_target:
                _orderList.append({"SecuCode": item['secucode'], "Market":item['Market'], "Volume": item['CanSellVolume']
                                   ,"Price":_code_ticks.get(code)['NowPrice'],"Direct":2,"EntrustType":2})
                _avalableBalance += item['CanSellVolume'] * _code_ticks.get(code)['NowPrice']
            elif _code_2_weight_target.get(code) < item['Positions']:
                _saleWeight = item['Positions'] - _code_2_weight_target.get(code)
                _saleVolume = round(_saleWeight * _totalBalance/_code_ticks.get(code)['NowPrice'],-2)
                _saleVolume = min(_saleVolume, item['CanSellVolume'])
                _orderList.append({"SecuCode": item['secucode'], "Market": item['Market'], "Volume": _saleVolume
                                      , "Price": _code_ticks.get(code)['NowPrice'], "Direct": 2,
                                       "EntrustType": 2})
                _avalableBalance += _saleVolume * _code_ticks.get(code)['NowPrice']

        #for buy
        _buyPowerReduce = 0.997 #可用资金留0.2%的缩放空间，以避免可用资金不足
        for code, weight in code_weights:
            if code not in _positions:
                _tick = _code_ticks.get(code)
                _buyNeed = _totalBalance * weight
                _realBuy = min(_buyNeed, _avalableBalance * _buyPowerReduce)
                _buyVolume = round(_realBuy / _tick['NowPrice'], -2)
                if _buyVolume > 0:
                    _tgwCode, _tgwmarket = self.codeConvert_Rqalpha2Oddly(code)
                    _orderList.append(
                        {"SecuCode": _tgwCode, "Market": _tgwmarket, "Volume": _buyVolume
                            , "Price": _tick['NowPrice'], "Direct": 1,"EntrustType": 2})
                    _avalableBalance -= _buyVolume * _tick['NowPrice']
            else:
                _holdItem = _positions.get(code)
                if weight > _holdItem['Positions']:
                    _tick = _code_ticks.get(code)
                    _buyWeight = weight - _holdItem['Positions']
                    _buyNeed = _totalBalance * _buyWeight
                    _realBuy = min(_buyNeed, _avalableBalance* _buyPowerReduce)
                    _buyVolume = round(_realBuy / _tick['NowPrice'], -2)
                    if _buyVolume > 0:
                        _orderList.append({"SecuCode": _holdItem['secucode'], "Market": _holdItem['Market'], "Volume": _buyVolume
                                              , "Price": _tick['NowPrice'], "Direct": 1,
                                           "EntrustType": 2})
                        _avalableBalance -= _buyVolume * _tick['NowPrice']

        print(_orderList)
        return self._BatchDelteGateOrder(uid=self._uid,accountid=self._accountid,combid=self._accountid,DeltegateList=json.dumps(_orderList))

if __name__ == "__main__":
    obj = TgwAccount()#tradeUrl = "http://www.tgw360.com/tgwapi/myapp/Trade")
    # res = obj.earningsData(combid=665)#uid=63790 ,combid=938)
    # print(res)
    # res = obj.orderToPercent(code_weights=[("150008.OF",0.2),("300047.XSHE",0.1),("600081.XSHG",0.2),("002387.XSHE",0.2),("600570.XSHG",0.3)],combid=665)  # uid=63790 ,combid=938)
    # print(res)
    res = obj.getHoldsList()#uid=63790 ,combid=938)
    print(res)
    # res = obj.EarningsData()#uid=63790 ,combid=938)
    # print(res)