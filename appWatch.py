#coding:UTF-8
import threading
import requests
import time


class SelfWatch(threading.Thread):
    newOrderCount=0
    effectOrderCount=0
    downLoadCount=0
    uploadCount=0
    mailSendCount=0
    msg=""
    def run(self):  # 定义每个线程要运行的函数
        try:
            while 1:
                self.reportToWechat()
                time.sleep(60*2)
        except Exception as e:
            print(str(e))
            return False

    def __init__(self):
        threading.Thread.__init__(self)
    def reportToWechat(self):
        sendStr=""
        sendStr+="新订单："+str(self.newOrderCount)+"\r\n"
        sendStr+="有备注订单："+str(self.effectOrderCount)+"\r\n"
        sendStr+="下载文件："+str(self.downLoadCount)+"\r\n"
        sendStr+="上传文件："+str(self.uploadCount)+"\r\n"
        sendStr+="发送邮件："+str(self.mailSendCount)+"\r\n"
        sendStr+="消息："+str(self.msg)+"\r\n"
        session = requests.session()
        data = {"msg": sendStr}
        resp = session.post("http://autoanswer.dandinglong.site/answer.php?user=o--w40ZO0YmoDMFEGGkGiIJqbCkU",data=data)
        print("微信监控：",resp.text)



