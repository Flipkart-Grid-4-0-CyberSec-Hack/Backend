from flask import Flask,request,jsonify
from cvefinder.getPackagesandVulnerabilities import *
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "Flask Server Working !!!"

@app.route("/getvulnerablepackages",methods = ['GET'])
def find_vulnerable_packages():
    url = request.args.get('url')
    rightLink = projectLink(url)

    if rightLink == "Network Error":
        return jsonify({"error":"Network Error"})

    packages = findPackages(rightLink)

    if packages == "Network Error":
        return jsonify({"error":"Network Error"})

    data = {
        'orginalurl':url,
        'projecturl':rightLink,
        'packages':[]
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


app.run(port = 8000, debug = True)