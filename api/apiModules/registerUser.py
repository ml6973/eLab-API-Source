import api.cloudModules.cloudAuth as cloudAuth
import api.cloudModules.cloudCompute as cloudCompute
import api.cloudModules.cloudImages as cloudImages
import api.configuration.globalVars as globalVars
import time
from api.models import Image, Instance
import api.models as modelFunctions
from subprocess import call

def registerUser(uname, email, preferred_pass, my_token_id):
    this_user, created = modelFunctions.get_or_create_user(uname, email, preferred_pass)
    if created is True:
        create_config(uname, preferred_pass)
        call("base64 cfg.sh > cfgb64.sh", shell=True)
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
        
        #make sure we are capturing the ipv4 ip address
        if(response.json()['server']['addresses']['internal'][0]['version'] == 6):
            ipaddr=response.json()['server']['addresses']['internal'][1]['addr']
        else:
            ipaddr=response.json()['server']['addresses']['internal'][0]['addr']
        
        modelFunctions.add_instance(uname, this_image.cloudId, compute_id, ipaddr, instance_name)

def create_config(uname, preferred_pass):
    fp = open('cfg.sh', 'w')
    fp.truncate()

    fp.write('#cloud-config\n')
    fp.write('chpasswd:\n')
    fp.write('  list: |\n')
    fp.write('    root:' + preferred_pass + '\n')
    fp.write('  expire: False\n')
    fp.close
