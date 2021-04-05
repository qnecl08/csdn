import pickle

import time
from selenium import webdriver

obj = pickle.load(open("./taobao"+".txt","rb+"))
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
driver.get("https://trade.taobao.com/trade/itemlist/list_sold_items.htm")