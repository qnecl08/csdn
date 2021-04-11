import os
import re
import threading
import time

import pickle
import requests
from selenium import webdriver

import appWatch
import csdnDownDb
import ipProxy
import taobaoDb


class csdnWatch(threading.Thread):
    appWatch={}
    def run(self):  # 定义每个线程要运行的函数
        try:
            while 1:
                self.watchChrome()
        except Exception as e:
            print(str(e))
            return False

    def __init__(self,appWatch):
        threading.Thread.__init__(self)
        self.appWatch=appWatch
        self.path = os.getcwd() + "\\files\\"
    def watchChrome(self):
        while 1:
            time.sleep(5)
            orders=taobaoDb.notDealOrder()
            if len(orders)>0:
                if csdnDownDb.hasCanUseAccount():
                    for order in orders:
                        try:
                            remarkDeal=self.dealRemark(order['remark'])
                            if remarkDeal==None:
                                taobaoDb.updateStepOrder(order['order_no'],9)
                                continue
                            self.appWatch.effectOrderCount+=1
                            account=csdnDownDb.useAccount()
                            if account==None:#没有可用账号了
                                self.appWatch.msg="没有可用账号了"
                                continue

                            downloadUrl=self.vipAccountDownFile(account,remarkDeal['src_url'])
                            if downloadUrl==None:
                                continue
                            fileName=self.downloadFile(downloadUrl)
                            if fileName==None:#下载失败
                                fileName=self.downloadFile(downloadUrl)
                                if fileName==None:
                                    print("下载文件失败",fileName)
                                    self.appWatch.effectOrderCount-=1
                                    continue
                            input={}
                            input['file_name']=fileName
                            input['mail']=remarkDeal['mail']
                            input['src_url']=remarkDeal['src_url']
                            input['path']=self.path
                            input['csdn_account']=account['account']
                            input['order_no']=order['order_no']
                            fileId=csdnDownDb.insertFile(input)
                            print("插入数据库文件--",fileId)
                            taobaoDb.updateStepOrder(order['order_no'],2)
                            self.appWatch.downLoadCount+=1
                        except Exception as e:
                            print("异常：",str(e))
    def vipAccountDownFile(self,account,src_url):
        try:
            session=requests.session()
            proxy=ipProxy.getIp()
            proxies = {"http": "http://" + proxy, "https": "http://" + proxy, }
            cookies = pickle.load(open("./files/cookies/" +account['account']+ ".txt", "rb+"))
            session.proxies=proxies
            for cookie in cookies:
                session.cookies.set(cookie['name'], cookie['value'])
            resp = session.get(src_url)

            searchObj2 = re.search("<a href=\"(https://.*?)\" id=\"vip_btn\" class=\"dl_btn vip_dl_btn\">VIP下载</a>",
                                   resp.text)
            url = searchObj2.group(1)
            resp = session.get(url, allow_redirects=False)
            if resp.headers['Location']:
                return resp.headers['Location']
        except Exception as e:
            print("异常下载:",str(e))
        return None


    def downloadFile(self,downloadUrl):
        try:
            fileName=None
            r = requests.get(downloadUrl,stream=True)
            hreads=r.headers
            print(hreads)
            print("目标：",r.headers['Content-Disposition'])
            print("目标：",type(r.headers['Content-Disposition']))
            search=re.search("attachment;filename=\"(.*?)\"",r.headers['Content-Disposition'])
            if search.group(1):
                fileName=search.group(1)
                fileName=fileName.encode("iso-8859-1").decode('utf8')
                fileName = fileName.replace(" ", "", -1)
            if fileName==None :
                return  None
                # download started
            with open(self.path+fileName, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
            return fileName
        except Exception as e:
            print("下载异常:",str(e))
            return None

    def dealRemark(self,remark):
        result={}
        searchObj = re.search('[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+', remark)
        # searchObj = re.search('([A-Za-z0-9_]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)', remark)

        searchObj2 = re.search('(download.csdn.net/download/.*?/\\d+)', remark)
        if searchObj:
            result["mail"]=searchObj.group()
        else:
            return None
        if searchObj2:
            result["src_url"]="https://"+searchObj2.group(1)
        else:
            return None
        return result


if __name__ == "__main__":
    appwatch=appWatch.SelfWatch()
    t=csdnWatch(appwatch)
    t.start()
    while 1:
        time.sleep(3)

    # str='attachment;filename="è½¦çè¯å«è¯¾ç¨è®¾è®¡.zip"'
    # bbb=str.encode("iso-8859-1").decode('utf8')
    # print(bbb)
    # print(bbb.decode('unicode_escape'))
