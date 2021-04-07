import re
import threading

import os

import csdnDownDb
import ipProxy
import taobaoDb
import time
from selenium import webdriver
from bs4 import BeautifulSoup


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
                    # prefs = {"profile.managed_default_content_settings.images": 2}
                    # chromeOptions.add_experimental_option("prefs", prefs)
                    path = os.getcwd() + "\\files"
                    prefs = {"download.default_directory": path,"profile.managed_default_content_settings.images": 2}
                    chromeOptions.add_experimental_option("prefs", prefs)
                    # PROXY = ipProxy.getIp()  # IP:PORT or HOST:PORT
                    # PROXY = "101.81.52.97:28803"  # IP:PORT or HOST:PORT
                    # print(PROXY)
                    # # time.sleep(5)
                    # chromeOptions.add_argument('--proxy-server=http://%s' % PROXY)
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
                            if account==None:
                                continue
                            self.login(driver,account)
                            if account['account_type']=='vip':
                                fileName=self.vipAccountDownFile(driver,remarkDeal['src_url'],srcFileName)
                            else:
                                fileName =self.normalAccountDownFile(driver,remarkDeal['src_url'],srcFileName)
                            print("fileName=",fileName)
                        except Exception as e:
                            print(str(e))
                            pass
                    driver.quit()
    def vipAccountDownFile(self,driver,src_url,srcFileName):
        result={}
        driver.get(src_url)
        time.sleep(1)
        driver.find_element_by_class_name("direct_download").click()
        time.sleep(2)
        btn = driver.find_element_by_id("vip_btn")
        btn.click()
        driver.get("chrome://downloads/")
        title_areas=driver.find_elements_by_class_name("title-area")
        downArea={}
        for area in title_areas:
            if srcFileName in area.find_element_by_tag_name("a").text:
                downArea=area
                result['fileName']=area.find_element_by_tag_name("a").text
                break
        times=500
        while 1:
            if downArea.find_element_by_id("show"):
                return result
            times-=1
            if time<0:
                return None


    def normalAccountDownFile(self,driver,src_url,srcFileName):
        result={}
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

        times=500
        while 1:
            soup=BeautifulSoup(driver.page_source,"html.parser")
            title_areas=soup.find_all(id="title-area")
            for area in title_areas:
                a=area.find("a")
                if srcFileName in a.string:
                    result['fileName']=a.string
                    if area.find(id="show"):
                        return result
            times-=1
            if times<0:
                return None
            time.sleep(1)
    def login(self,driver,account):
        url = 'https://passport.csdn.net/account/login'
        driver.get(url)
        driver.find_element_by_id('username').send_keys(account['account'])
        driver.find_element_by_id('password').send_keys(account['password'])
        driver.find_element_by_class_name("logging").click()
        time.sleep(2)

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
    t.start()
    while 1:
        time.sleep(3)