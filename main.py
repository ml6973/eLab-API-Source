import cloudModules.cloudAuth as cloudAuth
import cloudModules.cloudCompute as cloudCompute
import cloudModules.cloudImages as cloudImages
import configuration.globalVars as globalVars

globalVars.init()  #Initialize global variables

my_token_id = cloudAuth.auth()
#cloudCompute.bootVM(my_token_id)
cloudImages.getImageList(my_token_id)
