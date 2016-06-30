import configuration.globalVars as globalVars
import requests
import json

def bootVM(token_id, name, imageid):
    #Replaces {0} from config file with the appropriate tenant id
    url2 = globalVars.computeURL.format(globalVars.tenant_id) 

    body = {"server": 
                {"name": name,
                 "imageRef": imageid,
                 "flavorRef": "1"}}

    my_headers = {"X-Auth-Token": token_id}

    json_body = json.dumps(body)

    r = requests.post(url2, json_body, headers=my_headers)
    #print json.dumps(r.json(), indent=4)
    return r.json()['server']['id']

def deleteVM(token_id, server_id):
    url = globalVars.computeURL.format(globalVars.tenant_id) + '/' + server_id

    my_headers = {"X-Auth-Token": token_id}

    r = requests.delete(url, headers=my_headers)
    print r

def queryVM(token_id, server_id):
    url = globalVars.computeURL.format(globalVars.tenant_id) + '/' + server_id

    my_headers = {"X-Auth-Token": token_id}

    r = requests.get(url, headers=my_headers)
    
    print json.dumps(r.json(), indent=4)
    #print r
    print r.json()['server']['addresses']['private'][0]['addr']
    return r

def rebuildVM(token_id, server_id, image_id):
    url = globalVars.computeURL.format(globalVars.tenant_id) + '/' + server_id + '/action'

    body = {"rebuild":
                {"imageRef" : image_id,
                 "name" : "default"}}

    my_headers = {"X-Auth-Token": token_id}
    json_body = json.dumps(body)

    r = requests.post(url, json_body, headers=my_headers)
    print r

