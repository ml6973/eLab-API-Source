from django.contrib import admin
from .models import Instance, Image, UserProfile
# Register your models here.

admin.site.register(Instance)
admin.site.register(Image)
admin.site.register(UserProfile)
