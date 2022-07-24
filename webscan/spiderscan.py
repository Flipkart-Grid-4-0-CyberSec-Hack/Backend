from zapv2 import ZAPv2
from .apikey import key 
import time 


def spiderScan(url):
    try:
        zap = ZAPv2(apikey=key)
        scanID = zap.spider.scan(url)

        foundUrls = []
        timeout = time.time() + 30 
        while int(zap.spider.status(scanID)) < 100:
            if timeout < time.time():
                break
        ans = 0 
        for elem in zap.spider.results():
            foundUrls.append(elem)
            ans += 1
            if ans == 15 : break 
        return foundUrls
    except Exception as e:
        return str(e)