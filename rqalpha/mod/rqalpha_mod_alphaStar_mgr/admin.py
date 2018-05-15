#coding=utf-8

"""
@author: evilXu
@file: adminConsole.py
@time: 2017/12/28 17:46
@description: 
"""

import pymysql
from sqlalchemy import engine
from rqalpha.utils.logger import system_log, basic_system_log, user_system_log, user_detail_log
from datetime import *

class Admin():
    def __init__(self,db= None):
        '''
        '''
        self.conn = pymysql.connect(host=db.host, user=db.user, password=db.passwd,
                 database=db.db, port=db.port, charset='utf8')
        self.cursor = self.conn.cursor()

        _createUser = '''CREATE TABLE IF NOT EXISTS User(
                `name` varchar(64) primary key,
                `passwd` varchar(64) DEFAULT NULL
                )'''
        _createFactor = '''CREATE TABLE IF NOT EXISTS Factors(
                `fname` varchar(64) primary key,
                `user` varchar(64) NOT NULL,
                `status` varchar(20) NOT NULL,
                `uptime` timestamp NOT NULL,
                FOREIGN KEY(user) REFERENCES User(name)
                )'''
        _createStrategy = '''CREATE TABLE IF NOT EXISTS Strategys(
                `sname` varchar(64) primary key,
                `user` varchar(64) NOT NULL,
                `status` varchar(20) NOT NULL,
                `uptime` timestamp NOT NULL,
                `accountid` INTEGER NOT NULL,
                FOREIGN KEY(user) REFERENCES User(name)
                )'''
        _createStrategyLog = '''CREATE TABLE IF NOT EXISTS StrategyLog(
                        `id` bigint primary key auto_increment,
                        `sname` varchar(64) NOT NULL,
                        `log` TEXT NOT NULL,
                        `tradetime` timestamp NOT NULL,
                        `uptime` timestamp NOT NULL,
                        FOREIGN KEY(sname) REFERENCES Strategys(sname)
                        )'''
        self.cursor.execute(_createUser)
        self.cursor.execute(_createFactor)
        self.cursor.execute(_createStrategy)
        self.cursor.execute(_createStrategyLog)
        self.conn.commit()


    def addUser(self,uname = "",passwd="",adminPass=""):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            _sigPass = self._signaturePass(passwd)
            self.cursor.execute("insert into User(name,passwd) values(%s,%s)", (uname,_sigPass))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("addUser failed:{0}", e)
            return False

    def delUser(self,uname,adminPass):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("delete from User where name=%s",(uname,))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("delUser failed:{0}", e)
            return False

    def addAdminUser(self,passwd):
        _sigPass = self._signaturePass(passwd)
        try:
            self.cursor.execute("insert into User(name,passwd) values(%s,%s)",("admin",_sigPass))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("addAdminUser failed:{0}", e)
            return False

    def checkAdmin(self, passwd):
        try:
            self.cursor.execute("select passwd from User where name='admin'")
            _sigPass = self.cursor.fetchone()[0]
            if _sigPass == self._signaturePass(passwd):
                return True
            else:
                return False
        except Exception as e:
            system_log.error("getPublishedStrategys failed:{0}", e)
            return False

    def _signaturePass(self,passwd):
        #TODO implement this function
        return passwd;

    def registerFactor(self,fname,uname,adminPass):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("insert into Factors(fname,user,status,uptime) values(%s,%s,%s,%s)",(fname,uname,"new",datetime.now()))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("registerFactor failed:{0}", e)
            return False

    def delFactor(self,fname,adminPass,datapath):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("delete from Factors where fname=%s",(fname,))
            self.conn.commit()
            self._clearFactorData(fname,datapath)
            return True
        except Exception as e:
            system_log.error("delFactor failed:{0}", e)
            return False

    def _clearFactorData(self,fname,datapath):
        import shutil,os
        src = os.path.join(datapath,fname)
        dst = os.path.join(datapath,fname + "_unpublished_at_"+ datetime.now().strftime("%Y%m%d_%H-%M-%S"))
        shutil.move(src,dst)
        return

    def registerAndPublishFactor(self,fname,uname,adminPass):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("insert into Factors(fname,user,status,uptime) values(%(fname)s,%(user)s,%(status)s,%(uptime)s)"
                                " ON DUPLICATE KEY UPDATE status=%(status)s,uptime=%(uptime)s"
                                ,{"fname":fname,"user":uname,"status":"published","uptime":datetime.now()})
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("registerAndPublishFactor failed:{0}", e)
            return False

    def publishFactor(self,fname,adminPass):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("update Factors set status='published',uptime=%s where fname = %s",(datetime.now(),fname))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("publishFactor failed:{0}", e)
            return False

    def unPublishFactor(self,fname,adminPass,datapath):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("update Factors set status='unPublished',uptime=%s where fname = %s",(datetime.now(),fname))
            self.conn.commit()
            self._clearFactorData(fname, datapath)
            return True
        except Exception as e:
            system_log.error("unPublishFactor failed:{0}", e)
            return False

    def getPublishedFactors(self):
        res = []
        try:
            self.cursor.execute("select fname,user from Factors where status='published' order by uptime DESC")
            for row in self.cursor:
                res.append((row[0],row[1]))
            return res
        except Exception as e:
            system_log.error("getPublishedFactors failed:{0}", e)
            return res

    def getFactor(self,fname):
        try:
            self.cursor.execute("select fname,user,status from Factors where fname=%s",(fname,))
            for row in self.cursor:
                return row
            return None
        except Exception as e:
            system_log.error("checkFactorPublished failed:{0}", e)
            return None

    def registerStrategy(self,sname,uname,adminPass):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("insert into Strategys(sname,user,status,uptime) values(%s,%s,%s,%s)",(sname,uname,"new",datetime.now()))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("registerStrategy failed:{0}", e)
            return False

    def delStrategy(self,sname,adminPass):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("delete from Strategys where sname=%s", (sname,))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("delStrategy failed:{0}", e)
            return False

    def registerAndPublishStrategy(self, sname, uname,adminPass,accountID):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("insert into Strategys(sname,user,status,uptime,accountid) values(%(sname)s,%(user)s,%(status)s,%(uptime)s,%(accountid)s)"
                                "  ON DUPLICATE KEY UPDATE status=%(status)s,uptime=%(uptime)s,accountid=%(accountid)s"
                                ,{"sname":sname,"user":uname,"status":"published","uptime":datetime.now(),"accountid":accountID})
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("registerAndPublishStrategy failed:{0}", e)
            return False

    def publishStrategy(self,sname,adminPass,accountID):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("update Strategys set status='published',uptime=%s,accountid=%s where sname = %s"
                                ,(datetime.now(),accountID,sname))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("publishStrategy failed:{0}", e)
            return False

    def unPublishStrategy(self,sname,adminPass):
        if not self.checkAdmin(adminPass):
            system_log.error("check Admin failed,please connect admin User")
            return False
        try:
            self.cursor.execute("update Strategys set status='unPublished',uptime=%s where sname = %s",(datetime.now(),sname))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("unPublishStrategy failed:{0}", e)
            return False

    def getPublishedStrategys(self):
        res = []
        try:
            self.cursor.execute("select sname,user,accountid from Strategys where status='published' order by uptime DESC")
            for row in self.cursor:
                res.append((row[0],row[1],row[2]))
            return res
        except Exception as e:
            system_log.error("getPublishedStrategys failed:{0}", e)
            return res

    def getStrategy(self,sname):
        try:
            self.cursor.execute("select sname,user,accountid,status from Strategys where sname=%s",(sname,))
            for row in self.cursor:
                return row
            return None
        except Exception as e:
            system_log.error("getStrategy failed:{0}", e)
            return None

    def dumpStrategyLog(self,sname,tradingDt,log):
        try:
            self.cursor.execute("insert into StrategyLog(sname,tradetime,log,uptime) values(%s,%s,%s,%s)",(sname,tradingDt,log,datetime.now()))
            self.conn.commit()
            return True
        except Exception as e:
            system_log.error("dumpStrategyLog failed:{0}", e)
            return False

    def getStrategyLog(self,tradingDt=datetime(2015,1,1).date()):
        res = []
        try:
            _start = tradingDt.strftime("%Y-%m-%d")
            _end = (tradingDt + timedelta(days=1)).strftime("%Y-%m-%d")
            self.cursor.execute("select a.sname,a.log,a.uptime,b.user from StrategyLog as a "
                                "inner join Strategys as b on a.sname=b.sname where a.tradetime between %s and %s",(_start,_end))
            for row in self.cursor:
                res.append((row[0],row[1],row[2],row[3]))
            return res
        except Exception as e:
            system_log.error("getStrategyLog failed:{0}", e)
            return res

if __name__ == "__main__":
    obj = Admin(db=":memory:")
    _adminPass = "!@#$%6"
    obj.addAdminUser(_adminPass)
    obj.addUser(uname="test",passwd="",adminPass=_adminPass)


