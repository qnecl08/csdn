import os
import re
import threading
import time

from selenium import webdriver

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
    def watchChrome(self):
        while 1:
            time.sleep(5)
            orders=taobaoDb.notDealOrder()
            if len(orders)>0:
                if csdnDownDb.hasCanUseAccount():
                    chromeOptions = webdriver.ChromeOptions()
                    path = os.getcwd() + "\\files\\"
                    prefs = {"download.default_directory": path,"profile.managed_default_content_settings.images": 2}
                    chromeOptions.add_experimental_option("prefs", prefs)
                    PROXY = ipProxy.getIp()  # IP:PORT or HOST:PORT
                    chromeOptions.add_argument('--proxy-server=http://%s' % PROXY)
                    driver = webdriver.Chrome(chrome_options=chromeOptions)
                    driver.maximize_window()  # 浏览器最大化
                    for order in orders:
                        # taobaoDb.updateStepOrder(order['order_no'],1)
                        try:
                            remarkDeal=self.dealRemark(order['remark'])
                            if remarkDeal==None:
                                taobaoDb.updateStepOrder(order['order_no'],9)
                                continue

                            driver.get(remarkDeal['src_url'])
                            #获取资源积分
                            download_top=driver.find_element_by_id("download_top")
                            divs=download_top.find_elements_by_class_name("dl_download")
                            labels=divs[0].find_elements_by_tag_name("label")
                            em=labels[0].find_element_by_tag_name("em")
                            score=em.text
                            #获取文件名
                            download_top_t=driver.find_element_by_class_name("download_top_t")
                            srcFileName=download_top_t.find_element_by_tag_name("h3").get_attribute("title")
                            account=csdnDownDb.useAccount(score)
                            if account==None:#没有可用账号了
                                continue
                            if self.login(driver,account)==0:
                                continue
                            time.sleep(1)
                            if account['account_type']=='vip':
                                fileName=self.vipAccountDownFile(driver,remarkDeal['src_url'],path)
                            else:
                                fileName =self.normalAccountDownFile(driver,remarkDeal['src_url'],path)
                            if fileName==None:#下载失败
                                taobaoDb.updateStepOrder(order['order_no'],8)
                                continue
                            input={}
                            input['file_name']=fileName
                            input['mail']=remarkDeal['mail']
                            input['src_url']=remarkDeal['src_url']
                            input['path']=path
                            input['csdn_account']=account['account']
                            input['order_no']=order['order_no']
                            fileId=csdnDownDb.insertFile(input)
                            taobaoDb.updateStepOrder(order['order_no'],2)
                        except Exception as e:
                            print(str(e))
                            pass
                    driver.quit()
    def vipAccountDownFile(self,driver,src_url,path):
        driver.get(src_url)
        time.sleep(1)
        driver.find_element_by_class_name("direct_download").click()
        time.sleep(2)
        btn = driver.find_element_by_id("vip_btn")
        btn.click()
        driver.get("chrome://downloads/")
        fileName=self.findDownFileName(driver,path)
        if fileName==None:
            return None
        return fileName


    def normalAccountDownFile(self,driver,src_url,path):
        driver.get(src_url)
        time.sleep(1)
        driver.find_element_by_class_name("direct_download").click()
        time.sleep(2)
        aaa = driver.find_elements_by_class_name("js_download_btn")
        for el in aaa:
            if el.get_attribute("data-href"):
                el.click()
                break
        driver.get("chrome://downloads/")
        fileName=self.findDownFileName(driver,path)
        if fileName==None:
            return None
        return fileName

    def findDownFileName(self,driver ,path):

        driver.get("chrome://downloads/")
        q = driver.execute_script('return document.getElementsByTagName("downloads-manager")[0].shadowRoot.children["downloads-list"]._physicalItems[0].content.querySelectorAll("#file-link")[0].href;')
        driver.quit()
        print(q)
        return q
        lastFile=csdnDownDb.lastInsertFile()
        if lastFile==None:
            lastCreateTime=0
        else:
            lastCreateTime=lastFile['create_time']
        times = 3
        while 1:
            iterms = os.listdir(path)
            m_time = 0
            fileName = ""
            for item in iterms:
                stat = os.stat(path + "/" + item)
                if stat.st_mtime > lastCreateTime:
                    fileName = item
                    if ".crdownload" not in fileName:
                        return fileName
                    break
            if fileName=="":
                times-=1
            if times < 0:
                return None
            time.sleep(5)


    def login(self,driver,account):
        url = 'https://passport.csdn.net/account/login'
        driver.get(url)
        driver.find_element_by_id('username').send_keys(account['account'])
        driver.find_element_by_id('password').send_keys(account['password'])
        driver.find_element_by_class_name("logging").click()
        times=3
        while 1:
            if "www.csdn.net" in driver.current_url:
                return 1
            times-=1
            if times<0:
                return 0
            time.sleep(3)

    # driver.get("https://download.csdn.net/my")
    # datas = driver.find_element_by_class_name("datas")
    # spans = datas.find_elements_by_tag_name("span")
    # score = spans[0].text


    def dealRemark(self,remark):
        result={}
        searchObj = re.search('([A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)', remark)

        searchObj2 = re.search('(download.csdn.net/download/.*?/\\d+)', remark)
        if searchObj:
            result["mail"]=searchObj.group(1)
        else:
            return None
        if searchObj2:
            result["src_url"]="https://"+searchObj2.group(1)
        else:
            return None
        return result


if __name__ == "__main__":
    t=csdnWatch("")
    # t.findDownFileName("./files")
    t.start()
    while 1:
        time.sleep(3)