import api.configuration.globalVars as globalVars
import requests
import json

def bootVM(token_id, name, imageid):
    #Replaces {0} from config file with the appropriate tenant id
    url2 = globalVars.computeURL.format(globalVars.tenant_id) 

    with open('cfgb64.sh', 'r') as configfile:
        config_b64 = configfile.read()

    print config_b64

    body = {"server": 
                {"name": name,
                 "imageRef": imageid,
                 "flavorRef": "5",
                 "networks":[{"uuid":globalVars.networkID}],
                 "user_data":config_b64
                 }
            }

    my_headers = {"Content-Type": 'application/json', "X-Auth-Token": token_id}

    json_body = json.dumps(body)

    r = requests.post(url2, json_body, headers=my_headers)
    print json.dumps(r.json(), indent=4)
    return r.json()['server']['id']

def deleteVM(token_id, server_id):
    url = globalVars.computeURL.format(globalVars.tenant_id) + '/' + server_id

    my_headers = {"Content-Type": 'application/json',"X-Auth-Token": token_id}

    r = requests.delete(url, headers=my_headers)
    print r

def get_unused_floating_ip(token_id):
    url = globalVars.computeURL2.format(globalVars.tenant_id) + '/os-floating-ips'

    my_headers = {"Content-Type": 'application/json',"X-Auth-Token": token_id}
    
    r = requests.get(url, headers=my_headers)
    print json.dumps(r.json(), indent=4)

    floating_ip = None

    num_ips = len(r.json()['floating_ips'])

    #loop through all floating IPs and find first unused
    for x in range(0, num_ips):
        if r.json()['floating_ips'][x]['instance_id'] is None:
            floating_ip = r.json()['floating_ips'][x]['ip']
            break

    return floating_ip

def associate_floating_ip(token_id, server_id, this_floating_ip):
    url = globalVars.computeURL.format(globalVars.tenant_id) + '/' + server_id + '/action'

    my_headers = {"Content-Type": 'application/json',"X-Auth-Token": token_id}
    body = {"addFloatingIp": 
                {"address": this_floating_ip}
            }

    json_body = json.dumps(body)
    r = requests.post(url, json_body, headers=my_headers)

def queryVM(token_id, server_id):
    url = globalVars.computeURL.format(globalVars.tenant_id) + '/' + server_id

    my_headers = {"Content-Type": 'application/json',"X-Auth-Token": token_id}

    r = requests.get(url, headers=my_headers)
    
    print json.dumps(r.json(), indent=4)

    '''
    if(r.json()['server']['addresses']['internal'][0]['version'] == 6):
        print r.json()['server']['addresses']['internal'][1]['addr']
    else:
        print r.json()['server']['addresses']['internal'][0]['addr']
    '''

    return r

def rebuildVM(token_id, server_id, image_id, name):
    url = globalVars.computeURL.format(globalVars.tenant_id) + '/' + server_id + '/action'

    body = {"rebuild":
                {"imageRef" : image_id,
                 "name" : name
                }
            }

    my_headers = {"Content-Type": 'application/json',"X-Auth-Token": token_id}
    json_body = json.dumps(body)

    r = requests.post(url, json_body, headers=my_headers)
    return r

