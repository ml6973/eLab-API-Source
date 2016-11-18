from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_pass = models.CharField(max_length=50)
    external_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.user.username


class Cloud(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    name = models.CharField(max_length=50)
    cloud = models.ForeignKey('Cloud')
    cloudId = models.CharField(max_length=50)
    dateCreated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('name', 'cloud'), ('cloud', 'cloudId'))

    def __str__(self):
        return self.name


class Instance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=50)
    cloud = models.ForeignKey('Cloud')
    computeId = models.CharField(max_length=100)
    ipaddr = models.CharField(max_length=20)
    dateCreated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (('cloud', 'computeId'), ('user', 'image'))

    def __str__(self):
        return self.name


def add_instance(username, image_id, compute_id, ip_address, instance_name):
    new_instance = Instance(user=User.objects.get(username=username),
                            image=Image.objects.get(cloudId=image_id),
                            computeId=compute_id,
                            ipaddr=ip_address,
                            name=instance_name)
    new_instance.save()


def get_or_create_image(cloud, image_id, name, description):
    image, created = Image.objects.get_or_create(cloud=cloud, 
                                                 cloudId=image_id, 
						 name=name, 
						 description=description)
    return (image, created)


def add_image(cloud, cloud_id, name, description):
    new_image = Image(cloud=cloud, cloudId=cloud_id, name=name, description=description)
    new_image.save()


def add_user(this_username):
    new_user = User(userName=this_username)
    new_user.save()


def get_or_create_user(this_username, this_email, this_preferred_pass,
                       this_external_id):
    new_user, created = User.objects.get_or_create(username=this_username,
                                                   email=this_email)
    if created is True:
        new_user_profile = UserProfile(user=new_user,
                                       preferred_pass=this_preferred_pass,
                                       external_id=this_external_id)
        new_user_profile.save()
    return (new_user, created)


def get_labs(user_id):
    this_user_profile = UserProfile.objects.get(external_id=user_id)
    this_user = this_user_profile.user
    instance_dict = {}

    for instance in Instance.objects.filter(user=this_user):
        instance_dict[instance.image.name] = (instance.ipaddr + ' - ' +
                                              instance.image.description)

    return instance_dict
