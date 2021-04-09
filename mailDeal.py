
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import threading

import time

import pickle

import csdnDownDb
from selenium import webdriver

class mailDeal(threading.Thread):
    appWatch={}
    def run(self):  # 定义每个线程要运行的函数
        try:
            while 1:
                self.watchMail()
        except Exception as e:
            print(str(e))
            return False

    def __init__(self,appWatch):
        threading.Thread.__init__(self)
        self.appWatch=appWatch
    def watchMail(self):
        obj = pickle.load(open("./mail163" + ".txt", "rb+"))
        print(obj)
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome()
        driver.maximize_window()  # 浏览器最大化
        time.sleep(1)
        url = 'https://mail.163.com/js6/main.jsp'
        driver.get(url)
        for cookie in obj:
            driver.add_cookie(cookie)
        driver.get(url)
        btnLogout = driver.find_element_by_id("btnLogout")
        btnLogout.click()
        while 1:
            try:
                time.sleep(1)
                files=csdnDownDb.getFileToMail()
                print("发邮件列表",files)
                for file in files:
                    driver.get("https://mail.163.com/js6/main.jsp")
                    btnLogout = driver.find_element_by_id("btnLogout")
                    btnLogout.click()
                    time.sleep(1)
                    _mail_component_70_70 = driver.find_element_by_id("_mail_component_70_70")
                    _mail_component_70_70.click()

                    time.sleep(3)
                    by0 = driver.find_element_by_class_name("by0")
                    input = by0.find_element_by_tag_name("input")
                    input.send_keys(file['path']+""+file['file_name'])
                    nui = driver.find_element_by_class_name("nui-editableAddr-ipt")
                    nui.send_keys(file['mail'])
                    mainBtn = driver.find_element_by_class_name("nui-mainBtn")
                    mainBtn.click()
                    pv1 = ""
                    msgbox = ""
                    while 1:
                        time.sleep(3)
                        try:
                            pv1 = driver.find_element_by_class_name("pv1")
                        except Exception:
                            pass
                        if pv1:
                            csdnDownDb.updateFileStep(file['id'],1)
                            print("发邮件成功",file)
                            break
                        try:
                            msgbox = driver.find_element_by_class_name("nui-msgbox-title")
                        except Exception:
                            pass
                        if msgbox:
                            print("发送失败")
                            break
                driver.refresh()
                cookies = driver.get_cookies()
                byte_data = pickle.dump(cookies, open("./mail163" + ".txt", "wb+"))
                time.sleep(5)
            except Exception as e:
                print("发邮件异常",str(e))



if __name__ == "__main__":
    mail=mailDeal("")
    mail.start()
    while 1:
        time.sleep(3)