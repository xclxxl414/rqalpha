#coding=utf-8

"""
@author: xuchunlin
@file: sendMail.py
@time: 2016/7/28 17:47
@description: 
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

class SendMail():
    def __init__(self,smtpserver="",username="",passwd=""):
        self._smtp = smtpserver
        self._uname = username
        self._passwd = passwd
        # self._sender = sender

    def SendTo(self, to=[], subject="", content="", attaches = [], cc=[]):
        message = MIMEMultipart()
        message.attach(MIMEText(content, 'plain', 'utf-8'))#html plain
        message['Subject'] = Header(subject, 'utf-8')
        message['From'] = self._uname
        message['To'] = ";".join(to)
        message['cc'] = ";".join(cc)
        for f in attaches:
            _attpart = MIMEApplication(open(f, 'rb').read())
            _fname = os.path.split(f)[1]
            _attpart.add_header('Content-Disposition', 'attachment', filename=_fname)
            message.attach(_attpart)

        try:
            smtp = smtplib.SMTP()
            smtp.connect(self._smtp)#, '25')
            smtp.login(self._uname, self._passwd)
            smtp.sendmail(self._uname, to + cc, message.as_string())
            # print("邮件发送成功".decode('utf8'))
        except Exception as e:
            print("Error: 无法发送邮件：",e.smtp_error.decode("gb2312"))
        finally:
            smtp.quit()

if __name__ == "__main__":
    obj = SendMail(smtpserver="smtp.exmail.qq.com",username="receiver.quant@591hx.com",passwd="abc")

    receiver = ['chunlin.xu@591hx.com']
    cc = ['xclxxl414@163.com']
    subject = '啦啦啦我是卖报的小行家'
    content = "这是一封测试邮件"
    obj.SendTo(receiver,subject,content,["admin.py"],cc=cc)




