import api.configuration.globalVars as globalVars
import requests
import json

def auth():
    #url = 'http://129.114.110.198:5000/v2.0/tokens'
    url = globalVars.authURL
    
    body = {"auth" : 
               {"tenantName": "admin",
                "passwordCredentials": 
                   {"username": "admin",
                    "password": "secrete"}}}
                        
    json_body = json.dumps(body)

    r = requests.post(url, json_body)
    #print json.dumps(body, indent=4)
    #print json.dumps(r.json(), indent=4)
    globalVars.tenant_id = r.json()['access']['token']['tenant']['id']
    token_id = r.json()['access']['token']['id']
    return token_id
