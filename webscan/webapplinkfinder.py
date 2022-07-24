from bs4 import BeautifulSoup
import requests

def getWebAppLink(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        anchor = soup.find('span',class_='flex-auto min-width-0 css-truncate css-truncate-target width-fit')
        url = anchor.a.get('href')
        return url
    except Exception as e:
        return str(e)

