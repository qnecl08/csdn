import pickle
import threading

import csdnDownDb
import taobaoDb
import time
from selenium import webdriver

class csdnLogin(threading.Thread):
    lasttime=time.strftime("%Y-%m-%d", time.localtime())
    def run(self):  # 定义每个线程要运行的函数
        try:
            while 1:
                self.watchChrome()
        except Exception as e:
            print(str(e))
            return False

    def __init__(self):
        threading.Thread.__init__(self)
    def watchChrome(self):
        while 1:
            try:
                accounts=csdnDownDb.allAccount()
                for account in accounts:
                    chromeOptions = webdriver.ChromeOptions()
                    prefs = {"profile.managed_default_content_settings.images": 2}
                    chromeOptions.add_experimental_option("prefs", prefs)
                    # chromeOptions.add_argument('--proxy-server=http://%s' % PROXY)
                    driver = webdriver.Chrome(chrome_options=chromeOptions)
                    url = 'https://passport.csdn.net/account/login'
                    driver.get(url)
                    driver.find_element_by_id('username').send_keys(account['account'])
                    driver.find_element_by_id('password').send_keys(account['password'])
                    driver.find_element_by_class_name("logging").click()
                    times = 3
                    while 1:
                        if "www.csdn.net" in driver.current_url:
                            cookies = driver.get_cookies()
                            pickle.dump(cookies, open("./files/cookies/"+account['account']+ ".txt", "wb+"))
                            break
                        times -= 1
                        if times < 0:
                            break
                        time.sleep(3)
                    driver.quit()
                    time.sleep(1)
            except Exception as e:
                print("异常",str(e))
                driver.quit()
            self.todayTimesToZero()
            time.sleep(60*10)
    def todayTimesToZero(self):
        if self.lasttime!=time.strftime("%Y-%m-%d", time.localtime()) :
            csdnDownDb.updateTodayTimes()

if __name__ == "__main__":
    t=csdnLogin()
    t.start()








