import os

import time
from selenium import webdriver
from bs4 import BeautifulSoup

chromeOptions = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# chromeOptions.add_experimental_option("prefs", prefs)
path = os.getcwd() + "\\files\\2018"
prefs = {"download.default_directory": path,"profile.managed_default_content_settings.images": 2}
chromeOptions.add_experimental_option("prefs", prefs)
# PROXY = ipProxy.getIp()  # IP:PORT or HOST:PORT
# PROXY = "101.81.52.97:28803"  # IP:PORT or HOST:PORT
# print(PROXY)
# # time.sleep(5)
# chromeOptions.add_argument('--proxy-server=http://%s' % PROXY)
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.get("https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.21-winx64.zip")

driver.get("chrome://downloads/")
q=driver.execute_script('return document.getElementsByTagName("downloads-manager")[0].shadowRoot.children["downloads-list"]._physicalItems[0].content.querySelectorAll("#file-link")[0].href;')
fileName=driver.execute_script('return document.getElementsByTagName("downloads-manager")[0].shadowRoot.children["downloads-list"]._physicalItems[0].content.querySelectorAll("#name")[0].innerHTML;')

def compare(x, y):
    stat_x = os.stat(path + "/" + x)
    stat_y = os.stat(path + "/" + y)
    if stat_x.st_ctime < stat_y.st_ctime:
        return -1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return 1
    else:
        return 0
def findDownFileName(srcFileName):
    times = 500
    while 1:
        iterms = os.listdir(path)
        m_time = 0
        fileName = ""
        for item in iterms:
            stat = os.stat(path + "/" + item)
            if stat.st_mtime > m_time:
                fileName = item
        if ".crdownload" not in fileName:
            return fileName
        times -= 1
        if times < 0:
            return None
        time.sleep(1)





print(findDownFileName("mysql"))

