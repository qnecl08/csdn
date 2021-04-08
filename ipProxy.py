import requests


def getIp():
    url="http://120.25.150.39:8081/index.php/api/entry?method=proxyServer.generate_api_url&packid=&fa=&qty=1&time=3&pro=%E4%B8%8A%E6%B5%B7%E7%9B%B4%E8%BE%96%E5%B8%82&city=&port=1&format=txt&ss=1&css=&dt=1"
    resp=requests.get(url)
    proxies = {"http": "http://"+resp.text, "https": "http://"+resp.text, }
    print(proxies)
    try:
        resp2=requests.get("http://www.ip138.com/", proxies=proxies)
        print(resp2.text)
        return resp.text
    except Exception as e:
        return getIp()



if __name__ == "__main__":
   print(getIp())