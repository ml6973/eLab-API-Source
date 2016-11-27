import time
import string
import random
import getpass
import hashlib

from passlib.hash import sha512_crypt
from django.contrib.auth.models import User
from subprocess import call
from rest_framework import status

from api.models import Cloud, Image, Instance, UserProfile
import api.apiModules.cloudAdapter as cloudAdapter
import api.cloudModules.cloudCompute as cloudCompute
import api.configuration.globalVars as globalVars
import api.models as modelFunctions


def registerUser(uname, email, preferred_pass, external_id):
    this_user, created = modelFunctions.get_or_create_user(
            uname, email, preferred_pass, external_id)

    '''
    if created is True:
        
        create_config(uname, preferred_pass)
        call("base64 cfg.sh > cfgb64.sh", shell=True)
        create_new_user_instances(uname, my_token_id)
        enough_floating_ips = assign_floating_ips(uname, my_token_id)

        if enough_floating_ips == False:
            delete_user(uname, my_token_id)
            return status.HTTP_503_SERVICE_UNAVAILABLE
        
    else:
        delete_user(uname, my_token_id)
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    '''

    if created is True:
        return status.HTTP_201_CREATED
    else:
        return status.HTTP_200_OK


def enroll_user(user_id, image_name, cloud):
    # grab user profile object and user object from user_id
    this_user_profile = UserProfile.objects.get(external_id=user_id)
    this_user = this_user_profile.user

    # grab this users username and preferred lab password
    uname = this_user.username
    preferred_pass = this_user_profile.preferred_pass

    # grab image object from image_id
    cloudObject = Cloud.objects.get(name=cloud)
    this_image = Image.objects.get(name=image_name, cloud=cloudObject.id)
    instance_name = uname + '-' + str(this_image.name)

    # check if the user already has an instance running
    exists = True
    try:
        checkInstance = Instance.objects.get(user=this_user, image=this_image)
    except Instance.DoesNotExist:
        exists = False
    
    if (exists):
        return status.HTTP_200_OK


    # create config file and encode in base64 to pass to vm
    create_config(uname, preferred_pass)
    call("base64 cfg.sh > cfgb64.sh", shell=True)

    # create lab environment, save compute id(unique) of this instance
    this_compute_id = cloudAdapter.boot_vm(instance_name, this_image.cloudId, cloud)

    # continually sleeps until cloud has fully populated the response with
    # the data we need
    time.sleep(5)
    response = cloudAdapter.query_vm(this_compute_id, cloud)

    while(response.json()['server']['OS-EXT-STS:task_state'] != None):
        time.sleep(5)
	response = cloudAdapter.query_vm(this_compute_id, cloud)

    # ip address set to 0.0.0.0 before floating ip is assigned
    ipaddr = '0.0.0.0'

    # add this instance to database
    modelFunctions.add_instance(uname, this_image.cloudId, this_compute_id,
                                ipaddr, instance_name, cloudObject)

    this_instance = Instance.objects.get(computeId=this_compute_id)

    # find an unused floating ip and assign it to this vm
    floating_ip = cloudAdapter.get_unused_floating_ip(cloud)
    print floating_ip

    if floating_ip is not None:
	cloudAdapter.associate_floating_ip(this_compute_id, floating_ip, cloud)
        this_instance.ipaddr = floating_ip
        this_instance.save()
    else:
        print "All Floating IPs are in use. Please add more to the pool."
        return status.HTTP_500_INTERNAL_SERVER_ERROR

    return status.HTTP_201_CREATED


'''
def create_new_user_instances(uname, my_token_id):
    for this_image in Image.objects.all():
        instance_name = uname + '-' + str(this_image.name)
        compute_id = cloudCompute.boot_vm(my_token_id, instance_name,
                                         this_image.cloudId)

        time.sleep(5)
        response = cloudCompute.query_vm(my_token_id, compute_id)

        while(response.json()['server']['OS-EXT-STS:task_state'] != None):
            time.sleep(5)
            response = cloudCompute.query_vm(my_token_id, compute_id)

        # ip address set to 0.0.0.0 before floating ip is assigned
        ipaddr = '0.0.0.0'

        modelFunctions.add_instance(uname, this_image.cloudId, compute_id,
                                    ipaddr, instance_name)


'''
def delete_user(uname, my_token_id):
    # first delete all labs for this user on the cloud
    for this_instance in Instance.objects.filter(
            user=User.objects.get(username=uname)):
        cloudCompute.delete_vm(my_token_id, this_instance.computeId)

    # delete user from database, will also delete all info owned by this
    # user in database
    this_user = User.objects.get(username=uname)
    this_user.delete()


def assign_floating_ips(uname, my_token_id):
    for this_instance in Instance.objects.filter(
            user=User.objects.get(username=uname)):
        floating_ip = cloudCompute.get_unused_floating_ip(my_token_id)
        print floating_ip

        if floating_ip is not None:
            cloudCompute.associate_floating_ip(my_token_id,
                                               this_instance.computeId,
                                               floating_ip)
            this_instance.ipaddr = floating_ip
            this_instance.save()
        else:
            print "All Floating IPs are in use. Please add more to the pool."
            return False

    return True
'''
def create_config(uname, preferred_pass):
    fp = open('cfg.sh', 'w')
    fp.truncate()

    fp.write('#!/bin/sh\n')
    fp.write('sudo useradd ' + uname + '\n')
    fp.write('echo "'+ uname + ':' + preferred_pass + '" | sudo chpasswd -\n')
    fp.write('echo "' + uname + '  ALL=(ALL:ALL) ALL" >> /etc/sudoers\n')
    fp.write('sudo sed -i \'s|[#]*PasswordAuthentication no|'
             + 'PasswordAuthentication yes|g\' /etc/ssh/sshd_config\n')
    fp.write('sudo service ssh restart')


    fp.close
'''


def create_config(uname, preferred_pass):
    mysalt = ''.join(random.choice(string.ascii_letters +
                     string.digits) for i in range(16))
    hashed_pass = sha512_crypt.encrypt(preferred_pass, salt=mysalt,
                                       rounds=5000, implicit_rounds=True)

    # code to create password for jupyter notebook
    salt_len = 12
    algorithm = 'sha1'
    h = hashlib.new(algorithm)
    salt = ('%0' + str(salt_len) + 'x') % random.getrandbits(4 * salt_len)
    h.update(preferred_pass + salt)
    jupyter_pass = ':'.join((algorithm, salt, h.hexdigest()))

    print hashed_pass
    globalVars.init()

    fp = open('cfg.sh', 'w')
    fp.truncate()

    fp.write('#cloud-config\n')
    fp.write('users:\n')
    fp.write('  - name: ' + uname + '\n')
    fp.write('    ssh-authorized-keys:\n')
    fp.write('      - ' + globalVars.masterKey + '\n')
    fp.write('    groups: sudo\n')
    fp.write('    shell: /bin/bash\n')
    fp.write('    sudo: [\'ALL=(ALL) NOPASSWD:ALL\']\n')
    fp.write('    lock-passwd: False\n')
    fp.write('    passwd: ' + hashed_pass + '\n')
    fp.write('runcmd:\n')
    fp.write('  - touch /home/ryan/testfile.txt\n')
    fp.write('  - [ sudo, sed, -i, \'s/[#]*PasswordAuthentication no/'
             'PasswordAuthentication yes/g\', /etc/ssh/sshd_config ]\n')
    fp.write('  - sudo mv /home/' + uname + '/.ssh /home/' + uname + '/.ssh_temp\n')
    fp.write('  - sudo cp -r /home/cc/. /home/' + uname + '\n')
    fp.write('  - sudo rm -r /home/' + uname + '/.ssh\n')
    fp.write('  - sudo mv /home/' + uname + '/.ssh_temp /home/' + uname + '/.ssh\n')
    fp.write('  - sudo service ssh restart\n')
    fp.write('  - sudo sed -i "s/c\.NotebookApp\.password.*/c\.NotebookApp\.password = u\\\'' + jupyter_pass + '\\\'/g" /home/' + uname + '/.jupyter/jupyter_notebook_config.py\n')
    fp.write('  - sudo su - ' + uname + ' -c "sudo jupyter notebook &"\n')
    fp.close
