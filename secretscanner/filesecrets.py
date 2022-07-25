import requests 
import json 
import re 
import os 


def findSecrets(url):
    regex_objects = []
    # print("HERE")
    # print(os.getcwd())
    for elem in os.listdir('secretscanner/regexfiles'):
        f = open(f'secretscanner/regexfiles/{elem}','r')
        regex_objects.append(json.load(f))
        f.close()
    try :
        response = requests.get(url)
    except Exception as e:
        return []
    if 'text' in response.headers['content-type'] or 'json' in response.headers['content-type']:
        text = response.text
        data = []
        for elem in regex_objects:
            for key in elem:
                for secret in re.findall(elem[key],text):
                    data.append(secret)
        return data 
    else:
        return []
