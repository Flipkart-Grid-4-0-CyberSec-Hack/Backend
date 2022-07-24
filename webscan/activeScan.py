import time 
from zapv2 import ZAPv2
from .apikey import key

# Run only after Spider Scan 
def activeScan(url):
    try:
        zap = ZAPv2(apikey=key , proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})
        scanID = zap.ascan.scan(url)
        timeout = time.time() + 30 
        while int(zap.ascan.status(scanID)) < 100:
            if timeout < time.time(): break 
        
        issues = []
        ans = 0 
        for alert in zap.core.alerts():
            issues.append(alert)
            ans += 1
            if ans == 15:
                break
        return issues
    except Exception as e:
        return str(e)