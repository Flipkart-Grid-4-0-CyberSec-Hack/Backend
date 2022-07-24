from zapv2 import ZAPv2
from .apikey import key 
import time 


## Only run after Spider Scan 

def ajaxSpider(url):

    try:
        zap = ZAPv2(apikey=key)
        scanID = zap.ajaxSpider.scan(url)
        results = []
        timeout = time.time() + 30 
        ans = 0    
        while zap.ajaxSpider.status == 'running':
            if time.time() > timeout:
                break
        for elem in zap.ajaxSpider.results():
            results.append(elem)
            ans += 1
            if ans > 15 :
                break
        return results
    except Exception as e:
        return str(e)
