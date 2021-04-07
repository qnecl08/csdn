import re

line = "goldarowana@163.com https://download.csdn.net/download/shanshanxiao/1807189#comment";
line = "https://download.csdn.net/download/weixin_38490884/9849039 tzz1555@qq.com";

searchObj = re.search('([A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+)', line)

searchObj2=re.search('(download.csdn.net/download/.*?/\\d+)',line)
if searchObj:
    print("searchObj.group() : ", searchObj.group(0))
    print("searchObj.group(1) : ", searchObj.group(1))
    print("searchObj.group(2) : ", searchObj.group(2))
else:
    print("Nothing found!!")

if searchObj2:
    print(searchObj2.group(0))
    print(searchObj2.group(1))