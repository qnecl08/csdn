import requests


def getIp():
    url="http://120.25.150.39:8081/index.php/api/entry?method=proxyServer.generate_api_url&packid=&fa=&qty=1&time=2&pro=%E5%8C%97%E4%BA%AC%E7%9B%B4%E8%BE%96%E5%B8%82&city=&port=1&format=txt&ss=1&css=&dt=1"
    resp=requests.get(url)
    return resp.text