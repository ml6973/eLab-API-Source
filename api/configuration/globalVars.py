import ConfigParser


def init():
    get_config()

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

    global masterKey
    masterKey = config.get('GlobalInformation', 'masterKey')

    global apiUser
    try:
        apiUser = config.get('GlobalInformation', 'apiUser')
    except ConfigParser.NoOptionError:
        pass

    global apiPass
    try:
        apiPass = config.get('GlobalInformation', 'apiPass')
    except ConfigParser.NoOptionError:
         pass

    global awsAccess
    try:
         awsAccess = config.get('GlobalInformation', 'awsAccess')
    except ConfigParser.NoOptionError:
         pass

    global awsSecret
    try:
         awsSecret = config.get('GlobalInformation', 'awsSecret')
    except ConfigParser.NoOptionError:
         pass

    global awsRegion
    try:
        awsRegion = config.get('GlobalInformation', 'awsRegion')
    except ConfigParser.NoOptionError:
        pass

    
    global jetstreamAuthURL
    try:
        jetstreamAuthURL = config.get('GlobalInformation', 'jetstreamAuthURL')
    except ConfigParser.NoOptionError:
        pass

    global jetstreamComputeURL
    try:
        jetstreamComputeURL = config.get('GlobalInformation', 'jetstreamComputeURL')
    except ConfigParser.NoOptionError:
        pass

    global jetstreamBaseURL
    try:
        jetstreamBaseURL = config.get('GlobalInformation', 'jetstreamBaseURL')
    except ConfigParser.NoOptionError:
        pass

    global jetstreamComputeURL2
    try:
        jetstreamComputeURL2 = config.get('GlobalInformation', 'jetstreamComputeURL2')
    except ConfigParser.NoOptionError:
         pass

    global jetstreamTenantID
    try:
        jetstreamTenantID = config.get('GlobalInformation', 'jetstreamTenantID')
    except ConfigParser.NoOptionError:
        pass

    global jetstreamNetworkID
    try:
        jetstreamNetworkID = config.get('GlobalInformation', 'jetstreamNetworkID')
    except ConfigParser.NoOptionError:
        pass

    global jetstreamCloudUsername
    try:
        jetstreamCloudUsername = config.get('GlobalInformation', 'jetstreamCloudUsername')
    except ConfigParser.NoOptionError:
        pass

    global jetstreamCloudPassword
    try:
        jetstreamCloudPassword = config.get('GlobalInformation', 'jetstreamCloudPassword')
    except ConfigParser.NoOptionError:
        pass



def get_config():
    global config
    config = ConfigParser.RawConfigParser()
    config.read('api/configuration/config.txt')
