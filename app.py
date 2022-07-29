from flask import Flask,request,jsonify
from flask_cors import CORS

from cvefinder.getPackagesandVulnerabilities import *
from cvefinder.CVEScorefinder import *

from webscan.webapplinkfinder import getWebAppLink
from webscan.ajaxspider import ajaxSpider
from webscan.passivescan import passiveScan
from webscan.spiderscan import spiderScan
from webscan.activeScan import activeScan


from secretscanner.filefinder import findAllFiles
from secretscanner.filesecrets import findSecrets


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
        return jsonify({"error":rightLink}),400

    weblink = getWebAppLink(rightLink)
    if "http" not in weblink:
        weblink = None
    packages = findPackages(rightLink)

    if type(packages) == str:
        return jsonify({"error":packages}),400

    data = {
        'orginalurl':url,
        'projecturl':rightLink,
        'packages':[],
        'webLink' : weblink,
        'CVSS_Score' : 0,
    }

    total_CVSS_Score = 0
    ans = 0 
    for elem in packages:
        package_CVSS_Score = 0
        package = {
            'name': elem,
            'version' : packages[elem],
            'vulnerability': [],
            'CVSS_Score' : 0,
        }
        vulnerabilityData = findVulnerability(elem,packages[elem])
        for el in vulnerabilityData:
            package['vulnerability'].append({
                'CVE' : el,
                'description' : vulnerabilityData[el],
                'CVSS_Score' : findCVEScore(el)
            })            
            package_CVSS_Score += findCVEScore(el)
        if len(package['vulnerability']) > 0:
            ans += 1
            package['CVSS_Score'] = package_CVSS_Score/len(package['vulnerability'])
        data['packages'].append(package)
        total_CVSS_Score += package['CVSS_Score']
    if len(data['packages']) > 0:
        data['CVSS_Score'] = total_CVSS_Score/ans
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
        return jsonify({"error" : results}),400
    
    return jsonify(results)


@app.route("/findsecrets",methods = ['GET'])
def findsecrets():
    url = request.args.get('url')
    filedata = findAllFiles(url)
    if type(filedata) == str:
        return jsonify({'error' : filedata}),400
    final_data = []
    for elem in filedata:
        final_data.append({
            'file' : elem['name'],
            'url' : elem['url'],
            'secrets' : findSecrets(elem['url'])
        })
    
    return jsonify(final_data)



    


app.run(port = 8000, debug = True, threaded = True)