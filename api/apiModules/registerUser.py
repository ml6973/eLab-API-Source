import api.cloudModules.cloudAuth as cloudAuth
import api.cloudModules.cloudCompute as cloudCompute
import api.cloudModules.cloudImages as cloudImages
import api.configuration.globalVars as globalVars
import time
from passlib.hash import sha512_crypt
import string, random
from django.contrib.auth.models import User
from api.models import Image, Instance
import api.models as modelFunctions
from subprocess import call
from rest_framework import status

def registerUser(uname, email, preferred_pass, external_id, my_token_id):
    this_user, created = modelFunctions.get_or_create_user(uname, email, preferred_pass, external_id)
    if created is True:
        create_config(uname, preferred_pass)
        call("base64 cfg.sh > cfgb64.sh", shell=True)
        createNewUserInstances(uname, my_token_id)
        enough_floating_ips = assign_floating_ips(uname, my_token_id)

        if enough_floating_ips == False:
            delete_user(uname, my_token_id)
            return status.HTTP_503_SERVICE_UNAVAILABLE

        return status.HTTP_201_CREATED
    else:
        delete_user(uname, my_token_id)
        return status.HTTP_500_INTERNAL_SERVER_ERROR

def createNewUserInstances(uname, my_token_id):
    for this_image in Image.objects.all():
        instance_name = uname + '-' + str(this_image.name)
        compute_id = cloudCompute.bootVM(my_token_id, instance_name, this_image.cloudId)

        time.sleep(5)
        response = cloudCompute.queryVM(my_token_id, compute_id)

        while(response.json()['server']['OS-EXT-STS:task_state'] != None):
            time.sleep(5)
            response = cloudCompute.queryVM(my_token_id, compute_id)
        
        #ip address set to 0.0.0.0 before floating ip is assigned
        ipaddr = '0.0.0.0'
        
        modelFunctions.add_instance(uname, this_image.cloudId, compute_id, ipaddr, instance_name)

def delete_user(uname, my_token_id):
    #first delete all labs for this user on the cloud
    for this_instance in Instance.objects.filter(user=User.objects.get(username=uname)):
        cloudCompute.deleteVM(my_token_id, this_instance.computeId)

    #delete user from database, will also delete all info owned by this user in database
    this_user = User.objects.get(username=uname)
    this_user.delete()


def assign_floating_ips(uname, my_token_id):
    for this_instance in Instance.objects.filter(user=User.objects.get(username=uname)):
        floating_ip = cloudCompute.get_unused_floating_ip(my_token_id)
        print floating_ip

        if floating_ip is not None:
            cloudCompute.associate_floating_ip(my_token_id, this_instance.computeId, floating_ip)
            this_instance.ipaddr = floating_ip
            this_instance.save()
        else:
            print "All Floating IPs are in use. Please add more to the pool."
            return False

    return True

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
