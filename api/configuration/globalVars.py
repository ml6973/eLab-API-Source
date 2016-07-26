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

def getConfig():
   global config
   config = ConfigParser.RawConfigParser()
   config.read('api/configuration/config.txt')
