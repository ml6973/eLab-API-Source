import ConfigParser

def init():
   getConfig()

   global tenant_id
   tenant_id = ""

   global authURL
   authURL = config.get('GlobalInformation', 'AuthURL')

   global computeURL
   computeURL = config.get('GlobalInformation', 'ComputeURL')

   global baseURL
   baseURL = config.get('GlobalInformation', 'BaseURL')

   global computeURL2
   computeURL2 = config.get('GlobalInformation', 'ComputeURL2')

   global tenantName
   tenantName = config.get('GlobalInformation', 'tenantName')

   global networkID
   networkID = config.get('GlobalInformation', 'networkID')

   global cloudUsername
   cloudUsername = config.get('GlobalInformation', 'cloudUsername')

   global cloudPassword
   cloudPassword = config.get('GlobalInformation', 'cloudPassword')

def getConfig():
   global config
   config = ConfigParser.RawConfigParser()
   config.read('api/configuration/config.txt')
