import requests
from bs4 import BeautifulSoup
import re 
from packaging import version 


def projectLink(url):
    if 'pypi.org' in url.split('/'):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            anchor = soup.find('a',class_='vertical-tabs__tab vertical-tabs__tab--with-icon vertical-tabs__tab--condensed')
            return anchor.get('href')
        except Exception as e: 
            return str(e)
    elif 'www.npmjs.com' in url.split('/'):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            anchor = soup.find('a',class_='b2812e30 f2874b88 fw6 mb3 mt2 truncate black-80 f4 link')
            return anchor.get('href')
        except Exception as e:
            return str(e)
    elif 'github.com' in url.split('/'):
        return url 
    else : 
        return "Link not supported"

def findPackages(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        files_and_folders = soup.find_all('a',class_='js-navigation-open Link--primary')
        branch = soup.find('details',class_='details-reset details-overlay mr-0 mb-0').find('span',class_='css-truncate-target').text
    except Exception as e:
        return str(e)
    packages = {}
    for elem in files_and_folders: 
        if 'requirements.txt' in elem.text:
            try:
                response = requests.get(url.replace('github.com','raw.githubusercontent.com') + f'/{branch}/requirements.txt')
            except Exception as e:
                return str(e)
            unfiltered_text = response.text
            curr_string = ''

            for elem in unfiltered_text:
                if elem == '\n':
                    data = curr_string.split('==')
                    if len(data) == 2:
                        packages[data[0]] = data[1]
                    curr_string = ''
                elif ord(elem) > 0 and ord(elem)< 128:
                    curr_string += elem
            break

        elif 'package.json' in elem.text:
            response = requests.get(url.replace('github.com','raw.githubusercontent.com') + f'/{branch}/package.json')
            packages = response.json()['dependencies']
            break

    return packages

def findVulnerability(package_name, package_version):
    try:
        url = f'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={package_name.lower()}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'xml')
        CVES = {}
    except Exception as e: 
        return str(e)
    for elem in soup.find_all('tr'):
        try:
            tds = elem.find_all('td')
            CVEID = tds[0].a.text
            CVEDescription = tds[1].text
            if 'CVE-' in CVEID:
                CVES[CVEID] = CVEDescription
        except:
            pass

    filtered_CVES = {}

    for CVEID in CVES:
        CVEDescription = CVES[CVEID]
        version_number = re.findall(r'\d+\.\d+\.\d+', CVEDescription)
        for versions in version_number:
            if version.parse(versions) >=  version.parse(package_version) and versions.split('.')[0] == package_version.split('.')[0]:
                filtered_CVES[CVEID] = CVEDescription
                break
    return filtered_CVES