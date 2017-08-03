from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Image, Cloud


class CloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloud
	fields = ('name',)


class ImageSerializer(serializers.ModelSerializer):
    cloud = CloudSerializer(read_only=True)

    class Meta:
        model = Image
        fields = ('name', 'description', 'cloud')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
