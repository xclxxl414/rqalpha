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
        self._env.event_bus.add_listener(EVENT.BEFORE_TRADING, self.beforeTrading)
        self._tgwTick = TgwTick(tickUrl=mod_config.tickurl, secretId_TICK=mod_config.secretId_TICK
                                , secretKey_TICK=mod_config.secretKey_TICK)

    def beforeTrading(self, event):
        self._tgwAccont.beforeTrading()

    def afterTrading(self,event):
        self._tgwAccont.afterTrading()

    def get_portfolio(self):
        self._tgwAccont = TgwAccount(tradeUrl=self.mod_config.tgwurl, secretId=self.mod_config.secretId
                                     , secretKey=self.mod_config.secretKey, uid=self.mod_config.uid,
                                     accountid= list(self._env.config.base.accounts.values())[0].accountid)
        accounts = {}
        config = self._env.config
        units = 0

        name,account_info = list(config.base.accounts.items())[0]
        starting_cash = account_info.cash_base

        account_model = self._env.get_account_model(account_info.type)
        position_model = self._env.get_position_model(account_info.type)
        positions = Positions(position_model)

        _hodings = self._tgwAccont.getHoldsList(holdingType=HoldingType.Holding)
        for item in _hodings:
            code = TgwUtils.codeConvert_Oddly2Rqalpha(item['secucode'],item['Market'])
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
        account = account_model(name,_availableCash, positions)
        accounts[name] = account
        # print("get_portfolio",account.cash,account.total_value,positions)
        return Portfolio(config.base.start_date, account.total_value/starting_cash, starting_cash, accounts)

    def _getLatestPrice(self,code = ""):
        _res = self._tgwTick.getTick(codeList=[code])
        return _res[0]['NowPrice']

    def _fake_trade(self,order_book_id, quantity, price):
        return Trade.__from_create__(0, price, abs(quantity),
                                     SIDE.BUY if quantity > 0 else SIDE.SELL,
                                     POSITION_EFFECT.OPEN, order_book_id)

    def get_open_orders(self,order_book_id=None):
        return self._tgwAccont.openOrders()

    def submit_order(self, account,order):
        self._env.event_bus.publish_event(Event(EVENT.ORDER_PENDING_NEW, account=account, order=copy(order)))
        if order.is_final():
            return
        order.active()
        self._env.event_bus.publish_event(Event(EVENT.ORDER_CREATION_PASS, account=account, order=copy(order)))
        self._tgwAccont.orderPending(order.order_book_id, order.quantity if order.side == SIDE.BUY else -1 * order.quantity)

    def cancel_order(self,account, order):
        system_log.error(_(u"cancel_order function is not supported in signal mode"))
        return None

class HoldingType(Enum):
    All = 1
    Holding = 2
    History = 3

class TgwUtils():
    # 市场类型  65537【上海】  131073【深圳】  65545【上证指数】  131081【深证，创业】
    marketMap_oddly_STD = {65537: "XSHG", 131073: "XSHE", 131075: "OF"}
    marketMap_STD_oddly = {v: k for k, v in marketMap_oddly_STD.items()}

    @classmethod
    def codeConvert_Oddly2Rqalpha(cls,code,market):
        # print(code,market)
        return "%06d"%(code)+"."+ cls.marketMap_oddly_STD.get(market)

    @classmethod
    def codeConvert_Rqalpha2Oddly(cls,code):
        a = code.split(".")
        return a[0],cls.marketMap_STD_oddly.get(a[1])

    @staticmethod
    def post(url, _param = None):
        r = requests.post(url=url, data=_param)
        if r.status_code != requests.codes.ok:
            print("api: %s ,not 200!"%(_param,r))
            return None
        _res = r.json()
        if _res.get("errno") != 0:
            print("api: %s ,failed,msg:%s,%s" % (_param, _res.get("errno"),_res.get("errmsg")))
            return None
        return r.json().get("data")

    @staticmethod
    def get(url, params=None):
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

class TgwAccount():
    def __init__(self, tradeUrl = "http://www.tgwtest.com/tgwapi/myapp/Trade"
                 ,secretId="commonkey",secretKey="TGW_COMMONKEY",uid = None,accountid = None): #):
        # print(tradeUrl,tickUrl,secretId_TICK,secretKey_TICK,secretId,secretKey)
        self._tradeRootUrl = tradeUrl
        self._apiInfo = {"secretId": secretId, "secretKey": secretKey}
        self._uid = uid
        self._accountid = accountid
        self._openOrders = []

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
            _res = TgwUtils.get(self._tradeRootUrl + "/GetHoldsList",_param)
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
            _res = TgwUtils.get(self._tradeRootUrl + "/EarningsData", _param)
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
            _res = TgwUtils.get(self._tradeRootUrl + "/BatchDelteGateOrder", _param)
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

    def beforeTrading(self):
        self._openOrders = []

    def orderPending(self,code,volume):
        self._openOrders.append((code,volume))

    def openOrders(self):
        return self._openOrders

    def afterTrading(self):
        system_log.info("push order:{} to TGW account:{} ", str(self._openOrders),self._accountid)
        if len(self._openOrders) <1:
            return
        self._orderShare(self._openOrders)

    def _orderShare(self, code_Cnt=[]):
        if len(code_Cnt) <1:
            return None
        _orderList = []
        for code,volume in code_Cnt:
            _tgwcode,market = TgwUtils.codeConvert_Rqalpha2Oddly(code)
            _orderList.append({"SecuCode": _tgwcode, "Market": market, "Volume": abs(volume)
                            , "Price": 0, "Direct": 1 if volume > 0 else 2,"EntrustType": 2})
        return self._BatchDelteGateOrder(uid=self._uid, accountid=self._accountid, combid=self._accountid,
                                         DeltegateList=json.dumps(_orderList))


class TgwTick():
    def __init__(self,tickUrl = "http://tgw360.com/webapi/myapp/WxInterface/GetQueInfo"
                 ,secretId_TICK="dianziqianzhang",secretKey_TICK="B123456789"):
        self._tickUrl = tickUrl
        self._tickApiInfo = {"secretId": secretId_TICK, "secretKey": secretKey_TICK}

    def getTick(self,codeList = []):
        _param = {"secretId":self._tickApiInfo.get("secretId"), "time":str(round(time.time()))}
        _codeList = [{"SecuCode":code.split(".")[0],"MarketType":TgwUtils.marketMap_STD_oddly.get(code.split(".")[1])} for code in codeList]
        _param.update({"SecuCodeList":json.dumps(_codeList)})
        _secretStr = "&".join([str(k)+"="+str(v) for k,v in sorted(_param.items(),key=lambda x:x[0])])
        ss = hmac.new(key = bytes(self._tickApiInfo['secretKey'], "utf8"), msg=bytes(_secretStr, "utf8"), digestmod="sha1").digest()
        s1 = base64.b64encode(ss)
        _param.update({"sign":s1})
        _res = TgwUtils.get(self._tickUrl,_param)
        a = _res.get('data').get("info").get("GridDataList")
        if a is None:
            return None
        for item in a:item.update({"SecuCode":TgwUtils.codeConvert_Oddly2Rqalpha(item['SecuCode'],item['MarketType']),"MarketType":TgwUtils.marketMap_oddly_STD.get(item['MarketType'])})
        return a

if __name__ == "__main__":
    # obj = TgwAccount()#tradeUrl = "http://www.tgw360.com/tgwapi/myapp/Trade")
    # res = obj.earningsData(combid=665)#uid=63790 ,combid=938)
    # print(res)
    # res = obj.orderToPercent(code_weights=[("150008.OF",0.2),("300047.XSHE",0.1),("600081.XSHG",0.2),("002387.XSHE",0.2),("600570.XSHG",0.3)],combid=665)  # uid=63790 ,combid=938)
    # print(res)
    # res = obj.getHoldsList()#uid=63790 ,combid=938)
    # res = TgwTick().getTick(["000001.XSHE"])
    res = TgwUtils.codeConvert_Oddly2Rqalpha(1,131073)
    res = TgwUtils.marketMap_oddly_STD
    print(res)
    # res = obj.EarningsData()#uid=63790 ,combid=938)
    # print(res)