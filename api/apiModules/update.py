import api.cloudModules.cloudAuth as cloudAuth
import api.cloudModules.cloudCompute as cloudCompute
import api.cloudModules.cloudImages as cloudImages
import api.configuration.globalVars as globalVars
import api.models as modelFunctions
import json


def updateCatalog(my_token_id):
    response = cloudImages.getImageList(my_token_id)
    
    for image in response.json()['images']:
        modelFunctions.getOrCreateImage(image['id'], image['name'], '')
    
    
