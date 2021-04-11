
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import threading

import time

import pickle

import appWatch
import csdnDownDb
from selenium import webdriver


class Mailer(object):
    def __init__(self, maillist, mailtitle, mailcontent):
        self.mail_list = maillist
        self.mail_title = mailtitle
        self.mail_content = mailcontent

        self.mail_host = "smtp.163.com"
        self.mail_user = "zhangchungame@163.com"
        self.mail_pass = "zc59763451"
        self.mail_postfix = "163.com"

    def sendMail(self):

        me = self.mail_user + "<" + self.mail_user + "@" + self.mail_postfix + ">"
        msg = MIMEMultipart()
        msg['Subject'] = self.mail_title
        msg['From'] = me
        msg['To'] = ";".join(self.mail_list)

        puretext = MIMEText(self.mail_content)
        msg.attach(puretext)

        try:
            s = smtplib.SMTP()  # 创建邮件服务器对象
            s.connect(self.mail_host)  # 连接到指定的smtp服务器。参数分别表示smpt主机和端口
            s.login(self.mail_user, self.mail_pass)  # 登录到你邮箱
            s.sendmail(me, self.mail_list, msg.as_string())  # 发送内容
            s.close()
            return True
        except Exception as e:
            print(str(e))
        return False


class mailDeal(threading.Thread):
    appWatch={}
    def run(self):  # 定义每个线程要运行的函数
        try:
            while 1:
                self.watchMail()
        except Exception as e:
            print(str(e))
            return False

    def __init__(self,appWatch):
        threading.Thread.__init__(self)
        self.appWatch=appWatch

    def watchMail(self):
        while 1:
            time.sleep(5)
            files = csdnDownDb.getFileToMail()
            for file in files:
                mailto_list = [file['mail']]
                mail_title = file['file_name']
                mail_content=""
                mail_content+="感谢您对本店的支持\r\n"
                mail_content+="本次服务文件下载链接：http://daixiazai.dandinglong.site"+file['upload_path']+file['file_name']+"\r\n"
                mail_content+="请将链接复制到浏览器使用"
                mail_content+="本店地址：https://shop33792321.taobao.com/"
                mm = Mailer(mailto_list, mail_title, mail_content)
                res = mm.sendMail()
                if res:
                    csdnDownDb.updateFileStep(file['id'], 2)
                    self.appWatch.mailSendCount+=1



if __name__ == "__main__":
    # appwatch=appWatch.SelfWatch()
    # mail=mailDeal(appwatch)
    # mail.start()
    # while 1:
    #     time.sleep(3)
    str="apm硬件信息-适配Visual Studio.rar"
    str=str.replace(" ","",-1)
    print(str)

