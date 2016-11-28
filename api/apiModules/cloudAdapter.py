import api.configuration.globalVars as globalVars
import api.models as modelFunctions
from api.models import Cloud
import api.cloudModules.cloudAuth as cloudAuth
import api.cloudModules.cloudCompute as cloudCompute
import api.cloudModules.cloudImages as cloudImages
import api.cloudModules.aws.awsAuth as awsAuth
import api.cloudModules.aws.awsImages as awsImages
import api.cloudModules.aws.awsCompute as awsCompute
import json
from rest_framework import status

# These functions allow for multi-cloud support by allowing single function calls for shared cloud commands

# Updates the catalog from all clouds
def updateCatalog():
    globalVars.init()

    #Update the catalog from Chameleon
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


    #Update the catalog from AWS
    client = awsAuth.authClient(globalVars.awsAccess, 
                          globalVars.awsSecret, 
                          globalVars.awsRegion)
    images = awsImages.getImageList(client)
    cloud = Cloud.objects.get(name='aws')
    for image in images:
        print image
        modelFunctions.get_or_create_image(cloud,
	                                   image['ImageId'],
					   image['Name'],
					   image['Description'])


# Boots a VM, cloud used is dependent on the request
def boot_vm(instance_name, cloudId, cloud):
   globalVars.init()

   # Chameleon Cloud instance booting
   if (cloud == "chameleon"):
       my_token_id = cloudAuth.auth()
       instanceId = cloudCompute.boot_vm(my_token_id, instance_name, cloudId)
       return instanceId


   # AWS instance booting
   if (cloud == "aws"):
       resource = awsAuth.authResource(globalVars.awsAccess,
                                       globalVars.awsSecret, 
			               globalVars.awsRegion)
       instanceId = awsCompute.boot_vm(resource, instance_name, cloudId)
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
def get_unused_floating_ip(cloud, computeId):
    globalVars.init()
    
    # Chameleon Cloud floating ip retrieval
    if (cloud == "chameleon"):
	my_token_id = cloudAuth.auth()
	floatingIp = cloudCompute.get_unused_floating_ip(my_token_id)
	return floatingIp


    # AWS Cloud floating ip retrieval
    if (cloud == "aws"):
        # AWS can assign floating IPs automatically, we simply return it
	resource = awsAuth.authResource(globalVars.awsAccess,
	                                globalVars.awsSecret,
					globalVars.awsRegion)
	floatIp = awsCompute.get_IP(resource, computeId)
	return floatIp


# Associates the given floating IP to the specified instance
def associate_floating_ip(computeId, floating_ip, cloud):

    # Chameleon Cloud floating ip association
    if (cloud == "chameleon"):
        globalVars.init()
	my_token_id = cloudAuth.auth()
	cloudCompute.associate_floating_ip(my_token_id, computeId, floating_ip)
	return


    # AWS Cloud floating ip association
    if (cloud == "aws"):
        # Using a dummy function as AWS associates floating IPs automatically
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

    # AWS Cloud rebuild VM
    # AWS Does not support direct rebuilding, using a dummy function
    if (cloud == "aws"):
        return status.HTTP_200_OK
