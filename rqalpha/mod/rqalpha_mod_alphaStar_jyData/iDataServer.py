#coding=utf-8

"""
@author: evilXu
@file: iDataServer.py
@time: 2017/6/16 9:12
@description: 
"""

import requests
import simplejson

class IDataServer(object):
    def __init__(self,domain = "ip:port"):
        self._domain = domain
        self._headers = {'Content-type': 'application/json'}


    def get(self,suburl = "",params=None):
        try:
            _url = self._domain + suburl
            r = requests.get(_url,params=params,timeout=0.01,headers = self._headers)
            if r.status_code != requests.codes.ok:
                print("not 200!")
                return None
            return r.json()
        except requests.exceptions.Timeout as et:
            print("timeout")
            return None
        except Exception as e:
            print(e)
            return None

    def post(self,suburl = "",data = None):
        try:
            _url = self._domain + suburl
            # print(_url, data, self._headers)
            r = requests.post(_url,data = simplejson.dumps(data),timeout=15
                              ,headers = self._headers)
            # print(r,r.content)
            if r.status_code != requests.codes.ok:
                print("not 200!")
                return None
            return r.json()
        except requests.exceptions.Timeout as et:
            print("timeout")
            return None
        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()
            return None

    def _json2Object(self,json):
        return simplejson.loads(json)

if __name__ == "__main__":
    obj = IDataServer("http://172.18.44.123:8004/")
    data = {'factors': [{'params': {'dif_s': 12, 'dea': 9, 'dif_l': 26}, 'name': 'MACD_HIST'}, {'params': {'dif_s': 12, 'dea': 9, 'dif_l': 26}, 'name': 'MACD_DEA'}], 'codes': ['000001.SZ', '000002.SZ'], 'dateB': '2017-01-13', 'name': 'getfactor'}
    _res = obj.post(suburl="test/getfactor",data=data)
    print(_res)