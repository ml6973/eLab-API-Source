import requests
import time
import json
import api.configuration.globalVars as globalVars


# Boot a virtual machine (lab environment) and return compute id
def boot_vm(token_id, name, imageid):
    # Replaces {0} from config file with the appropriate tenant id
    url2 = globalVars.jetstreamComputeURL.format(globalVars.jetstreamTenantID)

    with open('cfgb64.sh', 'r') as configfile:
        config_b64 = configfile.read()

    # print config file for debugging purposes
    print config_b64

    body = {
            "server": {
                "name": name,
                "imageRef": imageid,
                "flavorRef": "3",
                "networks": [{"uuid": globalVars.jetstreamNetworkID}],
                "user_data": config_b64
                }
            }

    my_headers = {"Content-Type": 'application/json', "X-Auth-Token": token_id}

    json_body = json.dumps(body)

    r = requests.post(url2, json_body, headers=my_headers)
    print json.dumps(r.json(), indent=4)

    this_compute_id = r.json()['server']['id']
 
    # continually sleeps until cloud has fully populated the response with
    # the data we need
    time.sleep(5)
    response = query_vm(token_id, this_compute_id)
    while(response.json()['server']['OS-EXT-STS:task_state'] != None):
        time.sleep(5)
        response = query_vm(token_id, this_compute_id)


    return this_compute_id


# Delete VM from cloud
def delete_vm(token_id, server_id):
    url = globalVars.jetstreamComputeURL.format(globalVars.jetstreamTenantID) + '/' + server_id

    my_headers = {"Content-Type": 'application/json', "X-Auth-Token": token_id}

    r = requests.delete(url, headers=my_headers)
    print r


# Check cloud for available floating IPs, return first unused
def get_unused_floating_ip(token_id):
    url = (globalVars.jetstreamComputeURL2.format(globalVars.jetstreamTenantID) +
           '/os-floating-ips')

    my_headers = {"Content-Type": 'application/json', "X-Auth-Token": token_id}

    r = requests.get(url, headers=my_headers)
    print json.dumps(r.json(), indent=4)

    floating_ip = None

    num_ips = len(r.json()['floating_ips'])

    # loop through all floating IPs and find first unused
    for x in range(0, num_ips):
        if r.json()['floating_ips'][x]['instance_id'] is None:
            floating_ip = r.json()['floating_ips'][x]['ip']
            break

    return floating_ip


# Assign floating IP to a given instance
def associate_floating_ip(token_id, server_id, this_floating_ip):
    url = (globalVars.jetstreamComputeURL.format(globalVars.jetstreamTenantID) + '/' +
           server_id + '/action')

    my_headers = {"Content-Type": 'application/json', "X-Auth-Token": token_id}
    body = {
            "addFloatingIp": {
                "address": this_floating_ip
                }
            }

    json_body = json.dumps(body)
    r = requests.post(url, json_body, headers=my_headers)


# Query cloud for various VM info, print to console
def query_vm(token_id, server_id):
    url = globalVars.jetstreamComputeURL.format(globalVars.jetstreamTenantID) + '/' + server_id

    my_headers = {"Content-Type": 'application/json', "X-Auth-Token": token_id}

    r = requests.get(url, headers=my_headers)

    print json.dumps(r.json(), indent=4)
    return r


# Reset VM to base image
def rebuild_vm(token_id, server_id, image_id, name):
    url = (globalVars.jetstreamComputeURL.format(globalVars.jetstreamTenantID) + '/' +
           server_id + '/action')

    body = {
            "rebuild": {
                "imageRef": image_id,
                "name": name
                }
            }

    my_headers = {"Content-Type": 'application/json', "X-Auth-Token": token_id}
    json_body = json.dumps(body)

    r = requests.post(url, json_body, headers=my_headers)
    return r
