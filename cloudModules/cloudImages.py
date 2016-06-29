import configuration.globalVars as globalVars
import requests
import json

def getImageList(token_id):
    #Connect to glance API
    url = globalVars.baseURL + ':9292/v2/images'

    my_headers = {"X-Auth-Token": token_id}

    r = requests.get(url, headers=my_headers)
    print json.dumps(r.json(), indent=4)
    return r
