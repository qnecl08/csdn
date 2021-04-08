
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import threading

import time

import csdnDownDb

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
            try:
                time.sleep(5)
                files=csdnDownDb.getFileToMail()
                for file in files:
                    print("开始发邮件",file)
                    mailto_list = [file['mail']]
                    mail_title = file['file_name']
                    mail_content = file['file_name']
                    mm = Mailer(mailto_list, mail_title, mail_content,file['file_name'],file['path'])
                    res = mm.sendMail()
                    print("邮件结果=",res)
                    if res:
                        csdnDownDb.updateFileStep(file['id'],1)
            except Exception as e:
                print(str(e))

class Mailer(object):
    def __init__(self, maillist, mailtitle, mailcontent,fileName,path):
        self.mail_list = maillist
        self.mail_title = mailtitle
        self.mail_content = mailcontent
        self.fileName = fileName
        self.path = path

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

        puretext = MIMEText('蛋定龙淘宝店发送文件：' + self.mail_content)
        msg.attach(puretext)
        jpgpart = MIMEApplication(open(self.path+self.fileName, 'rb').read())
        jpgpart.add_header('Content-Disposition', 'attachment', filename=self.fileName)
        msg.attach(jpgpart)

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

if __name__ == "__main__":
    mail=mailDeal("")
    mail.start()
    while 1:
        time.sleep(3)