from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import json
import datetime

class Image(models.Model):
    description = models.CharField(max_length=1000)
    name = models.CharField(unique=True, max_length=50)
    cloudId = models.CharField(unique=True, max_length=50)
    dateCreated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Instance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    computeId = models.CharField(max_length=100)
    ipaddr = models.CharField(max_length=20)
    dateCreated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

def addInstance(username, imageid, computeid, ipaddr, instance_name):
    new_instance = Instance(user=User.objects.get(username = username),
                            image=Image.objects.get(cloudId = imageid),
                            computeId = computeid,
                            ipaddr = ipaddr,
                            name = instance_name)
    new_instance.save()

def getOrCreateImage(cloudId, name, description):
    image, created = Image.objects.get_or_create(cloudId = cloudId, name=name, description=description)
    return image

def addImage(cloudId, name, description):
    new_image = Image(cloudId = cloudId, name=name, description=description)
    new_image.save()
    
def addUser(uname):
    new_user = User(userName=uname)
    new_user.save()

def getOrCreateUser(uname):
    new_user, created = User.objects.get_or_create(userName=uname)
    return new_user