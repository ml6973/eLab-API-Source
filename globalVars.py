import ConfigParser

def init():
   getConfig()

   global tenant_id
   tenant_id = ""

   global authURL
   authURL = config.get('GlobalInformation', 'AuthURL')

   global computeURL
   computeURL = config.get('GlobalInformation', 'ComputeURL')

def getConfig():
   global config
   config = ConfigParser.RawConfigParser()
   config.read('config.txt')
