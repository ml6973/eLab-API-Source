import api.cloudModules.cloudAuth as cloudAuth
import api.cloudModules.cloudCompute as cloudCompute
import api.cloudModules.cloudImages as cloudImages
import api.configuration.globalVars as globalVars
import api.models as modelFunctions
import json


def updateCatalog(my_token_id):
    r = cloudImages.getImageList(my_token_id)
    print json.dumps(r.json(), indent=4)

    for image in r.json()['images']:
    	if image['owner'] == globalVars.tenantName:
	    	this_description = ""
	    	
	    	if 'description' in image:
	    		this_description = image['description']
	        modelFunctions.get_or_create_image(image['id'], image['name'], this_description)
    
    
