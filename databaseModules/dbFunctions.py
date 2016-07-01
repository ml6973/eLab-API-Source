import json
import datetime
import peewee
from peewee import *


db = MySQLDatabase("eLabAPI_ryan", user="ryan", passwd="password", host="129.114.110.223", port=3306)

class User(peewee.Model):
    userName = peewee.CharField(unique=True)
    authentication = peewee.CharField()
    dateCreated = peewee.DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        database = db

class Image(peewee.Model):
    description = peewee.TextField()
    name = peewee.CharField(unique=True)
    cloudId = peewee.CharField(unique=True)
    dateCreated = peewee.DateTimeField(default=datetime.datetime.now())

    class Meta:
        database=db

class Instance(peewee.Model):
    user = peewee.ForeignKeyField(User)
    image = peewee.ForeignKeyField(Image)
    name = peewee.CharField()
    computeId = peewee.CharField()
    ipaddr = peewee.CharField()
    dateCreated = peewee.DateTimeField(default=datetime.datetime.now())
    
    class Meta:
        database=db

def create_all_tables():
    User.create_table()
    Image.create_table()
    Instance.create_table()
    db.commit()

def getVMList(user_id):
    this_user = User.get(User.id == user_id)
    instance_dict = {}

    for instance in Instance.select().where(Instance.user == this_user):
        instance_dict[instance.name] = instance.ipaddr    

    print(json.dumps(instance_dict, indent=4))
    return instance_dict

def getCatalog():
    catalog = {}
    for image in Image.select():
        catalog[image.name] = image.description

    print(json.dumps(catalog, indent=4))
    return catalog

def addUser(uname):
    new_user = User(userName=uname, authentication="true")
    new_user.save()

def getOrCreateUser(uname):
    new_user, created = User.get_or_create(userName=uname, authentication="true")
    return new_user

def addImage(cloudId, name, description):
    new_image = Image(cloudId = cloudId, name=name, description=description)
    new_image.save()

def getOrCreateImage(cloudId, name, description):
    image, created = Image.get_or_create(cloudId = cloudId, name=name, description=description)
    return created
    
def addInstance(username, imageid, computeid, ipaddr, instance_name):
    new_instance = Instance(user=User.get(User.userName == username),
                            image=Image.get(Image.cloudId == imageid),
                            computeId = computeid,
                            ipaddr = ipaddr,
                            name = instance_name)
    new_instance.save()

getVMList(1)
#getCatalog()
#create_all_tables()
#user_ryan = User(userName="ryan", authentication="true")
#user_ryan.save()

#myimage = Image(description="machine learning", cloudId="oiawjeofjawoejfoiweijfjo2893492394")
#myimage.save()


#myInstance = Instance(user=User.get(User.userName=='ryan'), 
#                      image=Image.get(Image.description=='machine learning'),
#                      computeId = 'awfadgfgf',
#                      ipaddr = '10.0.0.5')
#myInstance.save()
