from django.contrib import admin
from .models import User, Permission, UserPermission

admin.site.register((User, Permission, UserPermission))
