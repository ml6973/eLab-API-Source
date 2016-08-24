import api.configuration.globalVars as globalVars
import requests
import json


def auth():
    url = globalVars.authURL

    body = {
            "auth": {
                "tenantName": globalVars.tenantName,
                "passwordCredentials": {
                    "username": globalVars.cloudUsername,
                    "password": globalVars.cloudPassword
                    }
                }
            }

    my_headers = {"Content-Type": 'application/json'}

    json_body = json.dumps(body)

    r = requests.post(url, json_body, headers=my_headers)
    # print json.dumps(body, indent=4)
    # print json.dumps(r.json(), indent=4)
    globalVars.tenant_id = r.json()['access']['token']['tenant']['id']
    token_id = r.json()['access']['token']['id']
    return token_id
