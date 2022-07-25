from bs4 import BeautifulSoup
import requests

desired_list_of_files = []

def currentUrl(url, branch, first = True):
    global desired_list_of_files 
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    files_and_folders = soup.find_all('div',class_ = 'Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item')
    for elem in files_and_folders:
        type = elem.find('div',class_ = 'mr-3 flex-shrink-0').svg['aria-label']
        name = elem.find('a',class_ = 'js-navigation-open Link--primary').text
        if type == 'Directory':
            if first:
                currentUrl(url + '/tree/' + branch + '/' + name,branch, False)
            else : 
                currentUrl(url + '/' + name,branch, False)
        else : 
            fileurl = url + '/' + name 
            fileurl = fileurl.replace('github.com','raw.githubusercontent.com')
            fileurl = fileurl.replace('tree/','')
            desired_list_of_files.append({
                'name' : name,
                'url' : fileurl})

def findAllFiles(url):
    global desired_list_of_files
    desired_list_of_files.clear()
    try : 
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        branch = soup.find('span',class_='css-truncate-target').text
        currentUrl(url,branch)
        return desired_list_of_files
    except Exception as e :
        return str(e)