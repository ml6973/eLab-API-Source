import api.configuration.globalVars as globalVars
import requests
import json


def auth():
    url = globalVars.jetstreamAuthURL

    body = {
            "auth": {
                "identity": {
		    "methods": [
		        "password"
		    ],
                    "password": {
		        "user": {
                            "name": globalVars.jetstreamCloudUsername,
			    "domain": {
			        "name": "tacc"
			    },
                            "password": globalVars.jetstreamCloudPassword
			}
                    }
                },
		"scope": {
		    "project": {
		        "id": globalVars.jetstreamTenantID
		    }
		}
            }
	}

    my_headers = {"Content-Type": 'application/json'}

    json_body = json.dumps(body)

    r = requests.post(url, json_body, headers=my_headers)
    # print json.dumps(body, indent=4)
    # print json.dumps(r.json(), indent=4)
    token_id = r.headers['X-Subject-Token']
    return token_id
