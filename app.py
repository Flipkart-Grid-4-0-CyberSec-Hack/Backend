from flask import Flask,request,jsonify
from cvefinder.getPackagesandVulnerabilities import *
from flask_cors import CORS
from webscan.webapplinkfinder import getWebAppLink
from webscan.ajaxspider import ajaxSpider
from webscan.passivescan import passiveScan
from webscan.spiderscan import spiderScan
from webscan.activeScan import activeScan

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Flask Server Working !!!"

@app.route("/getvulnerablepackages",methods = ['GET'])
def find_vulnerable_packages():
    url = request.args.get('url')
    rightLink = projectLink(url)

    if "http" not in rightLink:
        return jsonify({"error":rightLink})

    weblink = getWebAppLink(rightLink)
    if "http" not in weblink:
        weblink = None
    packages = findPackages(rightLink)

    if type(packages) == str:
        return jsonify({"error":packages})

    data = {
        'orginalurl':url,
        'projecturl':rightLink,
        'packages':[],
        'webLink' : weblink
    }


    for elem in packages:
        package = {
            'name': elem,
            'version' : packages[elem],
            'vulnerability': []
        }
        vulnerabilityData = findVulnerability(elem,packages[elem])
        for el in vulnerabilityData:
            package['vulnerability'].append({
                'CVE' : el,
                'description' : vulnerabilityData[el]
            })

        data['packages'].append(package)
    return jsonify(data)

@app.route("/runscan",methods = ['GET'])
def runScan():
    url = request.args.get('url')
    spider = request.args.get('spider')
    ajaxspider = request.args.get('ajaxspider')
    passivescan = request.args.get('passivescan')
    activescan = request.args.get('activescan')

    if spider == 'true':
        results = spiderScan(url)
    elif ajaxspider == 'true':
        results = ajaxSpider(url)
    elif passivescan == 'true':
        results = passiveScan(url)
    else : 
        results = activeScan(url)

    if type(results) == str:
        return jsonify({"error" : results})
    
    return jsonify(results)



    


app.run(port = 8000, debug = True, threaded = True)