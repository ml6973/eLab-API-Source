import cloudModules.cloudAuth as cloudAuth
import cloudModules.cloudCompute as cloudCompute
import cloudModules.cloudImages as cloudImages
import configuration.globalVars as globalVars
import databaseModules.dbFunctions as dbFunctions
import peewee
import time
from peewee import *

def registerUser(uname, my_token_id):
    this_user = dbFunctions.getOrCreateUser(uname)
    createNewUserInstances(uname, my_token_id)

def createNewUserInstances(uname, my_token_id):
    for this_image in dbFunctions.Image.select():
        instance_name = uname + '-' + str(this_image.id)
        compute_id = cloudCompute.bootVM(my_token_id, instance_name, this_image.cloudId)

        time.sleep(5)
        response = cloudCompute.queryVM(my_token_id, compute_id)

        while(response.json()['server']['OS-EXT-STS:task_state'] != None):
            time.sleep(5)
            response = cloudCompute.queryVM(my_token_id, compute_id)
        
        ipaddr=response.json()['server']['addresses']['private'][0]['addr']
        dbFunctions.addInstance(uname, this_image.cloudId, compute_id, ipaddr)

        

