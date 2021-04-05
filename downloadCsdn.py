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
driver.find_element_by_id('username').send_keys("13817249443")
# driver.find_element_by_id('password').clear()
driver.find_element_by_id('password').send_keys("Qwert12345@")
driver.find_element_by_class_name("logging").click()
time.sleep(2)
driver.get("https://download.csdn.net/download/peel0/1878822")
time.sleep(1)
driver.find_element_by_class_name("direct_download").click()
time.sleep(2)
aaa=driver.find_elements_by_class_name("js_download_btn")
for el in aaa:
    if el.get_attribute("data-href"):
        el.click()
print("waitdownload")
time.sleep(2)
driver.get("chrome://downloads/")
print(driver.page_source)
# time.sleep(20)
# driver.close()