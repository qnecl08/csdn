import pickle
import threading

import time
from selenium import webdriver

class taobaoOrderWatch(threading.Thread):
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
        obj = pickle.load(open("./taobao" + ".txt", "rb+"))
        print(obj)
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome()
        driver.maximize_window()  # 浏览器最大化
        url = 'https://www.taobao.com'
        driver.get(url)
        time.sleep(2)
        for cookie in obj:
            driver.add_cookie(cookie)
        time.sleep(2)
        driver.get(
            "https://trade.taobao.com/trade/itemlist/list_sold_items.htm?action=itemlist/SoldQueryAction&event_submit_do_query=1&auctionStatus=PAID&tabCode=waitSend")
        while 1:
            print("new round")
            time.sleep(3)
            try:
                driver.get("https://trade.taobao.com/trade/itemlist/list_sold_items.htm?action=itemlist/SoldQueryAction&event_submit_do_query=1&auctionStatus=PAID&tabCode=waitSend")
                time.sleep(1)
                orders = driver.find_elements_by_class_name("trade-order-main")
                for order in orders:
                    spans = order.find_elements_by_tag_name("span")
                    print("orderNo:", spans[2].text)  # 找到订单号
                    tables = order.find_elements_by_tag_name("table")
                    tds = tables[1].find_elements_by_tag_name("td")
                    a = tds[5].find_element_by_tag_name("a")  # 详情按钮
                    detailUrl = a.get_attribute("href")
                    driver.get(detailUrl)
                    dls = driver.find_elements_by_tag_name("dl")
                    print("买家留言", dls[3].find_element_by_tag_name("dt").text,dls[3].find_element_by_tag_name("dd").text)
                    self.appWatch.newOrderCount+=1
                    driver.back()
                cookies = driver.get_cookies()
                pickle.dump(cookies, open("./taobao" + ".txt", "wb+"))
            except Exception as e:
                print(str(e))









