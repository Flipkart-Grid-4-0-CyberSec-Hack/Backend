import requests
from bs4 import BeautifulSoup


def findCVEScore(CVEID):
    try:
        url = f'https://www.cvedetails.com/cve/{CVEID}/?q={CVEID}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return float(soup.find('div',class_='cvssbox').text)
    except Exception as e :
        return str(e)                


