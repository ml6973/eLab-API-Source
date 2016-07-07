from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Image

class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Image
		fields = ('name', 'description')

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'email')