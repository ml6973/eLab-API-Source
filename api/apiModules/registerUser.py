import api.cloudModules.cloudAuth as cloudAuth
import api.cloudModules.cloudCompute as cloudCompute
import api.cloudModules.cloudImages as cloudImages
import api.configuration.globalVars as globalVars
import time
from passlib.hash import sha512_crypt
import string, random
from api.models import Image, Instance
import api.models as modelFunctions
from subprocess import call

def registerUser(uname, email, preferred_pass, external_id, my_token_id):
    this_user, created = modelFunctions.get_or_create_user(uname, email, preferred_pass, external_id)
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

    fp.write('#!/bin/sh\n')
    fp.write('sudo adduser ' + uname + '\n')
    fp.write('echo "'+ uname + ':' + preferred_pass + '" | sudo chpasswd -')

    fp.close
'''
def create_config(uname, preferred_pass):
    mysalt =''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))
    hashed_pass = sha512_crypt.encrypt(preferred_pass,salt=mysalt, rounds=5000, implicit_rounds=True)

    print hashed_pass

    fp = open('cfg.sh', 'w')
    fp.truncate()

    fp.write('#cloud-config\n')
    fp.write('users:\n')
    fp.write('  - name: ' + uname + '\n')
    fp.write('    groups: sudo\n')
    fp.write('    sudo: [\'ALL=(ALL) NOPASSWD:ALL\']\n')
    fp.write('    lock-passwd: False\n')
    fp.write('    passwd: ' + hashed_pass + '\n')
    fp.close
'''
