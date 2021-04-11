import pickle
import re

import requests
import time
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.maximize_window()  # 浏览器最大化
url = 'https://passport.csdn.net/account/login'
driver.get(url)
# driver.find_element_by_id('username').()
driver.find_element_by_id('username').send_keys("13761151584")
# driver.find_element_by_id('password').clear()
driver.find_element_by_id('password').send_keys("Qwert12345@")
driver.find_element_by_class_name("logging").click()
time.sleep(2)
# driver.get("https://download.csdn.net/download/peel0/1878822")

cookies=driver.get_cookies()
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

url = "https://download.csdn.net/download/vanridin/10105089"
resp=session.get(url)

searchObj2 = re.search("<a href=\"(https://.*?)\" id=\"vip_btn\" class=\"dl_btn vip_dl_btn\">VIP下载</a>", resp.text)
url=searchObj2.group(1)
resp = session.get(url,  allow_redirects=False)
print(resp.headers['Location'])
# resp=session.get("https://download.csdn.net/index.php/vip_download/download_client/10298645/")
print(resp.text)