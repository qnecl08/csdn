#coding:UTF-8
import time
import appWatch,watchTaobao

t = appWatch.SelfWatch()

def startTaobaoWatch():
    taobao=watchTaobao.taobaoOrderWatch(t)
    taobao.start()


def startWatchSelf():
    t.start()



if __name__ == "__main__":
    startWatchSelf()
    startTaobaoWatch()
    while 1:
        time.sleep(3)