# 包含文件
import upyun

# 创建实例
up = upyun.UpYun('daixiazai', 'dandinglong', 'zc59763451')

headers = { 'x-gmkerl-thumb': '/fw/300' }

with open('./files/chromedriver_win32.zip', 'rb') as f:
    res = up.put('/up/chromedriver_win32.zip', f, checksum=True)
    print(res)

res = up.usage()
print(res)