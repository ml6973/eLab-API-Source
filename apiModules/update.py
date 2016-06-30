import cloudModules.cloudAuth as cloudAuth
import cloudModules.cloudCompute as cloudCompute
import cloudModules.cloudImages as cloudImages
import configuration.globalVars as globalVars
import databaseModules.dbFunctions as dbFunctions
import json

def updateCatalog(my_token_id):
    response = cloudImages.getImageList(my_token_id)
    
    for image in response.json()['images']:
        dbFunctions.getOrCreateImage(image['id'], image['name'], '')
    
    
