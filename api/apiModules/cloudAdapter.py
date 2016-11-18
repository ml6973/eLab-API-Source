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


# Boots a VM, cloud used is dependent on the request
def boot_vm(instance_name, cloudId, cloud):
   
   # Chameleon Cloud instance booting
   if (cloud == "chameleon"):
       globalVars.init()
       my_token_id = cloudAuth.auth()
       instanceId = cloudCompute.boot_vm(my_token_id, instance_name, cloudId)
       return instanceId


# Queries a VM, cloud queried is dependent on the request
def query_vm(computeId, cloud):

    # Chameleon Cloud instance querying
    if (cloud == "chameleon"):
       globalVars.init()
       my_token_id = cloudAuth.auth()
       response = cloudCompute.query_vm(my_token_id, computeId)
       return response


# Retrieves an available floating IP address from a specific cloud
def get_unused_floating_ip(cloud):

    # Chameleon Cloud floating ip retrival
    if (cloud == "chameleon"):
        globalVars.init()
	my_token_id = cloudAuth.auth()
	floatingIp = cloudCompute.get_unused_floating_ip(my_token_id)
	return floatingIp


# Associates the given floating IP to the specified instance
def associate_floating_ip(computeId, floating_ip, cloud):

    # Chameleon Cloud floating ip association
    if (cloud == "chameleon"):
        globalVars.init()
	my_token_id = cloudAuth.auth()
	cloudCompute.associate_floating_ip(my_token_id, computeId, floating_ip)
	return


# Rebuilds a VM from the base image
def rebuild_vm(computeId, imageId, instanceName, cloud):

    # Chameleon Cloud rebuild VM
    if (cloud == "chameleon"):
        globalVars.init()
	my_token_id = cloudAuth.auth()
	response = cloudCompute.rebuild_vm(my_token_id,
	                                   computeId,
					   imageId,
					   instanceName)
	return response
