import time

import pickle
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
driver.maximize_window()  # 浏览器最大化
url = 'https://login.taobao.com/member/login.jhtml'
driver.get(url)

time.sleep(2)
while 1:
    time.sleep(2)
    if "member/login.jhtml" in driver.current_url:
        pass
    else:
        break
cookies=driver.get_cookies()
# time.sleep(20)
byte_data = pickle.dump(cookies,open( "./taobao"+".txt", "wb+" ))
print(byte_data)
driver.quit()

