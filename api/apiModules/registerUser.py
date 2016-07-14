import api.cloudModules.cloudAuth as cloudAuth
import api.cloudModules.cloudCompute as cloudCompute
import api.cloudModules.cloudImages as cloudImages
import api.configuration.globalVars as globalVars
import time
from api.models import Image, Instance
import api.models as modelFunctions

def registerUser(uname, email, preferred_pass, my_token_id):
    this_user, created = modelFunctions.get_or_create_user(uname, email, preferred_pass)
    if created is True:
        createNewUserInstances(uname, my_token_id)
    else:
        return False

def createNewUserInstances(uname, my_token_id):
    for this_image in Image.objects.all():
        instance_name = uname + '-' + str(this_image.id)
        compute_id = cloudCompute.bootVM(my_token_id, instance_name, this_image.cloudId)

        time.sleep(5)
        response = cloudCompute.queryVM(my_token_id, compute_id)

        while(response.json()['server']['OS-EXT-STS:task_state'] != None):
            time.sleep(5)
            response = cloudCompute.queryVM(my_token_id, compute_id)
        
        ipaddr=response.json()['server']['addresses']['private'][0]['addr']
        modelFunctions.add_instance(uname, this_image.cloudId, compute_id, ipaddr, instance_name)

