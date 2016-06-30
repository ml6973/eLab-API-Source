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
    cloudId = peewee.CharField()
    dateCreated = peewee.DateTimeField(default=datetime.datetime.now())

    class Meta:
        database=db

class Instance(peewee.Model):
    user = peewee.ForeignKeyField(User)
    image = peewee.ForeignKeyField(Image)
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

#user_ryan = User(userName="ryan", authentication="true")
#user_ryan.save()

#myimage = Image(description="machine learning", cloudId="oiawjeofjawoejfoiweijfjo2893492394")
#myimage.save()


#myInstance = Instance(user=User.get(User.userName=='ryan'), 
#                      image=Image.get(Image.description=='machine learning'),
#                      computeId = 'awfadgfgf',
#                      ipaddr = '10.0.0.5')
#myInstance.save()
