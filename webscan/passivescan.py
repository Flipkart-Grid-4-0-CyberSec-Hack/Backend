from zapv2 import ZAPv2
from .apikey import key
import time 

# Only run after spider Scans
def passiveScan(url):
    try:
        zap = ZAPv2(apikey=key, proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'})
        timeout = time.time() + 30
        while int(zap.pscan.records_to_scan) > 0:
            if time.time() > timeout:
                break
        ans = 0 
        issues = []
        for alert in zap.core.alerts():
            issues.append(alert)
            ans += 1
            if ans == 15:
                break
        return issues
    except Exception as e:
        return str(e)