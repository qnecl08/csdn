#coding:UTF-8
import time
import appWatch,watchTaobao
import csdnDeal
import csdnLoginGetCookie
import mailDeal

t = appWatch.SelfWatch()

def startTaobaoWatch():
    taobao=watchTaobao.taobaoOrderWatch(t)
    taobao.start()


def startWatchSelf():
    t.start()
def startMail():
    mail=mailDeal.mailDeal(t)
    mail.start()
def startCsdn():
    mail=csdnDeal.csdnWatch(t)
    mail.start()
def startCsdnLogin():
    mail=csdnLoginGetCookie.csdnLogin()
    mail.start()




if __name__ == "__main__":
    startWatchSelf()
    startTaobaoWatch()
    startMail()
    startCsdnLogin()
    startCsdn()
    while 1:
        time.sleep(3)