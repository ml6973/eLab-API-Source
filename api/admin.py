from django.contrib import admin
from .models import Cloud, Instance, Image, UserProfile
# Register your models here.

admin.site.register(Cloud)
admin.site.register(Instance)
admin.site.register(Image)
admin.site.register(UserProfile)
