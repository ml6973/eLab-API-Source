import requests
import json

tenant_id = ""

def keystone_auth():
    global tenant_id
    url = 'http://129.114.110.199:5000/v2.0/tokens'
    
    body = {"auth" : 
               {"tenantName": "admin",
                "passwordCredentials": 
                   {"username": "admin",
                    "password": "password"}}}
                        
    json_body = json.dumps(body)

    r = requests.post(url, json_body)
    #print json.dumps(body, indent=4)
    #print json.dumps(r.json(), indent=4)
    tenant_id += r.json()['access']['token']['tenant']['id']
    token_id = r.json()['access']['token']['id']
    return token_id

def novaboot(token_id):
    global tenant_id
    url2 = 'http://129.114.110.199:8774/v2.1/' + tenant_id + '/servers'
    print url2

    body = {"server": 
                {"name": "ryan-server-test",
                 "imageRef": "4ee51968-3fce-49ba-aa34-4bae39f63229",
                 "flavorRef": "1"}}

    my_headers = {"X-Auth-Token": token_id}

    json_body = json.dumps(body)

    r = requests.post(url2, json_body, headers=my_headers)
    print r

my_token_id = keystone_auth()
novaboot(my_token_id)
