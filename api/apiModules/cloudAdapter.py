import api.configuration.globalVars as globalVars
import api.models as modelFunctions
from api.models import Cloud
import api.cloudModules.cloudAuth as cloudAuth
import api.cloudModules.cloudCompute as cloudCompute
import api.cloudModules.cloudImages as cloudImages
import json

# These functions allow for multi-cloud support by allowing single function calls for shared cloud commands

# Updates the catalog from all clouds
def updateCatalog():

    #Update the catalog from Chameleon
    globalVars.init()
    my_token_id = cloudAuth.auth()
    r = cloudImages.getImageList(my_token_id)
    print json.dumps(r.json(), indent=4)
    cloud = Cloud.objects.get(name='chameleon')
    for image in r.json()['images']:
        if image['owner'] == globalVars.tenantName:
	    this_description = ""

            if 'description' in image:
                this_description = image['description']
	    modelFunctions.get_or_create_image(cloud,
	                                       image['id'],
					       image['name'],
					       this_description)

    
# Authenticates with a cloud based on request
def auth(request):
    if (request.data['cloud'] == 'chameleon'):
        return cloudAuth.auth()
