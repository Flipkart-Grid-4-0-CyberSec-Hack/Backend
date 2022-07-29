# Security Inspector (Backend) : Repo Vulnerability Scanner 📁 💻 🐉

## Description : 


## Tech Stack (Frontend + Backend) 💻
```
1. React JS 
2. Flask Framework
3. Beautiful Soup Library
4. Owasp ZAP Proxy Tool
```

### Note: Approximate Running Time of Each API 🕥  30 sec to 1 minute

<br>

## Installation and Setup 🎛️

1. Install Stable OWASP ZAP Proxy from their Official Website
2. Install Python 3.10 Version from Official Website
3. Run OWASP ZAP Proxy Application. It runs on port 8080.
4. Get API Key of OWASP ZAP Proxy Application. Paste that API Key in WebScan/apikey.py file.
5. Run the following commands in main directory.

```
pip install -r requirements.txt
python app.py 
```

6. You are good to go !


## API Usage Examples

1. To get Vulnerable Packages of Repository 

Request Format

``` GET <url>/getvulnerablepackages?url={URL of your Open Source Project Pypi, GitHub, npm} ```

Sample Response 
```
{
    "CVSS_Score": 5.506909430438841,
    "orginalurl": "<Your URL>",
    "packages": [
        {
            "CVSS_Score": 6.075,
            "name": "amqp",
            "version": "1.4.9\r",
            "vulnerability": [
                {
                    "CVE": "CVE-2018-11087",
                    "CVSS_Score": 4.3,
                    "description": "Pivotal Spring AMQP, 1.x versions prior to 1.7.10 and 2.x versions prior to 2.0.6, expose a man-in-the-middle vulnerability due to lack of hostname validation. A malicious user that has the ability to intercept traffic would be able to view data in transit.\n\n"
                },
                {
                    "CVE": "CVE-2017-8045",
                    "CVSS_Score": 7.5,
                    "description": "In Pivotal Spring AMQP versions prior to 1.7.4, 1.6.11, and 1.5.7, an org.springframework.amqp.core.Message may be unsafely deserialized when being converted into a string. A malicious payload could be crafted to exploit this and enable a remote code execution attack.\n\n"
                },
               
                    ]
        }
        ],
        "projecturl": <GITHUB URL>
    "webLink": <WEB APP URL IF Applicable>
}
```

2. To get Secrets of a Repository


Request Format

``` GET <url>/findsecrets?url={URL of your Repo} ```

Sample Response

```
[
      {
        "file": "settings.py",
        "secrets": [
            "# SECURITY WARNING: keep the secret key used in production secret!",
            "SECRET_KEY = 'django-insecure-180(d!16vi4icc#nfc)83l*esib-ike^o_nuq@4anue@l+wf6+'"
        ],
        "url": "<Raw Url of File>"
    },
]
```


3. Web Scan API 

Request Format

``` GET <url>/runscan?url={URL of your Repo}?<typeofscan> = true?&<rest...> = false```

Sample Response Spider/Ajax Spider
```
[
    "https://github.com/trending/developers",
    "https://github.com/WerWolv/ImHex/stargazers",
    
]
```


Sample Response Active/Passive Scan (Run only after Spider Scans)
```
[

    {
        "alert": "Missing Anti-clickjacking Header",
        "alertRef": "10020-1",
        "attack": "",
        "confidence": "Medium",
        "cweid": "1021",
        "description": "The response does not include either Content-Security-Policy with 'frame-ancestors' directive or X-Frame-Options to protect against 'ClickJacking' attacks.",
        "evidence": "",
        "id": "0",
        "messageId": "4",
        "method": "GET",
        "name": "Missing Anti-clickjacking Header",
        "other": "",
        "param": "X-Frame-Options",
        "pluginId": "10020",
        "reference": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options",
        "risk": "Medium",
        "solution": "Modern Web browsers support the Content-Security-Policy and X-Frame-Options HTTP headers. Ensure one of them is set on all web pages returned by your site/app.\nIf you expect the page to be framed only by pages on your server (e.g. it's part of a FRAMESET) then you'll want to use SAMEORIGIN, otherwise if you never expect the page to be framed, you should use DENY. Alternatively consider implementing Content Security Policy's \"frame-ancestors\" directive.",
        "sourceid": "3",
        "tags": {
            "OWASP_2017_A06": "https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration.html",
            "OWASP_2021_A05": "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/",
            "WSTG-v42-CLNT-09": "https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/11-Client-side_Testing/09-Testing_for_Clickjacking"
        },
        "url": "https://public-firing-range.appspot.com",
        "wascid": "15"
    },

]
```


## Built by </>
## Built with ❤️
