#coding:UTF-8
import os

import time

import pickle
from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()
path = os.getcwd() + "\\files\\"
prefs = {"download.default_directory": path,}
chromeOptions.add_experimental_option("prefs", prefs)
# chromeOptions.add_argument('--proxy-server=http://%s' % PROXY)
driver = webdriver.Chrome(chrome_options=chromeOptions)

driver.get("https://mail.163.com/")

time.sleep(2)
while 1:
    time.sleep(2)
    if "js6/main.jsp" in driver.current_url:
        break
cookies=driver.get_cookies()
# time.sleep(20)
byte_data = pickle.dump(cookies,open( "./mail163"+".txt", "wb+" ))
print(byte_data)
driver.quit()
