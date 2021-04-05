from selenium import webdriver


chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory": "e:/download/python"}
chromeOptions.add_experimental_option("prefs", prefs)

PROXY = "116.226.25.247:28803"  # IP:PORT or HOST:PORT
chromeOptions.add_argument('--proxy-server=http://%s' % PROXY)
driver = webdriver.Chrome(chrome_options=chromeOptions)
# driver.get("http://cdn.npm.taobao.org/dist/chromedriver/2.37/chromedriver_win32.zip")
driver.get("http://www.ip138.com/")
