import pickle

import time

import os
from selenium import webdriver

obj = pickle.load(open("./mail163"+".txt","rb+"))
print(obj)
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.maximize_window()  # 浏览器最大化
url = 'https://mail.163.com/js6/main.jsp'
driver.get(url)
time.sleep(1)
for cookie in obj:
    driver.add_cookie(cookie)
time.sleep(1)
driver.get("https://mail.163.com/js6/main.jsp")
btnLogout=driver.find_element_by_id("btnLogout")
btnLogout.click()
time.sleep(1)
_mail_component_70_70=driver.find_element_by_id("_mail_component_70_70")
_mail_component_70_70.click()

time.sleep(3)
by0=driver.find_element_by_class_name("by0")
input=by0.find_element_by_tag_name("input")
input.send_keys("E:\code\python\csdn\sample\mail163.txt")
input.send_keys("E:\code\python\csdn\sample\\taobao.txt")
nui=driver.find_element_by_class_name("nui-editableAddr-ipt")
nui.send_keys("342219728@qq.com")
mainBtn=driver.find_element_by_class_name("nui-mainBtn")
mainBtn.click()

while 1:
    time.sleep(3)
    pv1=driver.find_element_by_class_name("pv1")
    if pv1:
        break

cookies=driver.get_cookies()
byte_data = pickle.dump(cookies,open( "./mail163"+".txt", "wb+" ))
driver.quit()




