import time

import pickle
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()  # 浏览器最大化
url = 'https://passport.csdn.net/account/login'
driver.get(url)
# driver.find_element_by_id('username').()
driver.find_element_by_id('username').send_keys("13817249443")
# driver.find_element_by_id('password').clear()
driver.find_element_by_id('password').send_keys("Qwert12345@")
driver.find_element_by_class_name("logging").click()
time.sleep(2)

cookies=driver.get_cookies()
# time.sleep(20)
byte_data = pickle.dump(cookies,open( "./13817249443"+".txt", "wb+" ))
print(byte_data)
driver.quit()

obj = pickle.load(open("./13817249443"+".txt","rb+"))
print(obj)
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.maximize_window()  # 浏览器最大化
url = 'https://www.csdn.net'
driver.get(url)
time.sleep(10)
for cookie in obj:
    driver.add_cookie(cookie)
driver.refresh()
