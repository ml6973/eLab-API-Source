import cloudAuth
import cloudCompute
import globalVars

globalVars.init()  #Initialize global variables

my_token_id = cloudAuth.auth()
cloudCompute.bootVM(my_token_id)
